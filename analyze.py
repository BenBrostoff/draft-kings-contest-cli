import re
import csv
import sys
import crayons
from collections import Counter
from terminaltables import AsciiTable
from mapping import build_lookup_table, get_team


# TODO - figure out way to build regex that doesn't
# get blank first string
SPLIT = 'QB | RB | QB | WR | FLEX | DST | TE'

# TODO
# Get terminal tables to work
# 10/7 -> List of 4, 3, 2,... with tema
# After -> handle multiple team instances


lineups_analyzed = 0
qbs = []
rb_1s = []
rb_2s = []
wr_1s = []
wr_2s = []
wr_3s = []
tes = []
flexs = []
defs = []

position_holders = [
     qbs,
     rb_1s,
     rb_2s,
     wr_1s,
     wr_2s,
     wr_3s,
     tes,
     defs,
]

entry_names = []
player_to_analyze = sys.argv[1]
entries_to_analyze = []

lookup_table = build_lookup_table()
with open('./week-4-results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for line in reader:
        entry_teams = []

        points = float(line['Points'])
        if points < float(sys.argv[2]):
            break 
        
        player = line['EntryName'].split(' ')[0]
        entry_names.append(player)
        if player == player_to_analyze:
            entries_to_analyze.append([line['Lineup'], points])

        lineup = line['Lineup']
        players = [
            p for p in
            re.split(SPLIT, lineup)
            if p
        ]

        for p in players:
            team = get_team(p, lookup_table)
            if team:
                entry_teams.append(team)

        for idx, lst in enumerate(position_holders):
            lst.append(players[idx + 1])

        lineups_analyzed += 1
        print(entry_teams)


def pretty_print_counter(c, lineups):
    for name, count in list(c.items())[:50]:
        pct = count / lineups_analyzed * 100
        print(crayons.yellow('{} {} {}'.format(name, count,  pct)))


for pos in position_holders:
    c = Counter(pos)
    print('')
    print('')
    pct_total = 0
    for name, count in c.items():
        pct = round(float(count) / lineups_analyzed, 5) * 100.0
        print(crayons.yellow('{} {} {}'.format(name, count,  pct)))
        pct_total += pct

    print(pct_total)

print('')
print('')
pretty_print_counter(Counter(entry_names), lineups_analyzed)
print(crayons.green('Lineups analyzed {}'.format(lineups_analyzed)))
print('Analyzing for {}'.format(sys.argv[1]))

for e in entries_to_analyze:
    print('')
    print('')
    print(e[1])
    print(re.split(SPLIT, e[0]))
