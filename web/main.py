import hashlib
import json
import os
import secrets
import config_manager as cfg
import logger
import storage

from flask import Flask, request, jsonify
from flask_cors import CORS
from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher
from cheroot.ssl.builtin import BuiltinSSLAdapter

app = Flask(__name__)
CORS(app)

CHARS = "abcdefghiklmnopqrstuvwxyz" + "abcdefghiklmnopqrstuvwxyz".upper() + "123456789" + "!@#$%^&*()"


def gen_rand_seq(length: int):
    return "".join([secrets.choice(CHARS) for _ in range(length)])


@app.route("/authenticate", methods=["POST"])
async def authenticate():
    args = json.loads(request.data)
    if list(args.keys()) != ["username", "password"]:
        return jsonify({
            "code": 400,
            "message": "Bad request. Authenticate requests must and only contain username and password key."
        })
    salt = storage.get_dtb().child("saltdb").child(args["username"]).get().val()
    if salt is None:
        response = jsonify({"code": 400, "message": "Unregistered user."})
    else:
        token = hashlib.sha256(
            (args["username"] + args["password"] + "NeverGonnaLetYouDown" + salt).encode("utf8")
        ).hexdigest()
        stored_token = storage.get_dtb().child("hashdb").child(args["username"]).get().val()
        valid = token == stored_token
        response = jsonify({"valid": valid, "token": token})
    return response


@app.route("/authenticate", methods=["PUT"])
async def register():
    args = request.json
    if list(args.keys()) != ["username", "password"]:
        return jsonify({"code": 400, "message": "Bad request. Register Requests must and only contain username key."})
    salt = gen_rand_seq(10)
    storage.get_dtb().child("saltdb").child(args["username"]).set(salt)
    token = hashlib.sha256(
        (args["username"] + args["password"] + "NeverGonnaLetYouDown" + salt).encode("utf8")
    ).hexdigest()
    storage.get_dtb().child("hashdb").child(args["username"]).set(token)
    response = jsonify({"code": 200, "message": "Entry created successfully."})
    return response


def ensure_ssl():
    with open("web/fullchain.pem", "w") as c:
        c.write(cfg.get("crypt.fullChain"))
    with open("web/privkey.pem", "w") as k:
        k.write(cfg.get("crypt.privateKey"))


if __name__ == "__main__":
    ensure_ssl()
    d = PathInfoDispatcher({'/': app})
    logger.info(f"Binding to port {os.environ['PORT']}")
    server = WSGIServer(("localhost", int(os.environ["PORT"])), d)
    server.ssl_adapter = BuiltinSSLAdapter("web/fullchain.pem", "web/privkey.pem", None)
    logger.info("web directory listing:" + str(os.listdir("web")))
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
