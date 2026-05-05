"""Configuration using Pydantic."""
from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import SecretStr

class DetectionSettings(BaseSettings):
    ddos_threshold: int = 300
    port_scan_threshold: int = 10
    severity_block_threshold: int = 80
    anomaly_threshold: float = -0.5

class CaptureSettings(BaseSettings):
    interfaces: List[str] = ["Ethernet"]

class ResponseSettings(BaseSettings):
    email_enabled: bool = True
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = "your.email@gmail.com"
    smtp_pass: SecretStr = SecretStr("***")

class Settings(BaseSettings):
    detection: DetectionSettings = DetectionSettings()
    capture: CaptureSettings = CaptureSettings()
    response: ResponseSettings = ResponseSettings()

settings = Settings()

