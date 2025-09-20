:- use_module(library(clpfd)).

% player(Name, Team, Wins, Pref, History).
% bye(Name).

% Ensure game mode compatibility
compatible_mode(P, P).
compatible_mode(any, P) :- P \= any.
compatible_mode(P, any) :- P \= any.

% Resolve actual mode once compatible
resolved_mode(P, P, P).
resolved_mode(any, P, P) :- P \= any.
resolved_mode(P, any, P) :- P \= any.

% Valid pair: must be cross-team, compatible, not in history
valid_pair(A, B, Score, Mode, TeamA, TeamB) :-
    player(A, TeamA, WinsA, PrefA, HistoryA),
    player(B, TeamB, WinsB, PrefB, HistoryB),
    TeamA \= TeamB,  % Must be from different teams
    \+ member(B, HistoryA),
    \+ member(A, HistoryB),
    compatible_mode(PrefA, PrefB),
    resolved_mode(PrefA, PrefB, Mode),
    Score #= abs(WinsA - WinsB).

% Allow a bye (sit out one round)
valid_pair(Player, bye, 0, none, Team, _) :-
    player(Player, Team, _, _, _),
    \+ bye(Player).   % cannot get a bye twice

% Generate all possible assignments where each player gets exactly one assignment
generate_assignment(AllPlayers, Assignments) :-
    generate_assignment_aux(AllPlayers, [], Assignments),
    % Declarative constraint: at most 1 bye in the entire assignment
    findall(1, member(pair(_, bye, _), Assignments), Byes),
    length(Byes, NumByes),
    NumByes =< 1.

% Base case: no more players to assign
generate_assignment_aux([], Assignments, Assignments).

% Case 1: Match current player with another unassigned player
generate_assignment_aux([Player|Rest], AccAssignments, FinalAssignments) :-
    % Find another player from different team
    select(Other, Rest, NewRest),
    player(Player, TeamA, _, _, _),
    player(Other, TeamB, _, _, _),
    TeamA \= TeamB,
    valid_pair(Player, Other, _, Mode, TeamA, TeamB),
    generate_assignment_aux(NewRest, [pair(Player, Other, Mode)|AccAssignments], FinalAssignments).

% Case 2: Give current player a bye
generate_assignment_aux([Player|Rest], AccAssignments, FinalAssignments) :-
    player(Player, Team, _, _, _),
    valid_pair(Player, bye, 0, none, Team, _),
    generate_assignment_aux(Rest, [pair(Player, bye, none)|AccAssignments], FinalAssignments).

% Calculate total penalty for an assignment (lower is better)
% Penalty = total score + (number of byes * 1000) to strongly prefer matches over byes
assignment_penalty(Assignments, TotalPenalty) :-
    findall(Score, (member(pair(P1, P2, _), Assignments), 
                   (P2 = bye -> Score = 1000 ; 
                    (player(P1, T1, _, _, _), player(P2, T2, _, _, _),
                     valid_pair(P1, P2, Score, _, T1, T2)))), Scores),
    sum_list(Scores, TotalPenalty).

% Find best assignment (minimizing penalty = minimizing byes first, then score)
best_assignment(TeamA, TeamB, BestPairs, _TeamAName, _TeamBName) :-
    % Get all players from both teams
    findall(P, (member(P, TeamA) ; member(P, TeamB)), AllPlayers),
    findall(Penalty-Pairs, 
            (generate_assignment(AllPlayers, Pairs),
             assignment_penalty(Pairs, Penalty)), 
            All),
    sort(All, [_BestPenalty-BestPairs|_]).
