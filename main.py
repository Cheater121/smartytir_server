from flask import Flask, request
from tests import msg_validator

app = Flask(__name__)
dict_of_games = {}


@app.route("/")
def start_page():
    return 'Welcome to smart shooting range!'


@app.route("/status")
def status():
    return dict_of_games


@app.route("/api/pushGame", methods=['POST'])
def save_data():
    schema = request.json
    flag = msg_validator(schema)
    if flag is True:
        game = schema.pop("game_id")
        dict_of_games[game] = schema
        return "Success!", 200
    else:
        return "Wrong format", 400


@app.route("/api/getGamesId/<string:user>")
def get_games_id(user):
    # select * from games_db where user=user
    return "User games ids: array"


@app.route("/api/getAllGames/<string:user>")
def get_all_games(user):
    # need to think about db request
    return "games: array with all games, where user played"


@app.route("/api/getGameInfo/<int:game_id>")
def get_game_info(game_id):
    info = dict_of_games.get(game_id, "Not found")
    if info != "Not found":
        answer = {game_id: info}
        return answer, 200
    else:
        return info, 400


if __name__ == '__main__':
    app.run(host='0.0.0.0')
