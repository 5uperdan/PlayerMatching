from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class GameMode(Enum):
    CORE = "core"
    FRANCHISE = "franchise"
    ANY = "any"
    DROP = "drop"
    BYE = "bye"


class Player(BaseModel):
    name: str
    game_mode: GameMode
    wins: int = 0  # match (not round) wins
    history: list[str] = Field(default_factory=list)  # names of players faced before
    had_bye: bool = False  # has this player had a bye before


@dataclass
class Team:
    name: str
    _players: dict[str, Player] = field(default_factory=dict[str, Player])

    def add_player(self, player: Player):
        """Add a player to the team."""
        player.name = player.name.lower()
        self._players[player.name] = player

    @property
    def players(self) -> list[Player]:
        """Return the list of players in the team, excluding dropped players."""
        return [player for player in self._players.values() if player.game_mode != GameMode.DROP]

    @property
    def score(self) -> int:
        """Return the total score of the team."""
        return sum(player.wins for player in self.players)


class Match(BaseModel):
    """Represents a single match between two players or a bye."""

    game_mode: GameMode
    player_1: str  # The first player (always present)
    player_2: Optional[str] = None  # The second player (None for bye)

    @property
    def is_bye(self) -> bool:
        """Return True if this is a bye match."""
        return self.player_2 is None


class MatchResult(BaseModel):
    player_1_name: str
    player_2_name: Optional[str]
    game_mode: GameMode
    player_a_wins: int
    player_b_wins: int
