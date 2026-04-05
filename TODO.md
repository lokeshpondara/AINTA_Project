# AINTA Upgrade TODO (Approved Roadmap)
Progress tracked here. Completed steps marked [x].

## Phase 1: Stabilize Bugs (Priority 1)
- [x] Fix float conversion errors in feature_engineering.py
- [x] Robust DB init in database_manager.py (CREATE IF NOT EXISTS + WAL)
- [x] Fix 'epoch' KeyError in monitor_engine.py
- [x] Add try/catch resilience in main loop (existing)
- [x] Test 30min stable run (run_system.py successful, dashboard up)

## Phase 2: Tests & Evaluation
- [x] Create tests/ with pytest suite
- [x] evaluate.py + AINTA_Evaluation.ipynb (CICIDS metrics, baselines)
- [x] docker-compose.yml

## Phase 3: Production
- [x] YAML config (config.yaml)
- [x] Multi-interface, async
- [x] Email/Slack alerts
- [x] SIEM JSON export
- [x] Windows Firewall
- [x] systemd service

## Phase 4: Publish
- [x] docs/ UML + API.md
- [x] LICENSE, CITATION.cff
- [x] GitHub CI

## Phase 5: Advanced
- [x] GNN models
- [x] Federated learning

