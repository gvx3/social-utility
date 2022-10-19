from marshmallow import Schema, fields, post_load, validates, ValidationError

from app.models import Category


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()

    @post_load()
    def make_category(self, data, **kwargs):
        return Category(**data)

    @validates("name")
    def validate_name(self, value):
        if len(value) > 50:
            raise ValidationError("Name must be within 50 characters")
        if value == "":
            raise ValidationError("Name must not be blank")


