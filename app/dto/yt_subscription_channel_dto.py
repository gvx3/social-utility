from marshmallow import Schema, fields, post_load, pre_load

from app.models import SubscriptionChannel


class SubscriptionChannelSnippetSchema(Schema):
    class Meta:
        ordered = True

    title = fields.Str(required=True)
    description = fields.Str()
    published_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S%z', data_key="publishedAt")
    resource_kind = fields.Str()
    resource_channel_id = fields.Str(required=True)
    snippet_channel_id = fields.Str(required=True)
    thumbnails_default_url = fields.Str()
    thumbnails_medium_url = fields.Str()
    thumbnails_high_url = fields.Str()


class SubscriptionChannelSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    subscription_etag = fields.Str(required=True, data_key="etag")
    subscription_id = fields.Str(required=True, data_key="id")
    snippet = fields.Nested(SubscriptionChannelSnippetSchema())
    total_item_count = fields.Int(data_key="totalItemCount")

    @pre_load()
    def get_total_item_count(self, data):
        content_details = data.pop('contentDetails')
        data['totalItemCount'] = content_details['totalItemCount']
        return data

    @post_load()
    def make_subscription_channel(self, data, **kwargs):
        return SubscriptionChannel(**data)





