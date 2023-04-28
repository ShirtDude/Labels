from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up the credentials object
creds = Credentials.from_authorized_user_file('creds.json', ['https://www.googleapis.com/auth/contacts', 'https://www.googleapis.com/auth/contacts.other.readonly'])

# Set up the People API client
people_service = build('people', 'v1', credentials=creds)

# Set up the email address of the Google account to share with
share_email = 'example@gmail.com'

# Get the resource name of your contact list
contact_list = people_service.contactGroups().list().execute()
resource_name = None
for group in contact_list.get('contactGroups', []):
    if group.get('name') == 'My Contacts':
        resource_name = group['resourceName']
        break

# Share your contact list with the other Google account
if resource_name is not None:
    try:
        people_service.contactGroups().share(
            resourceName=resource_name,
            body={'emailAddress': share_email}
        ).execute()
        print('Contacts shared successfully with {}'.format(share_email))
    except HttpError as error:
        print('An error occurred: {}'.format(error))
else:
    print('Could not find My Contacts group')
