import { useState, useEffect, useRef } from "react";
import { io } from "socket.io-client";

const socket = io(import.meta.env.VITE_SERVER_URL);
// module-level guard to avoid duplicate initialization across StrictMode remounts

function HostPage() {
  const [gameCode, setGameCode] = useState(null);
  const [players, setPlayers] = useState([]);
  const serverURL = import.meta.env.VITE_SERVER_URL
  const initRef = useRef(false);


  useEffect(() => {
    if (initRef.current) return;
    initRef.current = true;

    const createGame = async () => {
      try {
        const response = await fetch(`${serverURL}/create_game`, {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        const data = await response.json();
        setGameCode(data.room_id);
        localStorage.setItem("gameCode", data.room_id);
        socket.emit("subscribe_room", { room_id: data.room_id });
      } catch (err) {
        console.error("Error creating game:", err);
      }
    };
    const getRoomPlayers = async (room) => {
      try {
        const response = await fetch(`${serverURL}/players?room_id=${room}`);
        if (!response.ok) {
          localStorage.removeItem("gameCode");
          setGameCode(null);
          createGame();
          return;
        }
        const data = await response.json();
        setPlayers(data.players);
        socket.emit("subscribe_room", { room_id: room });
      } catch (error) {
        console.error("Error fetching player names:", error);
      }
    };


    const storedGameCode = localStorage.getItem("gameCode");
    if (storedGameCode) {
      setGameCode(storedGameCode);
      getRoomPlayers(storedGameCode);
    } else {
      createGame();
    }
  }, []);

  useEffect(() => {
    socket.on("player_joined_game", (response) => {
      setPlayers(response.players);
    });

    return () => {
      socket.off("player_joined_game");
    };
  }, []);

  const canStartGame = players.length === 2;

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Not hungry, not thirsty, but I sure wouldn't mind a few rounds of Gwent</h2>
      {gameCode ? (
        <p>Room code: {gameCode}</p>
      ) : (
        <p>Creating game...</p>
      )}
      {
        canStartGame ? (
          <button>Start Game</button>
        ) : (
          <p>Waiting for players to join...</p>
        )
      }
      <p>Current players:</p>
      <p>{players.join(", ")}</p>
    </div>
  );
}

export default HostPage;
