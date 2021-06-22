import numpy as np
from pandas import read_csv
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pickle

def loadData(path):
    df = read_csv(path, header=None)
    # split into input and output columns
    inputs, targets = df.values[:, :-4], df.values[:, -4:]
    # ensure all data are floating point values
    inputs = inputs.astype('float32')
    targets = targets.astype('float32')
    return (inputs,targets)

# load data of dataset and datatest
path = 'dataset.csv'
inputs,targets = loadData(path)
path = 'datatest.csv'
tests,results = loadData(path)

#Scale data for a faster learning of the NN
scaler = StandardScaler()
scaler.fit(inputs)

inputs = scaler.transform(inputs)
tests = scaler.transform(tests)
#print(inputs,tests)

#NN with adam learnig algoritm and 7 hidden layers of 1024,512,264,264,128,64 and 32 neurons respectively
clf = MLPClassifier(solver='adam', alpha=1e-6,
hidden_layer_sizes=(1024,512,264,264,128,64,32),learning_rate_init=1e-4,
max_iter=10000, random_state=2, verbose=True, validation_fraction=0.1, n_iter_no_change=2000)
clf.fit(inputs, targets)
predictData = clf.predict(tests)

#print(predictData)
#print(results)

#Print score of the NN in datatest
print(accuracy_score(results, predictData))

#save NN on file
pickle.dump(clf, open("MLPC.sav", 'wb'))
