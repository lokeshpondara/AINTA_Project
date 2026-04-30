import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data
import torch.nn as nn
import pandas as pd

import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../models", "gnn_model.pt")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "../../models", "gnn_scaler.pkl")

print(f"GNN DEBUG: __file__ dir: {os.path.dirname(__file__)}")
print(f"GNN DEBUG: MODEL_PATH: {MODEL_PATH}")
print(f"GNN DEBUG: exists model: {os.path.exists(MODEL_PATH)}")
print(f"GNN DEBUG: exists scaler: {os.path.exists(SCALER_PATH)}")

class GNNAnomalyDetector(nn.Module):
    def __init__(self, input_dim=5, hidden_dim=64):
        super().__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.conv3 = GCNConv(hidden_dim, 16)
        self.anomaly_head = nn.Linear(16, 1)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.2)
        x = F.relu(self.conv2(x, edge_index))
        x = F.relu(self.conv3(x, edge_index))
        anomaly_score = torch.sigmoid(self.anomaly_head(x)).squeeze()
        return anomaly_score

def build_graph(features_df):
    """Convert tabular flows to graph: nodes=flows, edges=temporal"""
    if features_df.empty:
        return None
    
    num_nodes = len(features_df)
    x = torch.tensor(features_df.values, dtype=torch.float)
    
    # Temporal edges (bidir chain)
    edge_index = []
    for i in range(num_nodes):
        if i > 0:
            edge_index += [[i-1, i], [i, i-1]]
    
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    
    data = Data(x=x, edge_index=edge_index)
    return data

def load_gnn_model():
    try:
        model = GNNAnomalyDetector()
        model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
        model.eval()
        
        # Load scaler
        import joblib
        scaler = joblib.load(SCALER_PATH)
        
        print("✅ GNN model loaded.")
        return model, scaler
    except FileNotFoundError:
        print("⚠️ GNN FileNotFoundError for model/scaler - check debug above")
        return None, None

def detect_gnn(model, scaler, features):
    if model is None or features.empty or len(features) < 2:
        return [0.0] * len(features)
    
    # Scale
    features_scaled = scaler.transform(features)
    data = build_graph(pd.DataFrame(features_scaled))
    
    if data is None:
        return [0.0] * len(features)
    
    with torch.no_grad():
        scores = model(data.x, data.edge_index)
    
    return scores.numpy().tolist()
