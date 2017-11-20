from random import *
import collections

''' "numGames" "winRate" "cID1" "cID2" "cID3" '''

model = []
numDecks = 1000
totalCards = 30
numArchs = 10

for i in range(0, numDecks):
    x = randint(1, numArchs)
    y = randint(1000, 10000)
    z = round(uniform(0.40, 0.65), 2)

    m = {"type":x,"numGames":y, "winRate":z}
    deck = collections.OrderedDict(m)
    deck.update({"cd1":2})
    numCards = 2;

    for i in range(2, totalCards+1):
        card = "cd" + str(i)
        num = randint(0, 2)
        if (numCards + num) < 30:      #BINGO BANGO BONGO
            deck.update({card:num})
            numCards += num
        else:
            deck.update({card:0})

    model.append(deck);

archmodel = collections.OrderedDict()
cards = collections.OrderedDict()

for i in range(1, numArchs+1):
    archmodel.update({str(i):collections.OrderedDict()})

for i in range(1, totalCards+1):
    cards.update({"cd" + str(i):0})

for i in archmodel:
    for j in range(1, totalCards+1):
        archmodel[i].update({'cd' + str(j):0})

print model

for i in model:
    for j in range(1, totalCards+1):
        if i['cd' + str(j)] > 0:
            cards['cd' + str(j)] += 1

for i in archmodel:
    for j in model:
        if j['type'] == int(i):
            for k in range(1, totalCards+1):
                if j['cd' + str(k)] > 0:
                    archmodel[i].update({'cd' + str(k):archmodel[i]['cd'+str(k)] + 1})

for i in archmodel:
    for k, v in archmodel[i].items():
        div = float(cards[k])
        if(div != 0):
            archmodel[i].update({k: round(float(v)/div, 2)})
        else:
            archmodel[i].update({k: 0})

print "type ",

for i in range(1, totalCards+1):
    print "cd" + str(i),

print ""

for i in archmodel:
    print i,
    for k, v in archmodel[i].items():
        print v,
    print ""


for k,v in cards.items():
    print k, v
