
# Forward your ports to the DB

```bash
ssh -L 27017:localhost:27017 hearthdb@andrewsosa.com
# password is ALongAndVeryComplicatedPassword
```

# Use HearthDB

```python
from HearthDB import HearthDB 
db = HearthDB()
```

## Methods 

### Get decks
```python
def get_decks(self, hero: int=None):
    """
    Returns an interable of deck models per Hero, or all if
    no hero specified.
    :param hero: Pass a Deck.CLASS_ constant
    :return: Iterable of decks.
    """
```

#### Example:
```python
priest_decks = db.get_decks(hero=HearthDB.CLASS_PRIEST)
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


### Count decks
```python
def deck_count(self, hero: int=None) -> int:
    """
    Returns a count of the decks available per Hero, or all if
    no hero specified.
    :param hero: Pass a Deck.CLASS_ constant
    :return: Int number of decks per class.
    """
```

#### Example
```python
num = db.deck_count(HearthDB.CLASS_PRIEST)
```