from flask import Flask, request, jsonify

app = Flask(__name__)

users = []


@app.route("/register", methods=["POST"])
def register():
    data = request.json

    user = {
        "username": data["username"],
        "interests": data["interests"],
        "lat": data.get("lat"),
        "lon": data.get("lon")
    }

    users.append(user)

    return jsonify({"message": "User added!"})


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

app.run(debug=True)