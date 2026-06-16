from flask import Flask, request, jsonify
import uuid


app = Flask(__name__)

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
    data = request.get_json(silent=True)
    if not data:
        app.logger.info(f"Malformed input provided.")
        return jsonify({"DeletionError": "Malformed input provided"}), 400

    data = dict(data)
    room_id = data.get("room_id", None)
    if not room_id:
        app.logger.info(f"No room id provided for deletion")
        return jsonify({"DeletionError": "Improper input provided"}), 400

    try:
        games.pop(room_id)
        return {"Deleted room": room_id}
    except KeyError:
        return jsonify({"DeletionError": f"Invalid game ID - {room_id}"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
