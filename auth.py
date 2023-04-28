import os
import json
import webbrowser
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate(scopes):
    # Load credentials from the file if it exists, otherwise start the OAuth flow
    creds = None
    if os.path.exists('creds.json'):
        with open('creds.json', 'r') as f:
            creds_data = json.load(f)
        creds = Credentials.from_authorized_user_info(creds_data, scopes=scopes)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes)
        creds = flow.run_local_server(port=0)
        # Save the credentials to a file
        creds_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes,
        }
        with open('creds.json', 'w') as f:
            json.dump(creds_data, f)
    return creds
