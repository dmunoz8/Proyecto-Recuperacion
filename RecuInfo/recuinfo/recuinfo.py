# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import time
import glob
import math
import operator
import string
import nltk
from nltk.corpus import stopwords
from nltk import PorterStemmer

#Crea el indice con las palabras ya normalizadas originadas por Scrapy. El indice devuelto contiene los tf's
def createIndex(files):
    #Crea indice vacio
    index = dict()
    #Itera sobre cada archivo
    for fname in files:
        addToIndex(index,fname)
    #Devuelve el indice creado
    return index 

#Agrega el documento @fname al indice @index con solo los tf's
def addToIndex(index, fname):
    #Abre el archivo
    with open(fname) as f:
        #Obtiene el identificador (nombre) del documento
        listFname = fname.split("/")
        id=listFname[-1]
        #Obtiene tokens
        content = f.readlines()
        for token in content:
            #Elimina fin de linea
            token = token.replace("\n","")
            #Agrega al indice el token
            if token in index:
                #Si ya esta
                if id in index[token]:
                    #Si el documento ya lo tenia, le suma
                    index[token][id] += 1
                else:
                    #Si el documento no lo tenia, coloca el primero
                    index[token][id] = 1
            else:
                #Si no estaba, agrega la entrada al indice
                tokenmap = dict()
                tokenmap[id] = 1
                index[token] = tokenmap 

#Calcula los pesos tf-idf del indice @index que contiene los tf's recorriendo el mismo. Devuelve el indice con los pesos tf-idf
def calcWeight(index, n):
    windex = dict()
    for token,tokenmap in index.items():
        windex[token] = dict()
        for id, count in tokenmap.items():
            windex[token][id] = calcTfIdf(len(index[token]), count, n)
    return windex

#Calcula los pesos tf-idf con el valor df @df y el valor tf @count.
def calcTfIdf(df, count, n):
    tf = 1+math.log(count,10)
    idf = math.log(n/df, 10)
    return tf*idf

def sumcDocs(index):
    sumDict = dict()
    for token,tokenmap in index.items():
        for id, weight in tokenmap.items():
            if id not in sumDict:
                sumDict[id] = weight **2
            else:
                sumDict[id] += weight **2
    for id in sumDict:
        sumDict[id] = math.sqrt(sumDict[id])
    return sumDict

def sumeDocs(index):
    sumDict = dict()
    for token,tokenmap in index.items():
        for id, weight in tokenmap.items():
            if id not in sumDict:
                sumDict[id] = weight 
            else:
                sumDict[id] += weight 
    return sumDict

def normcIndex(index):
    normIndex = dict()
    sumDict = sumcDocs(index)
    for token,tokenmap in index.items():
        normTokenmap = dict()
        for id, weight in tokenmap.items():
            weight = weight/sumDict[id]
            normTokenmap[id] = weight
        normIndex[token] = normTokenmap    
        
    return normIndex

def normeIndex(index):
    normIndex = dict()
    sumDict = sumeDocs(index)
    for token,tokenmap in index.items():
        normTokenmap = dict()
        for id, weight in tokenmap.items():
            weight = weight/sumDict[id]
            normTokenmap[id] = weight
        normIndex[token] = normTokenmap    
        
    return normIndex
    

#Guarda el indice @index recibido como argumento en el archivo llamado @fname
def saveIndex(index, fname):
    with open(fname, "w+") as file:
        for token, tokenmap in index.items():
            line = token+":"
            for id, count in tokenmap.items():
                line += id + "=" + str(count) + ","
            line = line[:-1]
            #print (line)
            line += "\n"
            file.write(line)
 
#Carga el indice guardado en el archivo llamado @fname y lo devuelve
def loadIndex(fname):
    index = dict()
    with open(fname) as file:
        content = file.readlines()
        for line in content:
            keyvalued = line.split(":")
            tokenmap = dict()
            ids = keyvalued[1].split(",")
            for id in ids:
                vals = id.split("=")
                tokenmap[vals[0]] = float(vals[1])
            index[keyvalued[0]] = tokenmap
    return index

