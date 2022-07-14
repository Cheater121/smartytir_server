from jsonschema import validate

schema = {
    "type": "object",
    "minProperties": 2,
    "maxProperties": 2,
    "uniqueItems": True,
    "properties": {
        "game_id": {
            "type": "integer",
            "minLength": 1
        },
        "users": {
            "type": "array",
            "minItems": 1,
            "maxItems": 4,
            "items": {
                    "type": "object",
                    "minProperties": 3,
                    "maxProperties": 3,
                    "uniqueItems": True,
                    "properties": {
                        "user": {
                            "type": "string",
                            "minLength": 1
                        },
                        "shoots": {
                            "type": "integer",
                            "minLength": 1
                        },
                        "hits": {
                            "type": "integer",
                            "minLength": 1
                        }
                    },
                    "required": [
                        "user",
                        "shoots",
                        "hits"]
                }
        }
    },
    "required": [
        "game_id",
        "users"]
}


def msg_validator(msg):
    try:
        validate(msg, schema)
    except:
        return False
    else:
        return True
