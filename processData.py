import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write,read
from scipy.fft import fft
import time
import numpy as np
import os
from grabar import record

#Hann window
def windowing(data):
    window = []
    windowData = []
    n=0
    N=len(data)
    while n < N:
        window.append(0.54 - 4.4 * np.cos((2*np.pi * n )/(N-1)))
        windowData.append(window[n] * data[n])
        n = n+1

    return windowData

#Premph filter (FIR)
def preEmphF(data):
    emph = []
    emphData = []
    n=1
    N=len(data)
    while n < N:
        emph.append(1-0.68*(1/n))
        emphData.append(emph[n-1] * data[n-1])
        n = n+1
    return emphData

#Get index in of frecuency in frecuency array
def getIndexOfFrec(F,frec):
    index = np.where(F<frec)
    return index[0][-1]

#Get bigest frecuency within a range
def getMaxFrecOnRange(data,F,rangeMin,rangeMax):
    maxMag = 0
    frec=F[rangeMin]
    i=getIndexOfFrec(F,rangeMin)
    while i<getIndexOfFrec(F,rangeMax):
        if data[i] > maxMag:
            maxMag = data[i]
            frec = F[i]
        i=i+1
    return [maxMag,int(np.ceil(frec))]

def plotData(x,y,xLabel="Eje X",yLabel="Eje Y"):
    plt.plot(x, y)
    plt.xlabel(xLabel, fontsize='14')
    plt.ylabel(yLabel, fontsize='14')
    plt.show()

#Compute the util data for clasificate
def getUtilFrec(data,F,min=20,max=5000,lenOut=5):
    frecArray = []
    magArray = []
    #Obtener la frecuencia para saber si es H o M
    frec = getMaxFrecOnRange(data,F,85,255)
    frecArray.append(frec[1])

    #Magnitud máxima de 256 a 400
    frec = getMaxFrecOnRange(data,F,256,400)
    magArray.append(np.ceil(frec[0].real))

    frec = getMaxFrecOnRange(data,F,400,600)
    magArray.append(np.ceil(frec[0].real))

    frec = getMaxFrecOnRange(data,F,601,800)
    magArray.append(np.ceil(frec[0].real))

    frec = getMaxFrecOnRange(data,F,801,1000)
    magArray.append(np.ceil(frec[0].real))

    frec = getMaxFrecOnRange(data,F,1001,1200)
    magArray.append(np.ceil(frec[0].real))

    frec = getMaxFrecOnRange(data,F,1201,1400)
    magArray.append(np.ceil(frec[0].real))

    frec = getMaxFrecOnRange(data,F,1401,1600)
    magArray.append(np.ceil(frec[0].real))

    frec = getMaxFrecOnRange(data,F,1601,3000)
    magArray.append(np.ceil(frec[0].real))

    #feed the result array with a porcentage of magnitudes regarding the bisgest
    maxMag = 0
    for mag in magArray:
        if mag > maxMag:
            maxMag=mag
    
    for mag in magArray:
        frecArray.append(int((mag/maxMag)*100))
    return frecArray

    '''
    frecArray = []
    frecArray2=[]
    i=0
    frecRange = int(np.floor((max-min)/lenOut))
    max = frecRange
    while i<lenOut:
        frecArray.append(getMaxFrecOnRange(data,F,min+(frecRange*i),max+(frecRange*i)))
        i=i+1
    
    frecArraySorted = sorted(frecArray, key=lambda x: x[0],reverse=True)
    for frec in frecArraySorted:
        frecArray2.append(frec[1])
    #print(frecArray2)

    #for frec in frecArray:
    #    frecArray2.append(frec[1])

    return frecArray2
    '''
#record("output.wav")


