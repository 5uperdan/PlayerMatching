"""Prolog interface utilities.

All prolog interactions should go through this module to ensure that atoms are made safe exactly once.
"""

import re
from typing import Iterable

from pyswip import Prolog

from player_matching.data_types import GameMode, Match, Player, Team


def safe_atom(name: str) -> str:
    """Convert a string to a Prolog-safe atom (lowercase, quoted)."""
    return f"'{name.lower()}'"


def safe_list(unsafe_atoms: Iterable[str]) -> str:
    """Convert Python list to Prolog list string, escaping atoms."""
    return "[{}]".format(",".join(safe_atom(x) for x in unsafe_atoms))


def reset_prolog_state(prolog: Prolog):
    """Reset all player and bye facts in Prolog."""

    # prolog.query returns a generator is lazily executed, so the list conversion forces execution
    list(prolog.query("retractall(player(_,_,_,_,_))"))
    list(prolog.query("retractall(bye(_))"))


def add_player(prolog: Prolog, player: Player, unsafe_team: str):
    """Add a player fact, making all atoms safe."""
    name_atom = safe_atom(player.name)
    team_atom = safe_atom(unsafe_team)
    wins = player.wins
    game_mode_atom = safe_atom(player.game_mode.value)
    history_str = safe_list(player.history)

    prolog.assertz(f"player({name_atom}, {team_atom}, {wins}, {game_mode_atom}, {history_str})")


def add_bye(prolog: Prolog, unsafe_name: str):
    """Add a bye fact for a player."""
    prolog.assertz(f"bye({safe_atom(unsafe_name)})")


def parse_prolog_pairs(pairs_data: list[str]) -> list[Match]:
    """Parse Prolog pairs data into Match objects."""
    matches: list[Match] = []

    for pair_string in pairs_data:
        # Use regex to extract player1, player2, and mode from strings like:
        # 'pair(a1, b1, core)' or 'pair(a4, bye, none)'
        pattern = r"pair\((\w+),\s*(\w+),\s*(\w+)\)"
        match = re.match(pattern, str(pair_string))

        if match:
            player_1 = match.group(1)
            player_2 = match.group(2)
            mode_str = match.group(3)

            # Convert mode string to GameMode enum
            if mode_str == "none":
                game_mode = GameMode.BYE
            else:
                game_mode = GameMode(mode_str.lower())

            if player_2 == "bye":
                match_obj = Match(player_1=player_1, game_mode=game_mode)
            else:
                match_obj = Match(player_1=player_1, player_2=player_2, game_mode=game_mode)

            matches.append(match_obj)

    return matches


def find_best_assignment(prolog: Prolog, team_a: Team, team_b: Team) -> list[Match] | None:
    """Query Prolog for best assignment, returning structured MatcherOutput."""
    team_a_players = safe_list([p.name for p in team_a.players])
    team_b_players = safe_list([p.name for p in team_b.players])
    team_a_atom = safe_atom(team_a.name)
    team_b_atom = safe_atom(team_b.name)

    query = f"best_assignment({team_a_players}, {team_b_players}, Pairs, {team_a_atom}, {team_b_atom})."

    # vomit
    result: list[dict[str, list[str]]] = list(prolog.query(query, maxresult=1))
    if result:
        pairs_data = result[0].get("Pairs")

        assert pairs_data, "Prolog query returned no pairs data"

        return parse_prolog_pairs(pairs_data=pairs_data)
    else:
        return None
