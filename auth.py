import os
import json
import webbrowser
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


def authenticate(scopes):
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as f:
            token_data = json.load(f)
        creds = Credentials.from_authorized_user_info(token_data, scopes=scopes)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes)
        creds = flow.run_local_server(port=0)
        # Save the credentials to a file
        token_data = creds.to_json()
        with open('token.json', 'w') as f:
            json.dump(token_data, f)
    elif creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds
