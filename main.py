from flask import Flask, request
from tests import msg_validator

app = Flask(__name__)
dict_of_names = {}


@app.route("/")
def start_page():
    return 'Welcome to smart shooting range!'


# getting messages by server from user
@app.route("/api/getSession", methods=['GET'])
def getmessage():
    msg = request.json
    flag = msg_validator(msg)
    if flag is True:
        recipient = msg.pop("Recipient")
        if recipient not in dict_of_names:
            dict_of_names[recipient] = [msg]
        else:
            dict_of_names[recipient].append(msg)
        return "Success! Received messages: 1.", 200
    else:
        return "Wrong format", 400


# sending messages to user from server
@app.route("/api/messenger/<username>")
def sendmessage(username):
    try:
        if len(dict_of_names[username]) > 0:
            messages = dict_of_names.get(username)
            answer = {username: messages}
            dict_of_names[username] = []
            return answer, 200
        elif len(dict_of_names[username]) == 0:
            return "Not found", 200
    except KeyError:
        return "Not found user", 400


if __name__ == '__main__':
    app.run()
