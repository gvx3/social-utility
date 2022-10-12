import os

import flask
import google_auth_oauthlib.flow
import googleapiclient.discovery
from config import Config
from app.api import bp
import google.oauth2.credentials


SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRET_FILE = Config.CLIENT_CREDENTIAL


@bp.route('/')
def index():
    return print_index_table()


@bp.route('/test')
def test_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

        # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=CLIENT_SECRET_FILE)
    request = youtube.subscriptions().list().execute()

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**request)


@bp.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES)
    flask.url_for()

@bp.route('/hello')
def hello_world():
    # yt_url_subscriptions = "https://www.googleapis.com/youtube/v3/subscriptions"
    # yt_url_channels = "https://www.googleapis.com/youtube/v3/channels"

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES)
    if os.path.exists(CLIENT_SECRET_FILE):
        print(f'Path to client_secret json file: {CLIENT_SECRET_FILE}')

    flow.redirect_uri('http://127.0.0.1:5000/api/blank')

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scope='true'
    )

    youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=CLIENT_SECRET_FILE)
    request = youtube.subscriptions().list().execute()
    print(request)


@bp.route('/blank')
def blank_response():
    return 'Redirected'


def print_index_table():
    return ('<table>' +
              '<tr><td><a href="/test">Test an API request</a></td>' +
              '<td>Submit an API request and see a formatted JSON response. ' +
              '    Go through the authorization flow if there are no stored ' +
              '    credentials for the user.</td></tr>' +
              '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
              '<td>Go directly to the authorization flow. If there are stored ' +
              '    credentials, you still might not be prompted to reauthorize ' +
              '    the application.</td></tr>' +
              '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
              '<td>Revoke the access token associated with the current user ' +
              '    session. After revoking credentials, if you go to the test ' +
              '    page, you should see an <code>invalid_grant</code> error.' +
              '</td></tr>' +
              '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
              '<td>Clear the access token currently stored in the user session. ' +
              '    After clearing the token, if you <a href="/test">test the ' +
              '    API request</a> again, you should go back to the auth flow.' +
              '</td></tr></table>')


def credentials_to_dict(credentials):
    return {'token': credentials.token,
              'refresh_token': credentials.refresh_token,
              'token_uri': credentials.token_uri,
              'client_id': credentials.client_id,
              'client_secret': credentials.client_secret,
              'scopes': credentials.scopes}
