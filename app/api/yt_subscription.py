import json

from flask import redirect, session, url_for, jsonify, request
import google_auth_oauthlib.flow
import googleapiclient.discovery
from config import Config
from app.api import bp
import google.oauth2.credentials


SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRET_FILE = Config.CLIENT_CREDENTIAL


@bp.route('/list_subscriptions')
def list_subscriptions():
    if 'credentials' not in session:
        return redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    extra_parameters = {"part": "snippet, contentDetails", "maxResults": 50, "mine": True, "pageToken": "CPoBEAA"}
    yt_request = youtube.subscriptions().list(
        part=extra_parameters['part'],
        maxResults=extra_parameters['maxResults'],
        mine=extra_parameters['mine'],
        pageToken=extra_parameters['pageToken']
    ).execute()

    # while True:
    #     yt_request = youtube.subscriptions().list(
    #         part=extra_parameters['part'],
    #         maxResults=extra_parameters['maxResults'],
    #         mine=extra_parameters['mine'],
    #         pageToken=extra_parameters['pageToken']
    #     ).execute()
    #
    #     with open(Config.YT_DATA, 'w') as f:
    #         json.dump(yt_request, f)
    #
    #     next_page_token = yt_request['nextPageToken']
    #     if next_page_token != "":
    #         print(f"======{next_page_token}======")
    #         extra_parameters['pageToken'] = next_page_token
    #     else:
    #         break

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    session['credentials'] = credentials_to_dict(credentials)

    return jsonify(**yt_request)


@bp.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES)
    # Redirect to /oauth2callback endpoint
    flow.redirect_uri = url_for('api.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scope='true'
    )

    session['state'] = state

    return redirect(authorization_url)


@bp.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('api.oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('api.list_subscriptions'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
              'refresh_token': credentials.refresh_token,
              'token_uri': credentials.token_uri,
              'client_id': credentials.client_id,
              'client_secret': credentials.client_secret,
              'scopes': credentials.scopes}
