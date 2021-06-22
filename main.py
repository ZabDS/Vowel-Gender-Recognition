from grabar import record
from processData import getData,decodeRes
from pandas import read_csv
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import pickle

def loadData(path):
    df = read_csv(path, header=None)
    # split into input and output columns
    inputs, targets = df.values[:, :-4], df.values[:, -4:]
    # ensure all data are floating point values
    inputs = inputs.astype('float32')
    targets = targets.astype('float32')
    return (inputs,targets)

# load the dataset for train the scaler
path = 'dataset.csv'
inputs,targets = loadData(path)

#Train the scaler
scaler = StandardScaler()
scaler.fit(inputs)

#Transform the input data for the NN
record("output.wav")
input = getData("output.wav")
input = scaler.transform([input])

#Load the NN
mlp = pickle.load(open("MLPC.sav","rb"))
#Input data to NN and get response
res=mlp.predict(input)
#print(Response of NN)
print(decodeRes(res))
