import openai_secret_manager
from googleapiclient.discovery import build

# Set up the API client and secrets
secrets = openai_secret_manager.get_secret("google")
api_service_name = "people"
api_version = "v1"
scopes = ["https://www.googleapis.com/auth/contacts"]
creds = secrets["web"]
service = build(api_service_name, api_version, credentials=creds)

# Print the names of the first 10 connections
connections = service.people().connections().list(resourceName='people/me', pageSize=10, personFields='names').execute().get('connections', [])
for person in connections:
    names = person.get('names', [])
    if names:
        print(names[0].get('displayName'))
