# pylint: disable=W0123,C0201,W0621
import json
from collections import Counter

total_decks = 0
decks_per_hero = Counter()
card_counter_total = Counter()
card_counter_unique = Counter()

heroes = {
    'DRUID' : 274,
    'HUNTER' : 31,
    'MAGE' : 637,
    'PALADIN': 671,
    'PRIEST': 813,
    'ROGUE': 930,
    'SHAMAN': 1066,
    'WARLOCK': 893,
    'WARRIOR': 7
}

cards_per_hero_total = {hero: Counter() for hero in heroes.keys()}
cards_per_hero_unique = {hero: Counter() for hero in heroes.keys()}

# Look up card names
card_db = json.load(open('db.json'))
def get_card(dbf_id: int) -> dict:
    return next(card for card in card_db if card["dbfId"] == dbf_id)

# Read dataset
with open('dataset.json') as json_data:
    data = json.load(json_data)['series']['data']

    for hero, decks in data.items():
        decks_per_hero[hero] = len(decks)
        total_decks += len(decks)
        for deck in decks:
            cards = eval(deck['deck_list'])
            for dbfID, count in cards:
                card_counter_total[dbfID] += count
                card_counter_unique[dbfID] += 1
                cards_per_hero_total[hero][dbfID] += count
                cards_per_hero_unique[hero][dbfID] += 1


# Normalize per-hero data
normal_hero_total_counts = Counter()
normal_hero_unique_counts = Counter()

def normalize(input_dict: dict, output: dict):
    for hero, counter in input_dict.items():
        for dbfID, count in counter.most_common():
            if dbfID not in output:
                output[dbfID] = 0.0
            output[dbfID] += (count / decks_per_hero[hero])

# normalize(cards_per_hero_total, normal_hero_total_counts)
# normalize(cards_per_hero_unique, normal_hero_unique_counts)


# Write files
def write_counter_file(countfile, counter, deck_count=total_decks, show_fraction=False):
    countfile.write("total decks: {}\n".format(deck_count))
    for card, count in counter.most_common():
        if show_fraction:
            count = "{}/{}".format(count, deck_count)
        countfile.write("{}, {}\n".format(count, get_card(card)['name']))


write_counter_file(open('data/cardcounts_total.csv', 'w'), card_counter_total)
write_counter_file(open('data/cardcounts_unique.csv', 'w'), card_counter_unique,
                   show_fraction=True)
# write_counter_file(open('data/cardcounts_total_normal.csv', 'w'), normal_hero_total_counts)
write_counter_file(open('data/cardcounts_unique_normal.csv', 'w'),
                   normal_hero_unique_counts)

for hero, counter in cards_per_hero_unique.items():
    write_counter_file(open('data/hero/cardcounts_unique_{}.csv'.format(hero), 'w'),
                       counter, decks_per_hero[hero], show_fraction=True)
