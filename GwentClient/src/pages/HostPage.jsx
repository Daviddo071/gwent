import { useState, useEffect } from "react";

function HostPage() {
  const [gameCode, setGameCode] = useState(null);
  const serverURL = import.meta.env.VITE_SERVER_URL

  useEffect(() => {
    const createGame = async () => {
      try {
        const response = await fetch(`${serverURL}/create_game`, {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        const data = await response.json();
        setGameCode(data.room_id);
      } catch (err) {
        console.error("Error creating game:", err);
      }
    };

    createGame();
  }, [serverURL]);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Not hungry, not thirsty, but I sure wouldn't mind a few rounds of Gwent</h2>
      {gameCode ? (
        <p>Room code: {gameCode}</p>
      ) : (
        <p>Creating game...</p>
      )}
    </div>
  );
}

export default HostPage;
