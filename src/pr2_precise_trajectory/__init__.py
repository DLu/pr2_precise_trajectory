
HEAD = 'h'
LEFT = 'l'
RIGHT = 'r'
BASE = 'b'
TIME = 't'
LEFT_HAND = 'lh'
RIGHT_HAND = 'rh'
MACRO = 'm'

DEFAULT_TIME = 3.0

def get_time(move):
    return move.get(TIME, DEFAULT_TIME)

def precise_subset(movements, key, include_label=False):
    t = 0.0
    L = []
    for move in movements:
        if key in move:
            m = {key: move[key], TIME: get_time(move) + t }
            if include_label and 'label' in move:
                m['label'] = move['label']
            L.append(m)
            t = 0.0
        else:
            t += get_time(move)
    return L


