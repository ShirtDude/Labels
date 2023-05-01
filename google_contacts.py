from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import openai_secret_manager

def get_secret(key_name):
    secrets = openai_secret_manager.get_secret("samsolano_labels")
    return secrets[key_name]


# Set up the scopes and the secrets
scopes = ['https://www.googleapis.com/auth/contacts']
secrets = openai_secret_manager.get_secret("google")

# Load the credentials
creds = None
if secrets:
    creds = Credentials.from_authorized_user_info(info=secrets, scopes=scopes)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_config(secrets, scopes)
        creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    openai_secret_manager.save_secret("google", creds.to_json())

# Build the Google Contacts API client
service = build('people', 'v1', credentials=creds)

# Print the names of the first 10 connections
connections = service.people().connections().list(resourceName='people/me', pageSize=10, personFields='names').execute().get('connections', [])
for person in connections:
    names = person.get('names', [])
    if names:
        print(names[0].get('displayName'))
