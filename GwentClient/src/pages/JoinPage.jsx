import { useState, useEffect } from "react";
import { io } from "socket.io-client";

const socket = io(import.meta.env.VITE_SERVER_URL);

function JoinPage() {
  // State variables
  const [playerID, setPlayerID] = useState(null);
  const [playerName, setPlayerName] = useState(null);
  const [roomCode, setRoomCode] = useState(null);
  const [players, setPlayers] = useState([]);
  const serverURL = import.meta.env.VITE_SERVER_URL
  const [playerJoinedGame, setPlayerJoinedGame] = useState(false);

  // One time setups:
  useEffect(() => {
    const playerInRoom = async (roomID, playerID) => {
      try {
        const response = await fetch(`${serverURL}/player_in_room?room_id=${roomID}&player_id=${playerID}`);
        return response.ok;
      } catch (error) {
        console.error("Error checking player in room:", error);
        return false;
      }
    };

    (async () => {
      const storedID = localStorage.getItem("playerID");
      const storedName = localStorage.getItem("playerName");
      const storedRoom = localStorage.getItem("roomCode");

      let currentID = storedID;
      if (storedID) {
        setPlayerID(storedID);
      } else {
        const newID = crypto.randomUUID();
        currentID = newID;
        setPlayerID(newID);
        localStorage.setItem("playerID", newID);
      }

      if (storedName) setPlayerName(storedName);
      if (storedRoom) {
        const isInRoom = await playerInRoom(storedRoom, currentID);
        if (isInRoom) {
          setRoomCode(storedRoom);
          await getRoomPlayers(storedRoom);
          setPlayerJoinedGame(true);
        }
      }
    })();
  }, []);

  // Socket listeners
  useEffect(() => {
    socket.on("player_joined_game", (response) => {
      setPlayers(response.players);
      setPlayerJoinedGame(true);
    });

    socket.on("JoinError", (response) => {
      alert(`Failed to join game: ${response.ErrorMessage}`);
    });

    return () => {
      socket.off("player_joined_game");
      socket.off("JoinError");
    };
  }, []);

  // Persist name/room when they change
  useEffect(() => {
    if (playerName) localStorage.setItem("playerName", playerName);
    if (roomCode) localStorage.setItem("roomCode", roomCode);
  }, [playerName, roomCode]);

  // Callbacks
  const joinGame = () => {
    if (playerName === null || roomCode === null) {
      alert("Please enter both your name and the room code.");
      return;
    }
    if (playerName.trim() === "" || roomCode.trim() === "") {
      alert("Please enter valid name and room code.");
      return;
    }

    try {
      const payload = {
        player_id: playerID,
        player_name: playerName,
        room_id: roomCode
      };
      // emit join; server will add the player and emit the updated players list
      socket.emit("join_game", payload);
    } catch (error) {
      console.error("Error joining game:", error);
    }
  }

  // helper functions
  const getRoomPlayers = async (room) => {
    try {
      const response = await fetch(`${serverURL}/players?room_id=${room}`);
      if (!response.ok) {
        // If something went wrong, assume the room DNE and remove it
        localStorage.removeItem("roomCode");
        return;
      }
      const data = await response.json();
      setPlayers(data.players);
      socket.emit("subscribe_room", { room_id: room });
    } catch (error) {
      console.error("Error fetching player names:", error);
    }
  };


  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Yearning for a few rounds of cards...</h2>
      {playerJoinedGame ? 
       (
        <div>
          <p>Players:</p>
          <p>{players.join(", ")}</p>
        </div>
      ):
      (
        <div>
          <input type="text" placeholder="Enter your name" onChange={(e) => setPlayerName(e.target.value)} style={{ padding: "10px", fontSize: "16px" }} />
          <input type="text" placeholder="Enter room code" onChange={(e) => setRoomCode(e.target.value)} style={{ padding: "10px", fontSize: "16px" }} />
          <button style={{ padding: "10px 20px", fontSize: "16px", marginLeft: "10px" }} onClick={joinGame}>
            Join Game
          </button>
        </div>
      ) }

    </div>
  );
}

export default JoinPage;
