# pylint: disable=W0123,C0201,W0621
import json, statistics
from collections import Counter

total_decks = 0
decks_per_hero = Counter()
card_counter_unique = Counter()
card_counter_unique_neutral = Counter()

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

cards_per_hero_unique = {hero: Counter() for hero in heroes.keys()}
cards_per_hero_choice = {hero: Counter() for hero in heroes.keys()}

card_choice_overall = Counter()
card_choice_no_legendary = Counter()

card_choice_neutral = Counter()
card_choice_neutral_per_hero = {hero: Counter() for hero in heroes.keys()}

card_choice_hero_only = {hero: Counter() for hero in heroes.keys()}

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
                card_counter_unique[dbfID] += 1
                cards_per_hero_unique[hero][dbfID] += 1
                cards_per_hero_choice[hero][(dbfID, count)] += 1
                card_choice_overall[(dbfID, count)] += 1

                card = get_card(dbfID)
                if card["rarity"] != "LEGENDARY":
                    card_choice_no_legendary[(dbfID, count)] += 1

                if card["playerClass"] == "NEUTRAL":
                    card_choice_neutral[(dbfID, count)] += 1
                    card_choice_neutral_per_hero[hero][(dbfID, count)] += 1
                    card_counter_unique_neutral[dbfID] += 1
                else:
                    card_choice_hero_only[hero][(dbfID, count)] += 1




# Normalize per-hero data
normal_hero_unique_counts = Counter()
normal_neutral_card_choice = Counter()
normal_all_choice = Counter()

def normalize_heroes(input_dict: dict, output: dict):
    card_hero_pres_percent = dict()
    for hero, counter in input_dict.items():
        for dbfID, count in counter.most_common():
            if card_hero_pres_percent.get(dbfID, None) is None:
                card_hero_pres_percent[dbfID] = dict()
            card_hero_pres_percent[dbfID][hero] = count / decks_per_hero[hero]

    for dbfID, _dict in card_hero_pres_percent.items():
        percents = [_dict.get(hero, 0) for hero in heroes.keys()]
        output[dbfID] = "{0:.4f}".format(statistics.mean(percents))


normalize_heroes(cards_per_hero_unique, normal_hero_unique_counts)
normalize_heroes(card_choice_neutral_per_hero, normal_neutral_card_choice)
normalize_heroes(cards_per_hero_choice, normal_all_choice)

# Write files
def write_counter_file(countfile, counter, deck_count=total_decks, show_fraction=False,
                       tuple_key=False):
    countfile.write("total decks: {}\n".format(deck_count))
    for card, count in counter.most_common():
        if show_fraction:
            count = "{0:.4f}".format(count / deck_count)
            # count = count / deck_count

        if not tuple_key:
            countfile.write("{}, {}\n".format(count, get_card(card)['name']))
        else:
            dbfID, times = card
            countfile.write("{}, {}, {}\n".format(count, get_card(dbfID)['name'], times))


# Percentage of unique appearances across total decks
write_counter_file(open('data/unique.csv', 'w'), card_counter_unique,
                   show_fraction=True)

# Percentage of unique appearances normalized for heroes
write_counter_file(open('data/unique_normal.csv', 'w'),
                   normal_hero_unique_counts)

# Percentage of unique appearances for only neutral cards
write_counter_file(open('data/neutral/unique.csv', 'w'), card_counter_unique_neutral,
                   show_fraction=True)

# Percentage of choices of neutral cards normalized for heroes
write_counter_file(open('data/neutral/choice_normal.csv', 'w'), normal_neutral_card_choice,
                   tuple_key=True)

# Normalized percentange of choices overall
write_counter_file(open('data/choice_normal.csv', 'w'), normal_all_choice,
                   tuple_key=True)

# Count of choice appearances for neutral cards (less useful)
write_counter_file(open('data/neutral/choice_count.csv', 'w'), card_choice_overall, tuple_key=True)

# Count of choice appearances for neutral cards with legendaries removed (less useful)
write_counter_file(open('data/neutral/count_no_legendary.csv', 'w'), card_choice_no_legendary,
                   tuple_key=True)

#
for hero, counter in card_choice_hero_only.items():
    write_counter_file(open('data/hero/choices_{}.csv'.format(hero), 'w'),
                       counter, decks_per_hero[hero], show_fraction=True, tuple_key=True)

#
for hero, counter in cards_per_hero_unique.items():
    write_counter_file(open('data/hero/neutral/unique_{}.csv'.format(hero), 'w'),
                       counter, decks_per_hero[hero], show_fraction=True)
