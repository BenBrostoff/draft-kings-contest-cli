import csv


def build_lookup_table():
    lookup = {}
    with open('./LOOKUP.csv', 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            # TODO - BUILD LOOKUP DICT
            lookup[line['Name']] = line['TeamAbbrev']

    return lookup


def get_team(player, lookup_dict, args):
    p = lookup_dict.get(player)
    if not p and args.v:
        print('No team found for player {}'.format(p))

    return p
