from flask import jsonify


class JsonResponse:
    @classmethod
    def message(cls, msg):
        return jsonify({"message": f"{msg}"})

    @classmethod
    def message_json(cls, msg=dict):
        return jsonify(msg)
