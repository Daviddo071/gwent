from pydantic import BaseModel

class GameInfoRequest(BaseModel):
    room_id: str
