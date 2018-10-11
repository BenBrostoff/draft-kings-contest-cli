import re
import csv
import pickle
from datetime import datetime
from collections import Counter
import crayons
from terminaltables import AsciiTable
import argparse
from mapping import build_lookup_table, get_team
from util import time_conversion

start = datetime.now()

parser = argparse.ArgumentParser(description='Process DraftKings contest results.')
parser.add_argument('-ms', type=int, default=150)
parser.add_argument('-player', type=str, default='')
parser.add_argument('-v', type=str, default='')
parser.add_argument('-csv', type=str, default='week.csv')
parser.add_argument('-use_cache', type=str, default='')

args = parser.parse_args()

# TODO - figure out way to build regex that doesn't
# get blank first string

# TODO - Control the print output
# Command line flag to limit number of players shown

# TODO - separate data gather and filtering options

SPLIT = 'QB | RB | QB | WR | FLEX | DST | TE'

# TODO - figure out what numerator means


lineups_analyzed = 0

entry_names = []
player_to_analyze = args.player
entries_to_analyze = []

if args.use_cache:
    entries_to_analyze = pickle.load(open('entries.p', 'rb'))
    print(len(entries_to_analyze))
else:
    with open(args.csv, 'r') as f:
        lookup_table = build_lookup_table()
        reader = csv.DictReader(f)
        for line in reader:
            entry_teams = []

            points = float(line['Points'])
            entry_components = line['EntryName'].split(' ')
            player = entry_components[0]

            if len(entry_components) < 2:
                numerator = 0
                total_entries = 0
            else:
                number_components = entry_components[1].split('/')
                numerator = number_components[0].replace('(', '')
                total_entries = \
                    int(
                        number_components[1].replace(')', '')
                    )

            if points < float(args.ms):
                break

            entry_names.append(player)
            lineup = line['Lineup']
            players = [
                p for p in
                re.split(SPLIT, lineup)
                if p
            ]

            for p in players:
                team = get_team(p, lookup_table, args)
                if team:
                    entry_teams.append(team)

            freq = Counter(entry_teams)

            fours = ''
            threes = ''
            twos = ''
            for team, count in freq.items():
                if count == 4:
                    fours += '{}, '.format(team)
                elif count == 3:
                    threes += '{}, '.format(team)
                elif count == 2:
                    twos += '{}, '.format(team)

            # TODO - this shouldn't be in data building stage
            if not args.player or player == args.player:
                entries_to_analyze.append([
                    player,
                    numerator,
                    total_entries,
                    points,
                    fours,
                    threes,
                    twos
                ])

            lineups_analyzed += 1

    pickle.dump(entries_to_analyze, open('entries.p', 'wb'))

HEADERS = [[
    'Player',
    'Numerator',
    'Total Entries',
    'Points',
    '4s',
    '3s',
    '2s'
]]
final = HEADERS + entries_to_analyze
table = AsciiTable(HEADERS + entries_to_analyze)

print(table.table)
print(crayons.green('Analyzed {} lineups'.format(len(entries_to_analyze))))

end = datetime.now()

print(
    crayons.yellow('Script took {} seconds'.format(
        time_conversion(end - start))
    )
)