import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///labels.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google API credentials
    GOOGLE_CLIENT_ID = '246245084452-u6g6040ajj1cabipleh83o6pn04vccm5.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    GOOGLE_REDIRECT_URI = "http://localhost:5000/google/callback"
