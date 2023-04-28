import auth
from googleapiclient.discovery import build

# Scopes to request access to
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Call auth.authenticate() to get credentials
creds = auth.authenticate(SCOPES)

# Build the Gmail API client
service = build('gmail', 'v1', credentials=creds)

# Call Gmail API to get user labels
results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])
if not labels:
    print('No labels found.')
else:
    print('Labels:')
    for label in labels:
        print(label['name'])
