from flask import Flask, jsonify, request, make_response
import jwt
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


def initialize_database():
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jwks (
            kid TEXT PRIMARY KEY,
            key TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/.well-known/jwks.json', methods=['GET'])
def get_jwks():
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()
    cursor.execute("SELECT kid, key FROM jwks")
    rows = cursor.fetchall()
    conn.close()
    keys = [{"kid": row[0], "kty": "RSA", "alg": "RS256", "use": "sig", "n": row[1]} for row in rows]
    return jsonify({"keys": keys})


@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "valid_user" and password == "valid_pass":
        token = jwt.encode({
            "sub": username,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=5)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token": token})
    else:
        return make_response(jsonify({"error": "Invalid credentials"}), 401)


if __name__ == '__main__':
    initialize_database()
    app.run(host="0.0.0.0", port=8080)
