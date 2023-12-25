import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import utils


server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)


fs = gridfs.GridFS(mongo.db)


connections = pika.BlockingConnection(
    pika.ConnectionParameters("rabbitmq")
)  # hpc block and non-block MPI

channel = connections.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def valid():
    access, err = validate.token(request)
    if err:
        return err
    print(type(access))
    access = json.loads(access)
    print(type(access))
    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exceeds the Number of files!Only 1 allowed", 400

        for _, f in request.files.items():
            err = utils.upload(f, fs, channel, access)

            if err:
                return err
        return "Done", 200
    else:
        return "Not authorized", 401


@server.route("/download", methods=["GET"])
def down():
    ...


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
