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




