import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { isMobile } from 'react-device-detect';

function WelcomePage() {
  const navigate = useNavigate();

  useEffect(() => {

    if (isMobile) {
      navigate("/join");
    }
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>How about a round of Gwent?</h1>
      <button onClick={() => navigate("/host")}>Host</button>
      <p></p>
      <button onClick={() => navigate("/join")}>Join</button>
    </div>
  );
}

export default WelcomePage;
