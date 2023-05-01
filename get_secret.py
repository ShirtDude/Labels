import openai_secret_manager
from googleapiclient.discovery import build


def get_google_contacts_service():
    """Returns a Google Contacts service object."""
    secrets = openai_secret_manager.get_secret("google")
    api_service_name = "people"
    api_version = "v1"
    scopes = ["https://www.googleapis.com/auth/contacts"]
    credentials = secrets["web"]
    service = build(api_service_name, api_version, credentials=credentials)
    return service
