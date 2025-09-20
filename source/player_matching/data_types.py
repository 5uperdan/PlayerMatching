from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class GameMode(Enum):
    CORE = "core"
    MOVIE = "movie"
    ANY = "any"
    DROP = "drop"
    BYE = "bye"


@dataclass
class Player:
    name: str
    game_mode: GameMode
    wins: int = 0  # match (not round) wins
    history: list[str] = field(default_factory=list[str])  # names of players faced before
    had_bye: bool = False  # has this player had a bye before


@dataclass
class Team:
    name: str
    _players: dict[str, Player] = field(default_factory=dict[str, Player])

    def add_player(self, player: Player):
        """Add a player to the team."""
        self._players[player.name] = player

    @property
    def players(self) -> list[Player]:
        """Return the list of players in the team, excluding dropped players."""
        return [player for player in self._players.values() if player.game_mode != GameMode.DROP]

    @property
    def score(self) -> int:
        """Return the total score of the team."""
        return sum(player.wins for player in self.players)


@dataclass
class Match:
    """Represents a single match between two players or a bye."""

    game_mode: GameMode
    player_1: str  # The first player (always present)
    player_2: Optional[str] = None  # The second player (None for bye)

    @property
    def is_bye(self) -> bool:
        """Return True if this is a bye match."""
        return self.player_2 is None
