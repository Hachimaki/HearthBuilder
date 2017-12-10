from vectors import get_decks, get_archs
from vectors import card_map

def main():

    inv_map = {v: k for k, v in card_map.items()}
    indexes = sorted(inv_map.keys())
    ids = [inv_map[index] for index in indexes]
    print('win_rate, archetype, ' + ', '.join(ids))

    for arch in get_archs():
        for deck in get_decks(int(arch)):
            vs = str(deck.to_vector()).replace('[', '').replace(']', '')
            print(str(deck.win_rate) + ', ' + str(deck.arch_id) + ', ' + vs)

if __name__ == '__main__':
    main()
