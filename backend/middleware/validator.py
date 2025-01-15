from flask import Response, json


def validate_request(request, required_fields):
    data = request.get_json()
    for field in required_fields:
        if field not in data:
            return False, None
    return True, data