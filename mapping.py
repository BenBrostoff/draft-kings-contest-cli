import os
import csv

_DIR = os.path.dirname(os.path.abspath(__file__))
_LOOKUP_TABLE_LOCATION = '{}/data/LOOKUP.csv'.format(_DIR)


def build_lookup_table():
    lookup = {}
    with open(_LOOKUP_TABLE_LOCATION, 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            lookup[line['Name']] = line['TeamAbbrev']

    return lookup


def get_team(player, lookup_dict, args):
    p = lookup_dict.get(player)
    if not p and args.v:
        print('No team found for player {}'.format(p))

    return p
