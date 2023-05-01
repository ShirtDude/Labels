from flask import Flask, redirect, url_for, request, render_template, session
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
import google.auth.transport.requests
import googleapiclient.discovery
import googleapiclient.errors
from secrets import get_secret

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def get_secret(key):
    secret = get_secret(key)
    if "error" in secret:
        raise ValueError(secret["error"])
    return secret["api_key"]

# The rest of the code remains the same
