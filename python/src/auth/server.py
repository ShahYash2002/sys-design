import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)

mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if not auth:
        return "missing credentials", 401

    cur = mysql.connection.cursor()
    res = cur.execute("select email,password from user where email=%s", (auth.username))

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(email, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
            "admin": authz,
        },
        secret,
    )


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    jwt_token = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(jwt_token, os.environ.get("JWT_SECRET"))
        return decoded, 200
    except:
        return "not authorized", 403


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
