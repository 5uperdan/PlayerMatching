from pyswip import Prolog

from player_matching.data_types import GameMode, Player, Team
from player_matching.prolog_interface import add_bye, add_player, find_best_assignment, reset_prolog_state


def load_competition_state(prolog: Prolog, teams: list[Team]):
    """Load players and byes into Prolog facts via prolog_interface."""
    reset_prolog_state(prolog)

    [add_player(prolog=prolog, player=player, unsafe_team=team.name) for team in teams for player in team.players]

    [add_bye(prolog=prolog, unsafe_name=player.name) for team in teams for player in team.players if player.had_bye]


if __name__ == "__main__":
    prolog = Prolog()
    prolog.consult("./matcher.pl", relative_to=__file__)

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

    load_competition_state(prolog=prolog, teams=[team_a, team_b])
    matches = find_best_assignment(prolog=prolog, team_a=team_a, team_b=team_b)

    if matches:
        print("\nRegular matches:")
        for match in matches:
            print(f"  {match.player_1} vs {match.player_2} ({match.game_mode.value})")
    else:
        print("No valid assignment found!")
