import psycopg2
import psycopg2.extras
from flask import Flask, request
from tests import msg_validator
from secret_info import user, password

app = Flask(__name__)


@app.route("/")
def start_page():
    return 'Welcome to smart shooting range!'


@app.route("/api/pushGame", methods=['POST'])
def save_data():
    schema = request.json
    flag = msg_validator(schema)
    if flag is True:
        save_to_db(schema)
        return "Success!", 200 # ToDo: return error if save failed
    else:
        return "Wrong format", 400


@app.route("/api/getGamesId/<string:user_name>")
def get_games_id(user_name):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute('SELECT game_id FROM games WHERE user_name=(%s);', [user_name])
        games_ids = cur.fetchall()
        answer = {"user_name": user_name, "games_ids": games_ids}
    except:
        return "Bad request", 400
    cur.close()
    conn.close()
    return answer


@app.route("/api/getAllGames/<string:user_name>")
def get_all_games(user_name):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute('SELECT * FROM games WHERE game_id IN (SELECT game_id FROM games WHERE user_name=(%s));', [user_name])
        games = cur.fetchall()
        answer = {"user_name": user_name, "all_games": games}
    except:
        return "Bad request", 400
    cur.close()
    conn.close()
    return answer


@app.route("/api/getGameInfo/<int:game_id>")
def get_game_info(game_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        game_id = int(game_id)
        cur.execute('SELECT * FROM games WHERE game_id=(%s);', [game_id])
        games_id = cur.fetchall()
        answer = {"game_id": game_id, "game_info": games_id}
    except:
        return "Bad request", 400
    cur.close()
    conn.close()
    return answer


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db1',
                            user=user,
                            password=password)
    return conn


def save_user_to_db(user_name):
    conn = get_db_connection()
    cur = conn.cursor()
    try:  # need to think: maybe upgrade by SELECT (if not exists - save)
        cur.execute('INSERT INTO users (user_name)'
                    'VALUES (%s)',
                    [user_name])
        conn.commit()
    except:
        print("Error in saving user")
    finally:
        cur.close()
        conn.close()


def save_to_db(schema):
    conn = get_db_connection()
    cur = conn.cursor()
    for one_user in schema.get("users"):
        try:
            game_id = int(schema.get("game_id"))
            user_name = str(one_user.get("user_name"))
            shoots = int(one_user.get("shoots"))
            hits = int(one_user.get("hits"))
            save_user_to_db(user_name)
            cur.execute('INSERT INTO games (game_id, user_name, shoots, hits)'
                        'VALUES (%s, %s, %s, %s)',
                        (game_id, user_name, shoots, hits))
            conn.commit()
        except:
            print("Error in saving game") # could be upgrade
    cur.close()
    conn.close()


if __name__ == '__main__':
    app.run()
