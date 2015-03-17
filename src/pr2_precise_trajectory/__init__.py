
HEAD = 'h'
LEFT = 'l'
RIGHT = 'r'
BASE = 'b'
TIME = 't'
LEFT_HAND = 'lh'
RIGHT_HAND = 'rh'
MACRO = 'm'
AUDIO = 'a'

WHEELCHAIR = 'w'

DEFAULT_TIME = 3.0

def get_time(move):
    return move.get(TIME, DEFAULT_TIME)

def precise_subset(movements, key, end_time=True):
    t = 0.0
    L = []
    for move in movements:
        if key in move:
            if end_time:
                m = {key: move[key], TIME: get_time(move) + t }
                t = 0.0
            else:
                m = {key: move[key], TIME: t}
                t = get_time(move)
            L.append(m)
        else:
            t += get_time(move)
    return L


