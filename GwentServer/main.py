from typing import Dict

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send

import validation
from Models.Game.Game import Game
from Models.Game.Player import Player
from Models.Requests.GameInfoRequest import GameInfoRequest
from Models.Requests.JoinRequest import JoinRequest

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

games: Dict[str, Game] = {}

@app.route('/create_game', methods=['POST'])
def create_game():
    # room_id = str(uuid.uuid4())[:4].upper()
    room_id = "1234"
    app.logger.info(f"Creating new game room: {room_id}")
    games[room_id] = Game()
    app.logger.info(f"Created game room: {room_id}")
    return {"room_id": room_id}


@app.route('/delete_game', methods=['DELETE'])
def delete_game():
    app.logger.info(f"Attempting to delete game room...")
    isValid, delete_request_payload, code = validation.deserialize_request_payload(app, request, GameInfoRequest)
    if not isValid:
        app.logger.info(f"Invalid input for deletion.")
        return jsonify(delete_request_payload), code
    room_id = delete_request_payload["room_id"]

    app.logger.info(f"Deleting game room: {room_id}")
    deleting_game = games.pop(room_id, None)
    if not deleting_game:
        app.logger.info(f"Could not delete game room: {room_id}")
        return validation.create_error("DeletionError", f"Could not delete game room: {room_id}"), 404

    app.logger.info(f"Deleted game room: {room_id}")
    return jsonify({"Deleted room": room_id}), 200


@app.route('/players', methods=['GET'])
def get_players():
    app.logger.info(f"Looking for room")
    room_id = request.args.get('room_id')
    if not room_id:
        return validation.create_error("SearchError", f"No room_id provided"), 404

    app.logger.info(f"Reading game room: {room_id}")
    current_game = games.get(room_id, None)
    if not current_game:
        app.logger.info(f"Could not find game room: {room_id}")
        return validation.create_error("SearchError", f"Could not find game room: {room_id}"), 404

    app.logger.info(f"Found game room: {room_id}")
    current_player_names = [player.player_name for player in current_game.players]
    return jsonify({"players": current_player_names}), 200


@socketio.on('join_game')
def handle_join(join_payload):
    isValid, join_request_payload, code = validation.deserialize_dictionary(app, join_payload, JoinRequest)
    if not isValid:
        app.logger.info(f"Invalid input for join.")
        emit("JoinError", {"ErrorMessage": f"Invalid input provided - {join_request_payload}"})
        return

    join_request = JoinRequest(**join_payload)

    app.logger.info(f"Finding room: {join_request.room_id}")
    current_game = games.get(join_request.room_id)
    if current_game is None:
        emit("JoinError", {"ErrorMessage": f"Invalid game ID - {join_request.room_id}"})
        return
    if len(current_game.players) > 1:
        emit("JoinError", {"ErrorMessage": f"Room {join_request.room_id} is full"})
        return
    if any(p.player_name == join_request.player_name for p in current_game.players):
        emit("JoinError", {"ErrorMessage": f"{join_request.player_name} already in game {join_request.room_id}"})
        return

    app.logger.info(f"Adding {join_request.player_name} to room: {join_request.room_id}")
    newPlayer = Player(player_name=join_request.player_name, player_id=join_request.player_id)
    current_game.players.append(newPlayer)
    games[join_request.room_id] = current_game
    current_player_names = [player.player_name for player in current_game.players]
    response = {"players": current_player_names}
    emit("player_joined_game", response, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
