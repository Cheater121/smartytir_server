from flask import Flask, request
from tests import msg_validator

app = Flask(__name__)
dict_of_sessions = {}


@app.route("/")
def start_page():
    return 'Welcome to smart shooting range!'


@app.route("/status")
def status():
    return dict_of_sessions


@app.route("/api/push/", methods=['POST'])
def save_data():
    schema = request.json
    flag = msg_validator(schema)
    if flag is True:
        session = schema.pop("Session")
        if session not in dict_of_sessions:
            dict_of_sessions[session] = [schema]
        else:
            dict_of_sessions[session].append(schema)
        return "Success!", 200
    else:
        return "Wrong format", 400


@app.route("/api/getSession/<int:session>")
def getsession(session):
    try:
        if len(dict_of_sessions[session]) > 0:
            info = dict_of_sessions.get(session)
            answer = {session: info}
            return answer, 200
        elif len(dict_of_sessions[session]) == 0:
            return "Not found", 200
    except KeyError:
        return "Not found user", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0')
