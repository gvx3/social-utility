from datetime import datetime
from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.now)

    def set_category(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Category: {self.name}>'

