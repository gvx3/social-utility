from app.api import bp


@bp.route('/hello')
def hello_world():
    return "Hi"
