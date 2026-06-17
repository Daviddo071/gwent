from pydantic import BaseModel

class JoinRequest(BaseModel):
    player_id: str
    player_name: str
    room_id: str
