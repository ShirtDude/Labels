from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth.exceptions
import os

creds_file = 'secrets.json'
scopes = ['https://www.googleapis.com/auth/contacts', 'https://www.googleapis.com/auth/contacts.other.readonly',
          'https://www.googleapis.com/auth/contacts.readonly', 'https://www.googleapis.com/auth/contacts']
creds = None

if os.path.exists('secrets.json'):
    creds = Credentials.from_authorized_user_file('secrets.json', scopes)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except google.auth.exceptions.RefreshError:
            flow = InstalledAppFlow.from_client_config(client_config={
                'installed': {
                    'client_id': '246245084452-9ddfpi1hrvv60e8fh0eq4mbap1dgjt79.apps.googleusercontent.com',
                    'client_secret': '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',
                    'redirect_uris': ['http://localhost:8080'],
                    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                    'token_uri': 'https://oauth2.googleapis.com/token',
                    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs'
                }
            }, scopes=scopes)
            creds = flow.run_local_server()
        with open(creds_file, 'w') as token:
            token.write(creds.to_json())
    else:
        flow = InstalledAppFlow.from_client_config(client_config={
            'installed': {
                'client_id': '246245084452-9ddfpi1hrvv60e8fh0eq4mbap1dgjt79.apps.googleusercontent.com',
                'client_secret': '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',
                'redirect_uris': ['http://localhost:8080'],
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
                'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs'
            }
        }, scopes=scopes)
        creds = flow.run_local_server()
        with open(creds_file, 'w') as token:
            token.write(creds.to_json())
