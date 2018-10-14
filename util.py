def time_conversion(td):
    seconds = td.seconds
    micro = td.microseconds
    ms = micro / 1000
    rem = ms / 1000
    return seconds + rem


POSITIONS = [
    'QB',
    'WR',
    'RB',
    'FLEX',
    'DST',
    'TE',
]


class Player(object):

    def __init__(self, name='', position=''):
        self.name = name
        self.position = position

    def __repr__(self):
        return '{} {}'.format(self.name, self.position)


def convert_lineup(csv_lineup: str) -> list:
    player_lst = []

    words = csv_lineup.split(' ')

    player = None
    for w in words:
        if w in POSITIONS:
            player = Player(position=w)
            if player:
                player_lst.append(player)
        elif player:
            player.name += '{} '.format(w)

    return player_lst
