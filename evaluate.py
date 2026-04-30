import pandas as pd
from sklearn.metrics import classification_report
from src.detection.anomaly_detector import load_model

print("AINTA Evaluation")
model = load_model()
if model is None:
    print("No model loaded - skipping evaluation")
    exit(1)

data = pd.read_csv('DATA/cicids_sample.csv')

features = data[['Flow Duration', 'Total Fwd Packets', 'Flow Bytes/s', 'Flow Packets/s', 'Average Packet Size']]

preds = model.predict(features)
print(classification_report(data['Label'], preds))
