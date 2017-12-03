#pylint: disable=W0123,C0326
import json

card_map = json.load(open('vectors/card_map.json'))

class Deck:
    def __init__(self, arch_id: int, cards: list):
        self.arch_id = arch_id
        self.cards = cards

    def to_vector(self) -> list:
        vector = [0 for i in range(len(card_map))]

        for dbfid, count in self.cards:
            index = card_map.get(str(dbfid))
            vector[index] = count

        return vector

def get_archs() -> list:
    """
    Returns a list of available archetypes
    """
    with open('vectors/decks_by_archetype.json') as deckfile:
        decks_by_archetype = json.load(deckfile)
        return list(decks_by_archetype.keys())

def get_decks(arch_id: int=None) -> list:
    """
    Returns a list of Deck objects for each deck in the archetype.
    Note that Deck.cards has had the popular cards removed.
    """
    with open('vectors/decks_by_archetype.json') as deckfile:
        decks_by_archetype = json.load(deckfile)
        decks = list(decks_by_archetype.get(str(arch_id), list()))
        return [Deck(arch_id, d['cards']) for d in decks]

# Look up card names
card_db = json.load(open('db.json'))
def get_card(dbf_id: int) -> dict:
    """
    Returns dict representing a card. Useful attribute is the
    name.
    :param dbf_id: Int ID of the card you're looking for.
    :return: A dict representing a card.
    """
    return next(card for card in card_db if card["dbfId"] == dbf_id)


if __name__ == '__main__':
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
