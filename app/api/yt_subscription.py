import json

from flask import redirect, session, url_for, jsonify, request
import google_auth_oauthlib.flow
import googleapiclient.discovery
from marshmallow import ValidationError
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound

from app.messages import JsonResponse
from app.extensions import db
from app.dto.yt_subscription_channel_dto import SubscriptionChannelFetchSchema, SubscriptionChannelUpdateCategorySchema, SubscriptionChannelSchema
from app.models import SubscriptionChannel, Category
from config import Config
from app.api import bp
import google.oauth2.credentials
from pprint import pprint

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRET_FILE = Config.CLIENT_CREDENTIAL
subscriptionChannelSchema = SubscriptionChannelSchema()
subscriptionChannelFetchSchema = SubscriptionChannelFetchSchema()
subscriptionChannelUpdateCategorySchema = SubscriptionChannelUpdateCategorySchema()


@bp.route('/fetch_subscriptions')  # Only fetch records from ytube
def fetch_subscriptions():
    if 'credentials' not in session:
        return redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    extra_parameters = {"part": "snippet, contentDetails", "maxResults": 50, "mine": True, "pageToken": ""}
    list_data = []
    while True:
        print("=======Call Youtube API=======")
        yt_request = youtube.subscriptions().list(
            part=extra_parameters['part'],
            maxResults=extra_parameters['maxResults'],
            mine=extra_parameters['mine'],
            pageToken=extra_parameters['pageToken']
        ).execute()

        list_data.append(yt_request)
        if "nextPageToken" in yt_request:
            next_page_token = yt_request['nextPageToken']
            extra_parameters['pageToken'] = next_page_token
        else:
            break

    # print("=======Write to json file=======")
    # # append file mode
    # with open(Config.YT_DATA, 'a') as f:
    #     for yt_page in list_data:
    #         json_object = json.dumps(yt_page, indent=4)
    #         f.write(json_object)
    # print("=======Done writing to json file=======")

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    session['credentials'] = credentials_to_dict(credentials)

    return jsonify(**yt_request)


@bp.route('/fetch_subscriptions_save')  # Fetch and save to DB
def fetch_subscriptions_test():
    if 'credentials' not in session:
        return redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    extra_parameters = {"part": "snippet, contentDetails", "maxResults": 50, "mine": True, "pageToken": ""}
    list_data = []
    while True:
        print("=======Call Youtube API=======")
        yt_request = youtube.subscriptions().list(
            part=extra_parameters['part'],
            maxResults=extra_parameters['maxResults'],
            mine=extra_parameters['mine'],
            pageToken=extra_parameters['pageToken']
        ).execute()

        list_data.append(yt_request)
        if "nextPageToken" in yt_request:
            next_page_token = yt_request['nextPageToken']
            extra_parameters['pageToken'] = next_page_token
        else:
            break

    stmt = select(SubscriptionChannel)
    subscription_channels = db.session.execute(stmt).scalars()
    db_result = subscriptionChannelSchema.dump(subscription_channels, many=True)
    db_result_compare_dict = {}

    # Add results to a dictionary
    for db_item in db_result:
        db_item.pop('id')  # Remove unnecessary fields to compare and update
        db_item.pop('category_id')
        db_item.pop('published_at')
        db_item.pop('resource_kind')
        db_result_compare_dict[db_item['subscription_id']] = db_item

    for yt_page in list_data:
        for item in yt_page['items']:
            try:
                channel = subscriptionChannelFetchSchema.load(item, many=False)
                subscription_id = channel.get_subscription_id()
                if subscription_id in db_result_compare_dict:
                    # Compare dict DB vs dict Channel object
                    if db_result_compare_dict[subscription_id] == SubscriptionChannel.to_dict(channel):
                        # Dict equals, no change needed to update to DB
                        pass
                    else:
                        stmt_update = update(SubscriptionChannel) \
                            .where(SubscriptionChannel.subscription_id == subscription_id) \
                            .values(
                            {
                                SubscriptionChannel.subscription_etag: channel.get_subscription_etag(),
                                SubscriptionChannel.title: channel.get_title(),
                                SubscriptionChannel.description: channel.get_description(),
                                SubscriptionChannel.resource_channel_id: channel.get_resource_channel_id(),
                                SubscriptionChannel.snippet_channel_id: channel.get_snippet_channel_id(),
                                SubscriptionChannel.thumbnails_default_url: channel.get_thumbnails_default_url(),
                                SubscriptionChannel.thumbnails_medium_url: channel.get_thumbnails_medium_url(),
                                SubscriptionChannel.thumbnails_high_url: channel.get_thumbnails_high_url(),
                                SubscriptionChannel.total_item_count: channel.get_total_item_count()
                            }
                        )
                        db.session.execute(stmt_update)
                else:
                    db.session.add(channel)
                    print("New records found, add to DB")
            except ValidationError as e:
                db.session.rollback()
                return JsonResponse.message(e), 400

    db.session.commit()

    yt_result_compare_dict = {}
    for yt_page in list_data:
        for item in yt_page['items']:
            yt_result_compare_dict[item['subscription_id']] = item
    # Delete records no longer in YT subscription from DB
    for sub_id in db_result_compare_dict.keys():
        if sub_id not in yt_result_compare_dict:
            stmt = delete(SubscriptionChannel).where(SubscriptionChannel.subscription_id == sub_id)
            db.session.execute(stmt)
        else:
            pass

    db.session.commit()

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    session['credentials'] = credentials_to_dict(credentials)

    return jsonify(**yt_request)


@bp.route('/list_subscription/<int:_id>', methods=['GET'])
def list_subscription(_id):
    try:
        stmt = select(SubscriptionChannel).where(SubscriptionChannel.id == _id)
        one_subscription = db.session.execute(stmt).scalars().one()
    except NoResultFound as e:
        return JsonResponse.message(e), 404
    result = subscriptionChannelSchema.dump(one_subscription)
    return JsonResponse.message_json(result)


@bp.route('/list_subscriptions', methods=['GET'])
def list_subscriptions():
    stmt = select(SubscriptionChannel)
    subscription_channel = db.session.execute(stmt).scalars()
    result = subscriptionChannelSchema.dump(subscription_channel, many=True)
    return JsonResponse.message_json(result)


@bp.route('/update_category_subscription/<int:_id>', methods=['PUT'])
def update_category_subscription(_id):
    data = request.get_json()
    try:
        stmt = select(SubscriptionChannel).where(SubscriptionChannel.id == _id)
        current_channel = db.session.execute(stmt).scalars().one()
    except NoResultFound as e:
        return JsonResponse.message("SubscriptionChannel not found"), 404
    except ValidationError as e:
        return JsonResponse.message(e.messages), 400

    try:
        stmt_category = select(Category).where(Category.id == data['category_id'])
        db.session.execute(stmt_category).scalars().one()

        update_object = subscriptionChannelUpdateCategorySchema.load(data)
        stmt_update = update(SubscriptionChannel) \
            .where(SubscriptionChannel.id == _id) \
            .values({
                SubscriptionChannel.category_id: update_object.category_id
            })
    except NoResultFound as e:
        return JsonResponse.message("Category not found"), 404
    except ValidationError as e:
        return JsonResponse.message(e.messages), 400
    except KeyError as e:
        return JsonResponse.message(f"Attribute does not exist. Do you mean {e}"), 422

    db.session.execute(stmt_update)
    db.session.commit()

    result = subscriptionChannelSchema.dump(current_channel)
    return JsonResponse.message_json(result)


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

    return redirect(url_for('api.fetch_subscriptions'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
