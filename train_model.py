import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
print("loading CICIDS dataset...")

data = pd.read_csv("DATA/cicids_sample.csv")
print(data.columns)
features = data[
    ["Flow Duration",
     "Total Fwd Packets",
     "Flow Bytes/s",
     "Flow Packets/s",
     "Average Packet Size",]
]
print("Training Isolation Forest model...")

model = IsolationForest(contamination=0.03,random_state=42)

model.fit(features)

joblib.dump(model,"MODEL/anomaly_model.pkl")

print("Model trained and saved successfully.")