from pyswip import Prolog

from player_matching.data_types import Team
from player_matching.prolog_interface import add_bye, add_player, find_best_assignment, reset_prolog_state
from player_matching.settings import general_settings
from player_matching.xlsx_interface import load_match_data_from_xlsx, load_team_data_from_xlsx, write_next_round_to_xlsx


def add_competition_state(prolog: Prolog, teams: list[Team]):
    """Add competition state to Prolog."""
    reset_prolog_state(prolog)

    [add_player(prolog=prolog, player=player, unsafe_team=team.name) for team in teams for player in team.players]

    [add_bye(prolog=prolog, unsafe_name=player.name) for team in teams for player in team.players if player.had_bye]


if __name__ == "__main__":

    prolog = Prolog()
    prolog.consult("./matcher.pl", relative_to=__file__)

    teams = load_team_data_from_xlsx(file_name=general_settings.xlsx_name, team_names=general_settings.team_names)
    load_match_data_from_xlsx(file_name=general_settings.xlsx_name, teams=teams)

    add_competition_state(prolog=prolog, teams=teams)
    matches = find_best_assignment(prolog=prolog, team_a=teams[0], team_b=teams[1])

    for team in teams:
        print(f"{team.name}: {team.score} points")

    if matches:
        print("\nRegular matches:")
        for match in matches:
            print(f"  {match.player_1} vs {match.player_2} ({match.game_mode.value})")
        write_next_round_to_xlsx(file_name=general_settings.xlsx_name, matches=matches)
    else:
        print("No valid assignment found!")
