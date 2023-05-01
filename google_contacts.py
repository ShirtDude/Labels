"""
Module for retrieving contacts from Google People API.
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from api_keys import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

# Set up scopes for accessing user's contacts
CONTACTS_SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

# Set up Google People API client
PEOPLE_API_NAME = 'people'
PEOPLE_API_VERSION = 'v1'

def create_google_flow():
    """
    Creates a Google OAuth2 flow for accessing user's contacts.
    """
    return Flow.from_client_config(
        {
            'web': {
                'client_id': GOOGLE_CLIENT_ID,
                'client_secret': GOOGLE_CLIENT_SECRET,
                'redirect_uris': [GOOGLE_REDIRECT_URI],
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
                'userinfo_uri': 'https://www.googleapis.com/oauth2/v1/userinfo',
                'scope': ' '.join(CONTACTS_SCOPES)
            }
        },
        scopes=CONTACTS_SCOPES
    )

def get_google_contacts_service(credentials: Credentials):
    """
    Returns a Google People API client for retrieving user's contacts.
    """
    service = build(PEOPLE_API_NAME, PEOPLE_API_VERSION, credentials=credentials)
    return service.people()
