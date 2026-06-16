import { useState } from "react";


function JoinPage() {
  const [playerName, setPlayerName] = useState(null);
  const [roomCode, setRoomCode] = useState(null);
  const serverURL = import.meta.env.VITE_SERVER_URL


  const joinGame = async () => {
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
        player_name: playerName,
        room_id: roomCode
      };

      const response = await fetch(`${serverURL}/join_game`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        const joinResponse = await response.json();
        const currentPlayers = joinResponse.Players;
        alert(`Join success, current players: ${currentPlayers}`);
      } else {
        const errorResponse = await response.json();
        alert(`Failed to join game due to ${errorResponse.ErrorType} - ${errorResponse.ErrorMessage}`);
      }

    } catch (error) {
      console.error("Error joining game:", error);
    }
  }


  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Yearning for a few rounds of cards...</h2>
      <input type="text" placeholder="Enter your name" onChange={(e) => setPlayerName(e.target.value)} style={{ padding: "10px", fontSize: "16px" }} />
      <input type="text" placeholder="Enter room code" onChange={(e) => setRoomCode(e.target.value)} style={{ padding: "10px", fontSize: "16px" }} />
      <button style={{ padding: "10px 20px", fontSize: "16px", marginLeft: "10px" }} onClick={joinGame}>
        Join Game
      </button>
    </div>

  ); 

}
export default JoinPage;
