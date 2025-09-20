import openpyxl

from .data_types import Team


def load_teams_from_xlsx(file_path: str) -> list[Team]:
    """Load teams and players from an xlsx file."""
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    teams = []
    current_team = None
    seen_player_names = set()  # To track duplicate player names

    for row in sheet.iter_rows(min_row=2, values_only=True):
        team_name, player_name, player_wins, player_pref, player_history = row

        if team_name != current_team:
            if current_team is not None:
                teams.append(current_team)
            current_team = Team(name=team_name, players=[])
        player = Player(
            name=player_name,
            wins=player_wins,
            pref=GameMode[player_pref],
            history=player_history.split(",") if player_history else [],
        )
        current_team.players.append(player)

    if current_team is not None:
        teams.append(current_team)

    return teams
