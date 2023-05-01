import openai_secret_manager
import google.auth
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from . import google_contacts

# Set up the scopes and the secrets
scopes = ['https://www.googleapis.com/auth/gmail.labels']
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
        flow = google.auth.default(scopes=scopes)
        creds = flow[0]

    # Save the credentials for the next run
    openai_secret_manager.save_secret("google", creds.to_json())

# Build the Gmail API client
service = build('gmail', 'v1', credentials=creds)

def create_label(label_name):
    """Create a new label in Gmail"""
    try:
        label = {
            'name': label_name,
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show',
            'color': {'backgroundColor': '#ffffff'}
        }

        # Call the Gmail API to create the label
        service.users().labels().create(userId='me', body=label).execute()
        print(f"Label {label_name} created successfully!")
    except HttpError as error:
        print(f"An error occurred: {error}")
        label = None
    return label

def get_contacts():
    """Get a list of contacts from Google Contacts"""
    # Build the Google Contacts API client
    service = contacts.get_people_service()

    # Get all connections
    connections = service.people().connections().list(resourceName='people/me', personFields='names,emailAddresses').execute().get('connections', [])

    # Create a list of contacts with their name and email address
    contacts_list = []
    for person in connections:
        names = person.get('names', [])
        email_addresses = person.get('emailAddresses', [])
        if names and email_addresses:
            contacts_list.append({'name': names[0].get('displayName'), 'email': email_addresses[0].get('value')})

    return contacts_list

def add_label_to_message(label_name, message_id):
    """Add a label to a Gmail message"""
    try:
        # Call the Gmail API to add the label to the message
        label = service.users().labels().get(userId='me', id=label_name).execute()
        message = service.users().messages().modify(userId='me', id=message_id,
                                                    body={'addLabelIds': [label['id']]}).execute()
        print(f"Label {label_name} added to message {message_id} successfully!")
    except HttpError as error:
        print(f"An error occurred: {error}")
        message = None
    return message
