import csv
import pickle
from datetime import datetime
from collections import Counter
import crayons
from terminaltables import AsciiTable
import argparse
from mapping import build_lookup_table, get_team, get_pos
from util import time_conversion, convert_lineup

start = datetime.now()

parser = argparse.ArgumentParser(description='Process DraftKings contest results.')
parser.add_argument('-ms', type=int, default=150)
parser.add_argument('-player', type=str, default='')
parser.add_argument('-v', type=str, default='')
parser.add_argument('-csv', type=str, default='week.csv')
parser.add_argument('-use_cache', type=str, default='')
parser.add_argument('-show', type=int, default=25)

# TODO - be able to tie to salaries
# LT TODO - be able to play these exact lineups
# TODO - figure out what numerator means

def get_csv_data(args: argparse.Namespace) -> list:
    entry_names = []
    entries_to_analyze = []

    if args.use_cache:
        entries_to_analyze = pickle.load(open('entries.p', 'rb'))
    else:
        print(args.csv)
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
                players = convert_lineup(lineup)

                for p in players:
                    team = get_team(p.name.strip(), lookup_table, args)
                    if team:
                        entry_teams.append(team)

                flex = [
                    p for p in players
                    if p.position == 'FLEX'
                ][0]

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

                # TODO - pass dict instead of list
                entries_to_analyze.append([
                    player,
                    get_pos(
                        flex.name.strip(),
                        lookup_table,
                        args
                    ),
                    flex.name,
                    total_entries,
                    points,
                    fours,
                    threes,
                    twos
                ])

        pickle.dump(entries_to_analyze, open('entries.p', 'wb'))

    return entries_to_analyze


def filter_data(all_entries: list, args: argparse.Namespace) -> list:
    filtered_entries = []
    for entry in all_entries:
        player = entry[0]
        if not args.player or player == args.player:
            filtered_entries.append(entry)

    return filtered_entries


if __name__ == '__main__':
    args = parser.parse_args()
    HEADERS = [[
        'Player',
        'Flex',
        'Flex Player',
        'Total Entries',
        'Points',
        '4s',
        '3s',
        '2s'
    ]]

    all_entries = get_csv_data(args)
    entries_to_analyze = filter_data(
        all_entries,
        args
    )

    table_data = HEADERS + entries_to_analyze[:args.show]
    table = AsciiTable(table_data)

    print(table.table)
    print(crayons.green('Analyzed {} lineups'.format(len(entries_to_analyze))))

    end = datetime.now()

    print(
        crayons.yellow('Script took {} seconds'.format(
            time_conversion(end - start))
        )
    )