import pytest
from pyswip import Prolog

from player_matching.data_types import GameMode, Match, Player, Team
from player_matching.main import add_competition_state
from player_matching.prolog_interface import find_best_assignment


@pytest.fixture
def prolog() -> Prolog:
    """Provide a Prolog instance with matcher.pl loaded for testing."""
    prolog_instance = Prolog()
    prolog_instance.consult("../player_matching/matcher.pl", relative_to=__file__)
    return prolog_instance


# TODO: make unit tests, not one single integration test like this
def test_example_assignment(prolog: Prolog) -> None:
    team_a = Team("Team A")
    team_a.add_player(Player(name="a1", wins=10, game_mode=GameMode.CORE, history=["b1"]))
    team_a.add_player(Player(name="a2", wins=5, game_mode=GameMode.ANY, history=[]))
    team_a.add_player(Player(name="a3", wins=8, game_mode=GameMode.ANY, history=["b2"]))
    team_a.add_player(Player(name="a4", wins=8, game_mode=GameMode.ANY, history=[], had_bye=True))

    team_b = Team("Team B")
    team_b.add_player(Player(name="b1", wins=9, game_mode=GameMode.CORE, history=["a1"]))
    team_b.add_player(Player(name="b2", wins=4, game_mode=GameMode.ANY, history=["a3"]))
    team_b.add_player(Player(name="b3", wins=7, game_mode=GameMode.ANY, history=[]))
    team_b.add_player(Player(name="b4", wins=7, game_mode=GameMode.DROP, history=[]))

    add_competition_state(prolog=prolog, teams=[team_a, team_b])
    matches = find_best_assignment(prolog=prolog, team_a=team_a, team_b=team_b)

    assert matches is not None
    assert len(matches) == 4  # Expecting 4 matches (including a bye)

    # Expected matches based on the current output
    expected_matches = [
        Match(player_1="a4", player_2="b1", game_mode=GameMode.CORE),
        Match(player_1="a3", player_2="b3", game_mode=GameMode.ANY),
        Match(player_1="a2", player_2="b2", game_mode=GameMode.ANY),
        Match(player_1="a1", player_2=None, game_mode=GameMode.BYE),
    ]

    assert matches == expected_matches
