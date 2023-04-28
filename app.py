from flask import Flask, request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)

# Set up OAuth2 client ID and secret from Google Cloud console
client_id = '246245084452-u6g6040ajj1cabipleh83o6pn04vccm5.apps.googleusercontent.com'
client_secret = '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'

# Set up redirect URI for Google OAuth2 flow
redirect_uri = 'http://localhost:8080/oauth2callback'

# Set up scopes for accessing user's contacts
scopes = ['https://www.googleapis.com/auth/contacts.readonly']

# Set up Google API client
service_name = 'people'
service_version = 'v1'
client = None

# Set up Google OAuth2 flow
flow = Flow.from_client_config(
    {
        'web': {
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uris': [redirect_uri],
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'userinfo_uri': 'https://www.googleapis.com/oauth2/v1/userinfo',
            'scope': ' '.join(scopes)
        }
    },
    scopes=scopes
)

@app.route('/')
def index():
    # Redirect user to Google OAuth2 authentication page
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return f'<a href="{authorization_url}">Click here to authorize this app to access your Google contacts</a>'

@app.route('/oauth2callback')
def oauth2callback():
    # Exchange authorization code for access token
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Use access token to create Google API client
    global client
    credentials = Credentials.from_authorized_user_info(info=flow.credentials.to_json())
    client = build(service_name, service_version, credentials=credentials)

    return 'Authorized!'

@app.route('/contacts')
def contacts():
    # Make request to People API to retrieve user's contacts
    results = client.people().connections().list(
        resourceName='people/me',
        personFields='names,emailAddresses'
    ).execute()

    # Extract name and email address from each contact
    contacts = []
    for person in results['connections']:
        if 'emailAddresses' in person:
            name = person.get('names', [{}])[0].get('displayName', '')
            email = person['emailAddresses'][0].get('value', '')
            contacts.append({'name': name, 'email': email})

    # Display list of contacts
    return '<br>'.join([f"{c['name']}: {c['email']}" for c in contacts])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
