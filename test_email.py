import yaml
import os
import smtplib

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(ROOT_DIR, 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

response_config = config.get('response', {})
print('Testing SMTP login:')
print('User:', response_config.get('smtp_user'))
print('Server:', response_config.get('smtp_server'), response_config.get('smtp_port'))
print('Pass preview:', repr(response_config.get('smtp_pass', '')[:10]) + '...')

server = smtplib.SMTP(response_config.get('smtp_server', 'smtp.gmail.com'), response_config.get('smtp_port', 587))
server.starttls()
try:
    server.login(response_config['smtp_user'], response_config['smtp_pass'])
    print('✅ LOGIN SUCCESS - Emails will work!')
except Exception as e:
    print('❌ LOGIN FAILED:', e)
    print('Fix: Generate Gmail App Password at https://myaccount.google.com/apppasswords')
finally:
    server.quit()
print('\\nRun: python test_email.py')
