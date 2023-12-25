import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL
# from dotenv import load_dotenv
server = Flask(__name__)
mysql = MySQL(server)
# load_dotenv()
# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))
# print(server.config["MYSQL_HOST"])


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )
    print(res)
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalide credentials", 401


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)

# import jwt
# import datetime, os
# import flask
# from flask import Flask, request
# from flask_mysqldb import MySQL

# server = Flask(__name__)

# mysql = MySQL(server)

# #! config
# server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
# server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
# server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
# server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
# server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


# @server.route("/login", methods=["POST", "GET"])
# def landing():
#     auth = (
#         request.authorization
#     )  # it is used with the basic authenticatio it has password and whatnot so we are accessing the data
#     if not auth:
#         return "Missing credentials", 401

#     # check the db if the user and password is right
#     cur = mysql.connection.cursor()
#     res = cur.execute(f"SELECT email,password from user where email={auth.username}")
#     if res > 0:
#         user_row = cur.fetchone()
#         email = user_row[0]
#         password = user_row[1]

#         if (auth.username != email) or (auth.password != password):
#             return "Invalid credentials", 401
#         else:
#             return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
#     else:
#         return "Invalid access and/or credentials", 401


# @server.route("/validate", methods=["POST", "GET"])
# def validate():
#     encoded_jwt = request.headers["Authorization"]
#     if not encoded_jwt:
#         return "No authorization", 401

#     # split the token Bearer XXXX into XXXX and barer seperate
#     encoded_jwt = encoded_jwt.split(" ")[1]

#     try:
#         decoded = jwt.decode(
#             encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HSA256"]
#         )
#     except Exception:
#         return "Not authorized", 403

#     return decoded, 200


# def createJWT(username, secrets, authz):
#     return jwt.encode(
#         {
#             "username": username,
#             "exp": datetime.datetime.now(tz=datetime.timezone.utc)
#             + datetime.timedelta(days=1),  # exp after a day
#             # issued at
#             "iat": datetime.datetime.utcnow(),
#             "admin": authz,
#         },
#         secrets,
#         algorithm="HS256",
#     )


# if __name__ == "__main__":
#     # 0.0.0.0 is letting it have all public ips
#     server.run(port=5000, host="0.0.0.0")