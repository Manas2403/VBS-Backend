from google.oauth2 import id_token
from google.auth.transport import requests
import firebase_admin
from firebase_admin import credentials, auth


CLIENT_ID = "575828521972-m8fu4782d5k11fgo54gnntqsugpsbur2.apps.googleusercontent.com"

cred = credentials.Certificate("venue-booking-system-e6b2f-firebase-adminsdk-4s58y-8e2a3e3c1d.json")
firebase_admin.initialize_app(cred)


def verify_oauth_token(token):
    if token is None:
        return False, None
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        return True, id_info['email']
    except Exception:
        return False, None


def verify_id_token(token):
    if token is None:
        return False, None
    try:
        decoded_token = auth.verify_id_token(token)
        return True, decoded_token['email']
    except Exception:
        return False, None

