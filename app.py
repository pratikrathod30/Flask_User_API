from flask import Flask, request, jsonify

app = Flask(__name__)

users = []
next_id = 1


@app.route("/")
def home():
    return "User API is running"


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200



@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404



@app.route("/users", methods=["POST"])
def create_user():
    global next_id
    data = request.json

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "name & email are required"}), 400

    user = {
        "id": next_id,
        "name": data["name"],
        "email": data["email"]
    }

    users.append(user)
    next_id += 1

    return jsonify(user), 201



@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json

    for user in users:
        if user["id"] == user_id:
            user["name"] = data.get("name", user["name"])
            user["email"] = data.get("email", user["email"])
            return jsonify(user), 200

    return jsonify({"error": "User not found"}), 404



@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    for index, user in enumerate(users):
        if user["id"] == user_id:
            users.pop(index)
            return jsonify({"message": "User deleted"}), 200

    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
