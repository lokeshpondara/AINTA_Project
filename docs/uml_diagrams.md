# AINTA UML Diagrams

## 1. Component Diagram
```mermaid
graph LR
  A[Multi-Interface Capture<br/>src/capture/packet_capture.py] --> B[Flow Extraction<br/>src/processing/flow_extractor.py]
  B --> C[Feature Engineering<br/>src/processing/feature_engineering.py]
  C --> D[Isolation Forest<br/>src/detection/anomaly_detector.py]
  C --> E[GNN Detector<br/>src/detection/gnn_detector.py]
  D --> F[Threat Intel<br/>src/detection/threat_intel.py]
  E --> F
  F --> G[Severity Engine<br/>src/detection/severity_engine.py]
  G --> H[Decision Engine<br/>src/core/decision_engine.py]
  H --> I[Streamlit SOC Dashboard<br/>dashboard.py]
  H --> J[Firewall Block<br/>src/response/windows_firewall.py]
  H --> K[Email Alerts<br/>src/response/email_alert.py]
  H --> L[SQLite + Evidence<br/>src/storage/database_manager.py<br/>evidence/*.pcap]
  H --> M[Incident Correlation<br/>src/analysis/incident_correlation.py]
  M --> H
  N[SystemController<br/>src/core/system_controller.py] -.-> H
  O[Monitor Engine<br/>src/monitoring/monitor_engine.py] --> G
```

## 2. Class Diagram
```mermaid
classDiagram
    class GNNAnomalyDetector {
        +__init__(input_dim, hidden_dim)
        +forward(data)
    }
    class SystemController {
        +__init__()
        +process_alert(alert)
        +enrich(alert)
        +score(alert)
        +prioritize(alert)
    }
    class DecisionEngine {
        +decide(incident)
    }
    class IncidentCorrelator {
        +correlate(alert)
    }
    MonitorEngine ..> SystemController
    MonitorEngine ..> DecisionEngine
    MonitorEngine ..> IncidentCorrelator
    MonitorEngine ..> GNNAnomalyDetector
```

## 3. Sequence Diagram - Threat Detection Flow
```mermaid
sequenceDiagram
    participant P as PacketCapture
    participant M as MonitorEngine
    participant FE as FlowExtractor
    participant FEng as FeatureEng
    participant Det as Detectors (IF/GNN)
    participant DE as DecisionEngine
    participant R as Response
    participant S as Storage
    participant D as Dashboard

    P->>M: capture_packets()
    M->>FE: extract_flow(packets)
    FE->>M: flows
    M->>FEng: build_features(flows)
    FEng->>M: features_df
    M->>Det: detect(features)
    Det->>M: alert
    M->>DE: process_alert(alert)
    DE->>R: block_ip() / send_email()
    DE->>S: insert_alert() / save_pcap()
    DE->>D: realtime_update()
```

## 4. Deployment Diagram
```mermaid
graph TB
  subgraph WindowsHost
    S[Windows Service<br/>windows_service.py + NSSM]
    DB[(SQLite alerts.db)]
    EV[evidence/ *.pcap *.json]
  end
  S --> DB
  S --> EV
  subgraph "SOC Dashboard"
    DASH[Streamlit<br/>localhost:8501]
  end
  S -.-> DASH
  subgraph Docker["Optional Docker"]
    DC[docker-compose.yml]
  end
  WindowsHost -.-> Docker
```

**Usage**:
- VSCode: Install Mermaid Preview extension.
- Online: mermaid.live
- PlantUML: Convert Mermaid or use VSCode PlantUML extension.
- Update docs/architecture.md: `![UML Diagrams](uml_diagrams.md)`

