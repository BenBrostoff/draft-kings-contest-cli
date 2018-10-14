import os
import csv
from argparse import Namespace

_DIR = os.path.dirname(os.path.abspath(__file__))
_LOOKUP_TABLE_LOCATION = '{}/data/LOOKUP.csv'.format(_DIR)


def build_lookup_table():
    lookup = {}
    with open(_LOOKUP_TABLE_LOCATION, 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            lookup[line['Name']] = {
                'team': line['TeamAbbrev'],
                'pos': line['Position'],
            }

    return lookup


def get_team(player, lookup_dict, args):
    datum = lookup_dict.get(player)
    if not datum:
        if args.v:
            print('No team found for player {}'.format(player))
        return None

    return datum['team']


def get_pos(player: str, lookup_dict: dict, args: Namespace):
    datum = lookup_dict.get(player)
    if not datum:
        if args.v:
            print('No position found for player {}'.format(player))
        return None

    return datum['pos']
