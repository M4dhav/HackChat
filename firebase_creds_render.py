import firebase_admin
from firebase_admin import credentials
import os
print(type(os.environ.get('project_id')))
if not firebase_admin._apps:
    cred = credentials.Certificate({\
        "type": "service_account",\
        "project_id": os.environ.get('project_id'),\
        "private_key_id": os.environ.get('private_key_id'),\
        "private_key": os.environ.get('private_key'),\
        "client_email": os.environ.get('client_email'),\
        "client_id": os.environ.get('client_id'),\
        "auth_uri": os.environ.get('auth_uri'),\
        "token_uri": os.environ.get('token_uri'),\
        "auth_provider_x509_cert_url": os.environ.get('auth_provider_x509_cert_url'),
        "client_x509_cert_url": os.environ.get('client_x509_cert_url'),\
        "universe_domain": "googleapis.com"})
    firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': os.environ.get('databaseURL')
                              })