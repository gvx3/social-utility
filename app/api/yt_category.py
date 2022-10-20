from marshmallow import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.api import bp
from flask import request, jsonify

from app.dto.yt_category_dto import CategoryCreationSchema
from app.extensions import db
from app.models import Category

categorySchema = CategoryCreationSchema()


@bp.route('/category/<int:_id>', methods=['GET'])
def list_category(_id):
    try:
        stmt = select(Category).where(Category.id == _id)
        one_category = db.session.execute(stmt).scalars().one()
    except NoResultFound as e:
        return jsonify({"message": f"{e}"}), 400

    result = categorySchema.dump(one_category)
    return jsonify(result)


@bp.route('/categories', methods=['GET'])
def list_categories():
    stmt = select(Category)
    categories = db.session.execute(stmt).scalars()
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


@bp.route('/category/<int:_id>', methods=['PUT'])
def update_category(_id):
    data = request.get_json()
    try:
        stmt = select(Category).where(Category.id == _id)
        current_category = db.session.execute(stmt).scalars().one()
        update_object = categorySchema.load(data)
        current_category.set_category(update_object.name, update_object.description)
        db.session.commit()
    except NoResultFound as e:
        return jsonify({"message": f"{e}"}), 400
    except ValidationError as e:
        return jsonify(e.messages_dict), 400

    result = categorySchema.dump(current_category)
    return jsonify(result)


@bp.route('/category/<int:_id>', methods=['DELETE'])
def delete_category(_id):
    pass
