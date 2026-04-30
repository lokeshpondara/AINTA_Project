import smtplib
from email.mime.text import MIMEText
import requests
import yaml
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

def send_notification(alert):
    """Send email + Slack alert (Phase 3)"""
    config_path = os.path.join(ROOT_DIR, "config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    response_config = config.get('response', {})
    alerts_config = config.get('alerts', {})
    
    subject = f"AINTA Alert: {alert['attack']} from {alert['src_ip']} (Sev: {alert['severity']})"
    body = f"""
Time: {alert['timestamp']}
IP: {alert['src_ip']}
Attack: {alert['attack']}
Rate: {alert['packet_rate']}
Severity: {alert['severity']}
Risk: {alert.get('risk_score', 0)}
Action: BLOCK if high
"""
    
    email_to = alerts_config.get('email_to', 'admin@example.com')
    smtp_server = response_config.get('smtp_server', 'localhost')
    host = smtp_server
    
    # Email
    if response_config.get('email_enabled', True):
        # ...
        host = smtp_server  # Use loaded server
    if response_config.get('email_enabled', True):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = response_config.get('smtp_user', 'ainta@local')
        msg['To'] = email_to
        try:
            print(f"[EMAIL] Config user: {response_config.get('smtp_user', 'NOT SET')}")
            print(f"[EMAIL] Server: {host}:{response_config.get('smtp_port', 587)}")
            host = response_config.get('smtp_server', 'localhost')
            port = response_config.get('smtp_port', 25)
            server = smtplib.SMTP(host, port)
            server.starttls()
            server.login(response_config['smtp_user'], response_config['smtp_pass'])
            server.send_message(msg)
            server.quit()
            print(f"📧 Email sent to {email_to}")
        except Exception as e:
            import traceback
            print(f"[ERROR] Email FAILED: {e}")
            print(traceback.format_exc())
    
    # Slack
    slack_webhook = response_config.get('slack_webhook', '')
    if slack_webhook and response_config.get('slack_enabled', False):
        slack_data = {
            "text": f":rotating_light: AINTA Alert!\n{subject}\n``` {body} ```"
        }
        try:
            resp = requests.post(slack_webhook, json=slack_data)
            if resp.status_code == 200:
                print("💬 Slack alert sent")
        except Exception as e:
            print(f"[ERROR] Slack failed: {e}")