#Get data array
def getData(file):
    Fs,data = read(file)
    data = data[:,0]
    data = data [19000:]
    L = len(data)
    #n = np.arange(0,L)/Fs    

    #data = windowing(data)
    #data = preEmphF(data)

    dataFFT = fft(data)

    M_dataFFT = abs(dataFFT)                                   # Tomamos la Magnitud de la FFT
    M_dataFFT = M_dataFFT[0:L//2]                              # Tomamos la mitad de los datos (recordar la simetría de la transformada)

    #Ph_dataFFT = np.angle(dataFFT)
    F = Fs*np.arange(0, L//2)/L
    #print(F)
    
    #print(getMaxFrecOnRange(dataFFT,F,20,1000))                                 # Imprimimos el valor de la frecuencia dominante
    Frec = getUtilFrec(dataFFT,F,20,1500,5)
    print(Frec,file)
    #plotData(F[32:2004],M_dataFFT[32:2004],"Frecuencia (Hz) "+ file,"Amplitud")
    #plotData(F[32:7000],M_dataFFT[32:7000],"Frecuencia (Hz) "+ file,"Amplitud")

    return Frec

def encode(target):
    if target == 'AH':
        return ("0.0.0.1")
    if target == 'EH':
        return ("0.0.1.0")
    if target == 'IH':
        return ("0.0.1.1")
    if target == 'OH':
        return ("0.1.0.0")
    if target == 'UH':
        return ("0.1.0.1")
    if target == 'AM':
        return ("1.0.0.1")
    if target == 'EM':
        return ("1.0.1.0")
    if target == 'IM':
        return ("1.0.1.1")
    if target == 'OM':
        return ("1.1.0.0")
    if target == 'UM':
        return ("1.1.0.1")

def decodeStr(cad):
    if cad == '0001':
        return ("Hombre -> A")
    if cad == '0010':
        return ("Hombre -> E")
    if cad == '0011':
        return ("Hombre -> I")
    if cad == '0100':
        return ("Hombre -> O")
    if cad == '0101':
        return ("Hombre -> U")
    if cad == '1001':
        return ("Mujer -> A")
    if cad == '1010':
        return ("Mujer -> E")
    if cad == '1011':
        return ("Mujer -> I")
    if cad == '1100':
        return ("Mujer -> O")
    if cad == '1101':
        return ("Mujer -> U")
    else:
        return cad

def decodeRes(res):
    res = res[0]
    cad = ""
    for num in res:
        cad=cad+str(num)
    print(res)
    return(decodeStr(cad))

def getFiles(directory):
    dir= directory+'/'
    fileName = directory+".csv"

    fp = open(fileName,'w')

    aux = []
    content = os.listdir(dir)
    content = sorted(content)

    for file in content:        
        #if file[0:2] == "AM":
        if True:
            pathFile = dir+str(file)
            aux = getData(pathFile)
            clase = encode(file[0:2]).split('.')
            for num in clase:
                aux.append(num)
            lst_new = [str(a) for a in aux]
            auxStr = "," . join(lst_new)
            fp.write(auxStr+"\n")
    fp.close()


#getFiles("dataset")
#getFiles("datatest")

#Fs,data = read('output.wav')
#data = data[:,0]
#data = data [19000:]
#L = len(data)
#n = np.arange(0,L)/Fs
#
##Plot Audio
##plotData(n,data,"Tiempo (s)","Magnitud")
#
#windowingData = windowing(data)
#
## Compute the FFT
#dataFFT = fft(data)
#
#M_dataFFT = abs(dataFFT)                                   # Tomamos la Magnitud de la FFT
#M_dataFFT = M_dataFFT[0:L//2]                              # Tomamos la mitad de los datos (recordar la simetría de la transformada)
#
#Ph_dataFFT = np.angle(dataFFT)
#F = Fs*np.arange(0, L//2)/L
#
##print(F)
##plotData(F,M_dataFFT,"Frecuencia (Hz)","Amplitud")
#
##print(getMaxFrecOnRange(dataFFT,F,20,1000))                                 # Imprimimos el valor de la frecuencia dominante
#Frec = getUtilFrec(dataFFT,F)
#
#