from typing import List, Optional
from pydantic import BaseModel

from Models.Game.Player import Player

class Game(BaseModel):
    players: Optional[List[Player]] = []