def calcCosinelDists(queryDict, index):
    docDists = dict()
    qisdis = dict()
    sqdis = dict()
    sqqi = 0
    for token in queryDict:
        sqqi += queryDict[token]**2 
        if token in index:
            for id in index[token]:
                if id in qisdis:
                    qisdis[id] += queryDict[token]*index[token][id]
                    sqdis[id] += index[token][id]**2
                else:
                    qisdis[id] = queryDict[token]*index[token][id]
                    sqdis[id] = index[token][id]**2
    sqqi = math.sqrt(sqqi)
    for id in sqdis:
        sqdis[id] = math.sqrt(sqdis[id])
        docDists[id] = qisdis[id] / sqqi * sqdis[id]
    return docDists 

def calcCosinesDists(queryDict, index):
    qisdis = dict()
    for token in queryDict:
        if token in index:
            for id in index[token]:
                if id in qisdis:
                    qisdis[id] += queryDict[token]*index[token][id]
                else:
                    qisdis[id] = queryDict[token]*index[token][id]
    return qisdis    

def calcDists(query, index, n):
    #Elimina signos de puntuacion
    exclude = set(string.punctuation)
    query = ''.join(ch for ch in query if ch not in exclude) 
    tokens = query.split()
    i = 0
    for t in tokens:
        if t.isalnum():
            tokens[i] = PorterStemmer().stem_word(t)
            i += 1
    #Obtiene stopwords con la misma codificacion
    sws = []
    for sw in stopwords.words("english"):
        sws = sws + [sw.encode(encoding='UTF-8',errors='strict')]
    #Elimina stopwords
    for token in tokens:
        if token in sws:
            tokens.remove(token)
    count = dict()
    queryDict = dict()
    wsum = 0
    for token in tokens:
        if token in count:
            count[token] += 1
        else:
            count[token] = 1
        if token in index:
            queryDict[token] = calcTfIdf(len(index[token]), count[token], n)
        else:
            queryDict[token] = calcTfIdf(1, count[token], n)
        wsum += queryDict[token] **2
    wsum = math.sqrt(wsum)
    for token in queryDict:
        queryDict[token] = queryDict[token] / wsum
    #return calcCosinelDists(queryDict, index)
    return calcCosinesDists(queryDict, index)

def calcOrderedDists(query, index, n):
    dists = calcDists(query, index, n)
    return sorted(dists.items(), key=operator.itemgetter(1), reverse=True)

#Metodo principal del proyecto
if __name__ == "__main__":
    files = glob.glob("../recuscrapy/norm/*.txt")
    n = len(files)
    print("Cantidad de documentos: ")
    print(" "+str(n))
    indexFname = "index.dat"
    inicio = time.time()
    index = normcIndex(calcWeight(createIndex(files), n))
    #index = normeIndex(calcWeight(createIndex(files), n))
    fin = time.time()
    total = fin - inicio
    print("Duracion de creacion de indice normalizado (metodo 1): ")
    print(" "+str(total))

    saveIndex(index, indexFname)
    index = loadIndex(indexFname)
    print("Cantidad de terminos: ")
    print(" "+str(len(index)))
    print("Indice tf-idf normalizados: ")
    print(" "+str(index))
    q = "differences between computer science and informatics"
    dists = calcOrderedDists(q, index, n)
    print("Resultado de consulta: \""+q+"\":")
    print(" "+str(dists))
    
from tkinter import *
from tkinter import ttk

def query(*args):
    try:
        q = squery.get()
        res = calcOrderedDists(q, index, n)
        files = []
        result.set("")
        for doc in res:
            f = "../recuscrapy/norm/"+doc[0]
            files += [f]
            result.set(result.get() + f + "\n")
            #listbox.insert(END, f)
        
    except ValueError:
        pass
    
root = Tk()
root.title("CIDR - Computing & Informatics Document Recovery")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

squery = StringVar()
result = StringVar()

ttk.Label(mainframe, text="Type your query:").grid(column=1, row=1, sticky=E)
query_entry = ttk.Entry(mainframe, width=7, textvariable=squery)
query_entry.grid(column=1, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Search!", command=query).grid(column=2, row=2, sticky=W)
ttk.Label(mainframe, textvariable=result).grid(column=1, row=3, sticky=(W, E))
#listbox = Listbox(root)
#listbox.grid(column=1, row=3, sticky=(W, E), columnspan=2)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

query_entry.focus()
root.bind('<Return>', query)

root.mainloop()