from marshmallow import ValidationError
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.api import bp
from flask import request

from app.dto.yt_category_dto import CategoryCreationSchema
from app.extensions import db
from app.messages import JsonResponse
from app.models import Category

categorySchema = CategoryCreationSchema()


@bp.route('/category/<int:_id>', methods=['GET'])
def list_category(_id):
    try:
        stmt = select(Category).where(Category.id == _id)
        one_category = db.session.execute(stmt).scalars().one()
    except NoResultFound as e:
        return JsonResponse.message(e), 404
    result = categorySchema.dump(one_category)
    return JsonResponse.message_json(result)


@bp.route('/categories', methods=['GET'])
def list_categories():
    stmt = select(Category)
    categories = db.session.execute(stmt).scalars()
    result = categorySchema.dump(categories, many=True)
    return JsonResponse.message_json(result)


@bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        new_category = categorySchema.load(data)
        db.session.add(new_category)
        db.session.commit()
    except ValidationError as e:
        return JsonResponse.message(e.messages), 400
    except IntegrityError as e:
        db.session.rollback()
        return JsonResponse.message(e.orig), 400

    result = categorySchema.dump(new_category)
    return JsonResponse.message_json(result)


@bp.route('/category/<int:_id>', methods=['PUT'])
def update_category(_id):
    data = request.get_json()
    try:
        update_object = categorySchema.load(data)
        stmt_update = update(Category) \
            .where(Category.id == _id) \
            .values(
            {
                Category.name: update_object.name,
                Category.description: update_object.description
            }
        )
        print(stmt_update)
        db.session.execute(stmt_update)
        db.session.commit()

        stmt = select(Category).where(Category.id == _id)
        # Exception at select statement
        current_category = db.session.execute(stmt).scalars().one()
        db.session.commit()
    except NoResultFound as e:
        return JsonResponse.message(e), 404
    except ValidationError as e:
        return JsonResponse.message(e.messages), 400

    result = categorySchema.dump(current_category)
    return JsonResponse.message_json(result)


@bp.route('/category/<int:_id>', methods=['DELETE'])
def delete_category(_id):
    stmt = delete(Category).where(Category.id == _id)
    delete_object = db.session.execute(stmt)
    db.session.commit()
    if delete_object.rowcount == 0:
        return JsonResponse.message("Not find anything to delete"), 404

    return JsonResponse.message("Deleted successfully")
