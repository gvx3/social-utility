from marshmallow import Schema, fields, post_load, pre_load, EXCLUDE

from app.models import SubscriptionChannel


class SubscriptionChannelSchema(Schema):
    class Meta:
        ordered = True
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    subscription_etag = fields.Str(required=True, data_key="subscription_etag")
    subscription_id = fields.Str(required=True, data_key="subscription_id")
    title = fields.Str(required=True, data_key="title")
    description = fields.Str(data_key="description")
    published_at = fields.DateTime(data_key="publishedAt")
    resource_kind = fields.Str(data_key="resource_kind")
    resource_channel_id = fields.Str(required=True, data_key="resource_channel_id")
    snippet_channel_id = fields.Str(required=True, data_key="channelId")
    thumbnails_default_url = fields.Str(data_key="thumbnails_default_url")
    thumbnails_medium_url = fields.Str(data_key="thumbnails_medium_url")
    thumbnails_high_url = fields.Str(data_key="thumbnails_high_url")

    total_item_count = fields.Int(data_key="total_item_count")

    @pre_load()
    def get_subscription_channel(self, data, **kwargs):
        content_details = data.pop('contentDetails')
        data['total_item_count'] = content_details['totalItemCount']
        data['subscription_id'] = data.pop('id')
        data["subscription_kind"] = data.pop("kind")
        data['subscription_etag'] = data.pop('etag')

        snippet = data.pop('snippet')
        data['title'] = snippet['title']
        data['description'] = snippet['description']
        data['publishedAt'] = snippet['publishedAt']
        data['channelId'] = snippet['channelId']

        resource_id = snippet.pop('resourceId')
        data['resource_kind'] = resource_id['kind']
        data['resource_channel_id'] = resource_id['channelId']

        thumbnails = snippet.pop('thumbnails')
        data['thumbnails_default_url'] = thumbnails['default']['url']
        data['thumbnails_medium_url'] = thumbnails['medium']['url']
        data['thumbnails_high_url'] = thumbnails['high']['url']

        return data

    @post_load()
    def make_subscription_channel(self, data, **kwargs):
        return SubscriptionChannel(**data)





