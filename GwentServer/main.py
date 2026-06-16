from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

import validation
from validation import create_error

app = Flask(__name__)
CORS(app)

games = {}

@app.route('/create_game', methods=['POST'])
def create_game():
    room_id = str(uuid.uuid4())[:4].upper()
    app.logger.info(f"Creating new game room: {room_id}")
    games[room_id] = {"players": [], "state":{}}
    app.logger.info(f"Created game room: {room_id}")
    return {"room_id": room_id}


@app.route('/delete_game', methods=['DELETE'])
def delete_game():
    app.logger.info(f"Attempting to delete game room...")
    isValid, data, code = validation.deserialize_request_payload(app, request, ["room_id"])
    if not isValid:
        app.logger.info(f"Invalid input for deletion.")
        return jsonify(data), code
    room_id = data["room_id"]

    app.logger.info(f"Deleting game room: {room_id}")
    deleting_game = games.pop(room_id, None)
    if not deleting_game:
        app.logger.info(f"Could not delete game room: {room_id}")
        return create_error("DeletionError", f"Could not delete game room: {room_id}"), 404

    app.logger.info(f"Deleted game room: {room_id}")
    return jsonify({"Deleted room": room_id}), 200


@app.route('/join_game', methods=['POST'])
def join_game():
    app.logger.info(f"Attempting to join game room...")
    isValid, data, code = validation.deserialize_request_payload(app, request, ["room_id", "player_name"])

    if not isValid:
        app.logger.info(f"Invalid input to join a game.")
        return jsonify(data), code

    player_name = data["player_name"]
    room_id = data["room_id"]

    app.logger.info(f"Adding {player_name} to room {room_id}")
    currentGame = games.get(room_id, None)
    if currentGame is None:
        return create_error("JoinError", f"Invalid game ID - {room_id}"), 400
    if len(currentGame["players"])>1:
        return create_error("JoinError", f"Room {room_id} is full"), 400
    if player_name in currentGame["players"]:
        return create_error("JoinError", f"{player_name} already in game {room_id}"), 400
    currentGame["players"].append(player_name)

    return jsonify({"Players": currentGame["players"]}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
