import csv
import numpy as np
import operator
import copy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn import svm
from sklearn.cluster import KMeans

X = []         # Features/Cards of each deck
Y = []         # Class labels/Archetype ID's of each deck for use in SVM Archetype prediction
Z = []         # Class labels/Winrates of each deck for use in KMeans winrate prediction
data = []
count = 0;
splitData = 0.9


with open('data.csv', 'rb') as csvfile:     # Read in dataset from csv
    reader = csv.reader(csvfile)
    for row in reader:
        if count == 0:                      # Will skip first row, which is the column names: Winrate Archetype_ID Card_ID1 CardID_2 ...
            count +=1
            continue

        data.append(row)

for row in data:
    X.append(row[2:])               # Grab Cards for each deck and store in X
    Y.append(row[1])                # Grab Archetype ID of each deack and store in Y
    Z.append(row[0])                # Grab Winrate of Each deck and store in Z

X = np.array(X).astype(np.int)      # Convert to np.arrays for use in sklearn models
Y = np.array(Y)
Z = np.array(Z).astype(np.float)

unique = {}     # Create/set Dictionary to keep track of all the unique archetypes
for i in Y:
    if i not in unique:
        unique[i] = 1
    else:
        unique[i] += 1

counts = copy.deepcopy(unique)   # Deep copy dictionary for splitting datset into training data and test data

for k,v in counts.items():       # Set counts dictionary for splitting datset
    counts[k] = 0;

                    # Create lists for containing split data
X_Train = []        # Cards
Y_Train = []        # Archetypes
Z_Train = []        # Winrates

X_Test = []         # Cards
Y_Test = []         # Archetypes
Z_Test = []         # Winrates


for i in range(0, len(X)):                            # Goal here is to use a certain percent of data set
    if counts[Y[i]] > (unique[Y[i]] * splitData):           # for Training, and rest for Testing each model
        X_Test.append(X[i])
        Y_Test.append(Y[i])
        Z_Test.append(Z[i])
    else:
        X_Train.append(X[i])
        Y_Train.append(Y[i])
        Z_Train.append(Z[i])
        counts[Y[i]] += 1

X_Train = np.array(X_Train)             # Decks to Train models
Y_Train = np.array(Y_Train)             # Archetypes to Train SVM model
Z_Train = np.array(Z_Train)             # Winrates to train KMeans model

X_Test = np.array(X_Test)               # Decks to Test models
Y_Test = np.array(Y_Test)               # Archetypes of each deck, will compare with predicted archetypes of SVM
Z_Test = np.array(Z_Test)               # Winrates of each deck, will compare with predicted winrates from KMeans

print "=-=-=-=-=-=-=-=-=-=-= Creating and Training SVM Model ==-=-=-=-=-=-=-=-=-=-=-=\n"
sv = svm.LinearSVC()                    # Create SVM model
sv.fit(X_Train, Y_Train)                # Train model using date from splitting data set

predicted = sv.predict(X_Test)                           # Test SVM model using data from splitting dataset
numDecks = X_Test.shape[0]                               # Get number of decks used to Test model
numMissed = (Y_Test != predicted).sum()                  # Get number of mislabels by comparing predicted labels with actual labels
accuracy = float(numDecks-numMissed)/float(numDecks)     # Get overall accuracy of model

print "=-=-=-=-=-=-=-=-=-=-= Printing information of SVM Model =-=-=-=-=-=-=-=-=-=-=-="
print "Number of Decks: %d\nNumber of Mislabeled: %d\nAccuracy: %f" % (numDecks, numMissed, accuracy)
print "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

print "\n\n=-=-=-=-=-=-=-=-= Creating Graph of SVM Prediction vs Actual =-=-=-=-=-=-=-=-=-="
plt.figure(1)                                               # Create Graph to compare actual archetypes with predicted Archetypes from SVM
t = np.linspace(0, len(X_Test), len(X_Test))
plt.plot(t, Y_Test, 'r', label="Actual")                    # Plot actual
plt.plot(t, predicted, 'b', label="Predicted")              # Plot predicted
plt.title("SVM Predicted Archetypes vs. Actual Archetypes")
plt.xlabel("Deck ID")
plt.ylabel("Archetype ID")
plt.legend()
plt.savefig('Graphs/SVM')                                          # Save graph to file called 'SVM'
print "=-=-=-=-=-=-=-=-=-= Graph Created and saved as 'SVM.png' =-=-=-=-=-=-=-=-=-=-=-="


print "\n=-=-=-=-=-=-=-=-=-=-= Creating and Training KMeans Model ==-=-=-=-=-=-=-=-=-=-=-=\n"
kmeans = KMeans(n_clusters=len(unique), random_state=0)     # Create KMeans model, number of clusters=number of unique archetypes
kmeans.fit(X_Train)                                         # Train Model
labels = kmeans.labels_                                     # Obtain labels of each cluster
predicted = kmeans.predict(X_Test)                          # Test model

A = []          # Will hold actual winrates of decks for use of plotting on graph
P = []          # Will hold predicted winrate of decks for us of plotting on graph

for j in range(0, len(predicted)):              # Iterate through each predicted winrate
    cluster = []
    for i in range(0, len(labels)):             # Iterate through labels of clusters
        if labels[i] == predicted[j]:           # If the label is equal to predicted label, then found point in same cluster
            cluster.append(Z_Train[i])          # Add winrate from same cluster as predicted

    prediction = 100.0;
    distance = 100.0;
    for i in cluster:                           # Iterate through cluster to find the closest point to the predicted deck
        if abs(i - Z_Test[j]) < distance:       # If new shortest distance found
            distance = abs(i - Z_Test[j])       # Update the shortest distance
            prediction = i                      # Update the predicted wirnate to match deck closest to predicted deck

    P.append(prediction)                        # Add predicted winrate for use of plotting
    A.append(Z_Test[j])                         # Add actual winrate for use of plotting

print "\n\n=-=-=-=-=-=-=-=-= Creating Graph of KMeans Prediction vs Actual =-=-=-=-=-=-=-=-="
plt.figure(2)                                   # Create graph for KMeans model
t = np.linspace(0, len(X_Test), len(X_Test))
plt.plot(t, A, 'r', label="Actual")             # Plot Actual
plt.plot(t, P, 'b', label="Predicted")          # plot predicted
plt.title("KMeans Actual Winrate vs. Predicted Winrate")
plt.xlabel("Deck ID")
plt.ylabel("Winrate in %")
plt.legend()
plt.savefig('Graphs/KMeans')                           # Save graph to file called 'KMeans'
print "=-=-=-=-=-=-=-=-=-= Graph Created and saved as 'KMeans.png' =-=-=-=-=-=-=-=-=-=-="
print "\n\n=-=-=-=-=-=-=-=-= Graphs saved and stored in Graphs directory =-=-=-=-=-=-=-=-=-=\n\n"


