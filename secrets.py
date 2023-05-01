import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import openai_secret_manager
from utils import save_secret

# Define your secrets here
MY_SECRET = "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"
print(MY_SECRET)

# Save Google client ID
save_secret("google_client_id", "246245084452-u6g6040ajj1cabipleh83o6pn04vccm5.apps.googleusercontent.com")

# Save Google client secret
save_secret("google_client_secret", "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")

# Save Google redirect URI
save_secret("google_redirect_uri", "http://localhost:8080/oauth2callback")

# Save OpenAI API key
save_secret("openai_api_key", "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")
# Set up scopes for accessing user's contacts
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

# Set up Google API client
SERVICE_NAME = 'people'
SERVICE_VERSION = 'v1'


def save_openai_secret():
    """
    Save the OpenAI API key using OpenAI Secret Manager.
    """
    # Use the openai_secret_manager module to save the secret
    openai_secret_manager.save_secret("openai", MY_SECRET)


def get_google_contacts_service():
    """
    Returns an authorized Google People API service object.
    """
    # Fetch the credentials from the secret manager
    secrets = openai_secret_manager.get_secret("google")

    # Load the credentials into a Credentials object
    creds = Credentials.from_authorized_user_info(secrets)

    # Build the Google People API client
    service = build("people", "v1", credentials=creds)

    # Return the client
    return service


if __name__ == "__main__":
    save_openai_secret()
    get_google_contacts_service()
