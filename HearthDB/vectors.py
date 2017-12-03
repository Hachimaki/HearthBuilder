#pylint: disable=W0123
import json

card_map = json.load(open('vectors/card_map.json'))

class Deck:
    def __init__(self, arch_id: int, cards: list):
        self.arch_id = arch_id
        self.cards = cards

    def to_vector(self) -> list:
        pass

# Read cards dataset
with open('dataset.json') as dataset, open('vectors/most_popular_cards.json') as most_common:
    common = set(json.load(most_common)['most_common'])

    all_decks = json.load(dataset)['series']['data']
    all_archetypes = dict()

    for hero, decks in all_decks.items():
        for deck in decks:
            cards = eval(deck['deck_list'])
            cards = list(filter((lambda pair: pair[0] not in common), cards))
            arch = deck['archetype_id']

            if arch not in all_archetypes.keys():
                all_archetypes[arch] = list()

            all_archetypes[arch].append({
                'cards': cards,
                'archetype_id': arch
            })

    with open('vectors/decks_by_archetype.json', 'w') as outfile:
        outfile.write(json.dumps(all_archetypes))
