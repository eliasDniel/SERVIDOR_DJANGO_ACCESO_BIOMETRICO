from pathlib import Path
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
import json
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'firebase', 'notifications.json')

def send_push_notification_v1(device_token, title, body):
    print('Entro a la send:')
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )
    credentials.refresh(Request())

    access_token = credentials.token
    project_id = credentials.project_id

    url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }

    message = {
    "message": {
        "token": device_token,
        "notification": {   # 👈 Necesario para que funcione en app cerrada
            "title": title,
            "body": body,
        },
        "android": {
            "priority": "high"
        }
    }
}
    print(f'Message: {message}')

    response = requests.post(url, headers=headers, data=json.dumps(message))
    print("Respuesta FCM:", response.status_code, response.text)
