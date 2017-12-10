# HearthDB

Purpose:

From raw HSReplay data generate:

1. Card usage statistics
2. Card Popularity graphs per hero
3. Deck vectors for model creation

## Running the code

1. Install requirements: `pip install -r requirements.txt`
2. Generate statistics: `python cardcounter.py`
3. Generate vectors: `python vectors.py`.

Using the popularity graph generator requires special steps for matplotlib which are not covered here. Use at your own discretion.


## Methods

```python
from vectors import get_decks, get_archs, get_card
```

### Get decks
```python
def get_decks(arch_id: int=None) -> list:
    """
    Returns a list of Deck objects for each deck in the archetype.
    Note that Deck.cards has had the popular cards removed.
    """
```

#### Example:
```python
some_arch = get_decks(arch_id=147)
```

### Get Archetypes
```python
def get_archs() -> list:
    """
    Returns a list of available archetypes
    """
```

#### Example:
```python
all_archs = get_archs()
```

### Look up a card
```python
def get_card(self, dbf_id: int) -> dict:
    """
    Returns dict representing a card. Useful attribute is the
    name.
    :param dbf_id: Int ID of the card you're looking for.
    :return: A dict representing a card.
    """
```

#### Example
```python
for cardid, count in priest_deck.as_cards():
    print(db.get_card(cardid)['name'])

```


