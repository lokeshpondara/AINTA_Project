import flwr as fl
from src.detection.gnn_detector import GNNAnomalyDetector
import torch
import pandas as pd

MODEL_PATH = "../models/gnn_fed.pt"

class GNNClient(fl.client.Client):
    def get_parameters(self, config):
        model = GNNAnomalyDetector()
        return [val.cpu().numpy() for _, val in model.state_dict().items()]

    def set_parameters(self, parameters):
        model = GNNAnomalyDetector()
        params_dict = zip(model.state_dict().keys(), parameters)
        state_dict = {k: torch.tensor(v) for k, v in params_dict}
        model.load_state_dict(state_dict, strict=True)
        torch.save(model.state_dict(), MODEL_PATH)

    async def fit(self, parameters, config):
        # No local model needed for stub
        print("Fit stub")
        # Load local data (simulate edge flows)
        data = pd.read_csv("../../DATA/cicids_sample.csv", nrows=1000)
        features = data[["Flow Duration", "Total Fwd Packets", "Flow Packets/s", "Flow Bytes/s", "Average Packet Size"]]
        # Stub local training
        print("Local training stub complete")
        return self.get_parameters(config={}), len(features), {}
        
        return self.get_parameters(config={}), len(data), {}

    def evaluate(self, parameters, config):
        loss, num_examples = 0.0, 1000
        return loss, num_examples, {"accuracy": 0.95}

fl.client.start_client(server_address="localhost:8080", client=GNNClient())

