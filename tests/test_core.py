"""Core module tests."""
from src.core.config import settings

def test_settings_load():
    assert settings.detection.ddos_threshold > 0

def test_detection_thresholds():
    det = settings.detection
    assert det.ddos_threshold >= 300

def test_response_config():
    resp = settings.response
    assert resp.email_enabled is True
    assert resp.smtp_port == 587
