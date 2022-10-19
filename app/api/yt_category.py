from marshmallow import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.api import bp
from flask import request, jsonify

from app.dto.yt_category_dto import CategoryCreationSchema
from app.extensions import db
from app.models import Category

categorySchema = CategoryCreationSchema()
category = Category()


@bp.route('/category/<int:_id>', methods=['GET'])
def list_category(_id):
    stmt = select(Category).where(Category.id == _id)
    try:
        one_category = db.session.execute(stmt).scarlars().one()
    except NoResultFound as e:
        return jsonify({"message": f"{e}"}), 400

    result = categorySchema.dump(one_category)
    return jsonify(result)


@bp.route('/categories', methods=['GET'])
def list_categories():
    stmt = select(category)
    categories = db.session.execute(stmt).scarlars()
    result = categorySchema.dump(categories, many=True)
    return jsonify(result)


@bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        new_category = categorySchema.load(data)
        db.session.add(new_category)
        db.session.commit()
    except ValidationError as e:
        return jsonify(e.messages_dict), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": f"{e.orig}"}), 400

    result = categorySchema.dump(new_category)
    return jsonify(result)


@bp.route('/categories', methods=['PUT'])
def update_category():
    pass


@bp.route('/category/<int:_id>', methods=['DELETE'])
def delete_category():
    pass
