from flask import Flask, request, jsonify
from flask_cors import CORS
from TechnicalToolsV2 import log, sha256
from time import time
import secrets
import sqlite3

DATABASE_NAME = "users.db"
SESSION_DURATION = 1000000  # Seconds
app = Flask(__name__)
CORS(app)


def connect():
    log("Connecting to database")
    connection = sqlite3.connect(DATABASE_NAME)
    return connection, connection.cursor()


def disconnect(connection, cursor):
    log("Disconnecting from database")
    connection.commit()
    cursor.close()
    connection.close()


def generate_session_cookie():
    return f"{secrets.token_hex(16)}__{int(time())}"


def signup_into_database(name, email, password):
    connection, cursor = connect()
    hashed_password = password

    cursor.execute(
        "INSERT INTO Users (name, email, password_hash) VALUES (?,?,?);",
        (name, email, hashed_password)
    )

    disconnect(connection, cursor)


def check_value_in_column_exists(value, column_name):
    connection, cursor = connect()
    cursor.execute(f"SELECT EXISTS(SELECT 1 FROM Users WHERE {column_name} = ?) ", (value,))
    exists = cursor.fetchone()[0]
    disconnect(connection, cursor)
    return exists == 1


@app.route('/api/signup', methods=['POST'])
def api_signup_handler():
    data = request.json
    log("Received signup data:", logtitle="POST REQUEST", var=data, color='yellow')

    signup_into_database(data['name'], data['email'], data['password'])

    return jsonify({"message": "Recieved Info!"})


@app.route('/api/login', methods=['POST'])
def api_login_handler():
    data = request.json
    log("Received login data:", logtitle="POST REQUEST", var=data, color='yellow')

    if check_value_in_column_exists(data["email"], "email"):
        connection, cursor = connect()
        cursor.execute(f"SELECT id,password_hash FROM Users WHERE email = ? ", (data["email"],))
        user_id, password = cursor.fetchone()
        disconnect(connection, cursor)
        if password == data["password"]:
            session_cookie = generate_session_cookie()

            connection, cursor = connect()
            cursor.execute(f"INSERT INTO Sessions (user_id,token,start_time,duration) VALUES (?,?,?,?)",
                           (user_id, session_cookie, int(time()), SESSION_DURATION))
            disconnect(connection, cursor)
            log("Created cookie : ", var=session_cookie, color="green", logtitle="COOKIE MONSTER")
            return jsonify({"success": True, "sessionCookie": session_cookie, "duration": SESSION_DURATION})

    return jsonify({"success": False, "sessionCookie": None})


@app.route('/api/checkEmail', methods=['POST'])
def api_check_same_email():
    data = request.json
    log("Received check email data:", logtitle="POST REQUEST", var=data, color='yellow')
    return jsonify({"value": check_value_in_column_exists(data["email"], "email")})


@app.route('/api/getAccountInfo', methods=['POST'])
def api_get_account_info():
    data = request.json
    log("Requesting account info : ", logtitle="POST REQUEST", var=data, color='yellow')
    # Check if session cookie exists
    try:
        data["session_cookie"]
    except KeyError:
        return jsonify({"id": None, "name": None, "email": None})

    # Getting account info
    connection, cursor = connect()
    cursor.execute("SELECT id,name,email FROM Users WHERE id = (SELECT user_id FROM Sessions WHERE token = ?)",
                   (data["session_cookie"],))
    info = cursor.fetchone()
    if info:
        user_id, name, email = info
        disconnect(connection, cursor)
        return jsonify({"id": user_id, "name": name, "email": email})
    else:
        log("Can't find cookie", logtitle="error", color="red")
        return jsonify({"id": None, "name": None, "email": None})


@app.route('/api/uploadFile', methods=['POST'])
def api_upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    # Save the uploaded file to a designated location
    file.save('/home/sirat/Code/WebBackend/uploads/' + file.filename)

    return 'File uploaded successfully', 200


@app.route('/')
def hello():
    return "<b>Just checking if the backend works or not lol nice port number am I right :)</b>"


if __name__ == '__main__':
    app.run(debug=True,port=6969)
