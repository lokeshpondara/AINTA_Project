import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from torch_geometric.data import Data
from src.detection.gnn_detector import GNNAnomalyDetector
from sklearn.ensemble import IsolationForest

print("Loading CICIDS for GNN training...")

data = pd.read_csv("DATA/cicids_sample.csv", nrows=5000)
features = data[["Flow Duration", "Total Fwd Packets", "Flow Packets/s", "Flow Bytes/s", "Average Packet Size"]]

# Labels from IsolationForest baseline
baseline_model = IsolationForest(contamination=0.03)
baseline_labels = baseline_model.fit_predict(features)

# Prepare graph data
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
graphs = []
labels_list = []

for i in range(0, len(features_scaled) - 32, 32):  # Batches of 32 flows as graphs
    batch_features = features_scaled[i:i+32]
    batch_labels = baseline_labels[i:i+32]
    
    edge_index = []
    for j in range(len(batch_features)):
        if j > 0:
            edge_index += [[j-1, j], [j, j-1]]
    
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous() if edge_index else torch.empty((2,0), dtype=torch.long)
    x = torch.tensor(batch_features, dtype=torch.float)
    
    data = Data(x=x, edge_index=edge_index, y=torch.tensor(batch_labels, dtype=torch.float))
    graphs.append(data)
    labels_list.extend(batch_labels)

# Train GNN
device = torch.device('cpu')
model = GNNAnomalyDetector(input_dim=5).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

model.train()
for epoch in range(10):
    total_loss = 0
    for data in DataLoader(graphs, batch_size=1):
        data = data.to(device)
        optimizer.zero_grad()
        scores = model(data.x, data.edge_index)
        loss = F.binary_cross_entropy_with_logits(scores, data.y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    if epoch % 20 == 0:
        print(f"Epoch {epoch}, Loss: {total_loss/len(graphs):.4f}")

# Save
torch.save(model.state_dict(), "models/gnn_model.pt")
joblib.dump(scaler, "models/gnn_scaler.pkl")
print("✅ GNN trained & saved.")
