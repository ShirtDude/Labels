from flask import Flask, request, redirect
from googleapiclient.errors import HttpError
from google_contacts import get_google_contacts_service
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)


@app.route('/')
def index():
    # Redirect user to Google OAuth2 authentication page
    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Exchange authorization code for access token
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    return 'Authorized!'


@app.route('/contacts')
def get_contacts():
    try:
        # Get Google API client for People API
        service = get_google_contacts_service()

        # Make request to People API to retrieve user's contacts
        results = service.people().connections().list(
            resourceName='people/me',
            personFields='names,emailAddresses'
        ).execute()

        # Extract name and email address from each contact
        contacts = []
        for person in results.get('connections', []):
            if 'emailAddresses' in person:
                name = person.get('names', [{}])[0].get('displayName', '')
                email = person['emailAddresses'][0].get('value', '')
                contacts.append({'name': name, 'email': email})

        # Display list of contacts
        return '<br>'.join([f"{c['name']}: {c['email']}" for c in contacts])
    except HttpError as error:
        return f"An error occurred: {error}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
