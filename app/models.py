from datetime import datetime
from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.now)
    subscription_channels = db.relationship('SubscriptionChannel', lazy='select', backref='categories')

    def set_category(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Category: {self.name}>'


class SubscriptionChannel(db.Model):
    __tablename__ = "subscription_channels"

    id = db.Column(db.Integer, primary_key=True)
    subscription_etag = db.Column(db.Text, nullable=False)
    subscription_id = db.Column(db.Text, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    published_at = db.Column(db.DateTime)
    resource_kind = db.Column(db.String(30))
    resource_channel_id = db.Column(db.String(30), unique=True, nullable=False)
    snippet_channel_id = db.Column(db.String(30), nullable=False)
    thumbnails_default_url = db.Column(db.Text)
    thumbnails_medium_url = db.Column(db.Text)
    thumbnails_high_url = db.Column(db.Text)
    total_item_count = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return f'''
            <SubscriptionChannel: Title: {self.title} 
            -- ID: {self.subscription_id}
            -- Description: {self.description[:20]}
            -- Etag: {self.subscription_etag}
            -- Published at: {self.published_at}
            -- ChannelId: {self.snippet_channel_id}
        >'''

    def get_subscription_id(self):
        return self.subscription_id

    def get_subscription_etag(self):
        return self.subscription_etag

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_resource_channel_id(self):
        return self.resource_channel_id

    def get_snippet_channel_id(self):
        return self.snippet_channel_id

    def get_thumbnails_default_url(self):
        return self.thumbnails_default_url

    def get_thumbnails_medium_url(self):
        return self.thumbnails_medium_url

    def get_thumbnails_high_url(self):
        return self.thumbnails_high_url

    def get_total_item_count(self):
        return self.total_item_count

    @staticmethod
    def to_dict(self):
        return {
            "subscription_etag": self.subscription_etag,
            "subscription_id": self.subscription_id,
            "title": self.title,
            "description": self.description,
            # "resource_kind": self.resource_kind,
            "resource_channel_id": self.resource_channel_id,
            "snippet_channel_id": self.snippet_channel_id,
            "thumbnails_default_url": self.thumbnails_default_url,
            "thumbnails_medium_url": self.thumbnails_medium_url,
            "thumbnails_high_url": self.thumbnails_high_url,
            "total_item_count": self.total_item_count
        }

