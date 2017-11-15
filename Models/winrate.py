from random import *
import collections

''' "numGames" "winRate" "cID1" "cID2" "cID3" '''

model = []
numDecks = 10000

for i in range(0, numDecks+1):
    x = randint(1000, 10000)
    y = round(uniform(0.40, 0.65), 2)

    m = {"numGames":x, "winRate":y}
    deck = collections.OrderedDict(m)
    deck.update({"cd1":2})
    numCards = 2;

    for i in range(2, 31):
        card = "cd" + str(i)
        num = randint(0, 2)
        if (numCards + num) < 30:
            deck.update({card:num})
            numCards += num
        else:
            deck.update({card:0})

    model.append(deck);


archmodel = collections.OrderedDict()

for j in range(1, 31):
    numGames = 0
    p = 0.0
    q = 0

    for i in model:
        #print "=-=-=-=-=-=-=-=-=Deck=-=-=-=-=-=-=-=-=-=-=-="
        #print "NumGames: ", i["numGames"]
        #print "Win Rate: ", i["winRate"]
        #print "cd" + str(j) + " : ", i["cd" + str(j)]
        '''p = p + (i['numGames'] * i['winRate'] * i['cd' + str(j)])'''
        # if i['cd' + str(j)] != 0:
        #g = (i['cd' + str(j)] * i['winRate']) #(i['cd' + str(j)] * i['winRate'])

        if i['cd' + str(j)] != 0:
            p += (1 * i['winRate']) #(i['cd' + str(j)] * i['winRate'])
            q += 1


    if (q != 0):
        archmodel.update({"cd"+str(j): round(p/q * 100, 2)})
    else:
        print "fuck my ass"
        archmodel.update({"cd"+str(j):0})

sum = 0
for k,v in archmodel.items():
    print k, str(v) + "%"
    sum += v

print sum/30




'''
winrate of deck =  wins / losses;
winrate of card = ((wins / losses) * presence_of_card) / num_decks_card_appears
'''





