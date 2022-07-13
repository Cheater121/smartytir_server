from jsonschema import validate


schema = {
	"type": "object",
	"minProperties": 5,
	"maxProperties": 5,
	"properties": {
		"Username": {
			"type": "string",
			"minLength": 1
			},
		"Timestamp": {
			"type": "string",
			"format": "date-time"
			},
		"Session": {
			"type": "number",
			"minLength": 1
			},
		"Shots": {
			"type": "number",
			"minLength": 1
			},
		"Hits": {
			"type": "number",
			"minLength": 1
			}
		}, 
	"required": ["Username", "Timestamp", "Session", "Shots", "Hits"]
	}


def msg_validator(msg):
	try:
		validate(msg, schema)
	except:
		return False
	else:
		return True