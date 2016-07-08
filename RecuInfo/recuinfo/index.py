import math
import operator
import string
from nltk.corpus import stopwords
from nltk import PorterStemmer
import glob

class Index:
    
    def __init__( self, norm = "./norm", docs = "./docs"  ):
        # guarda nombres de directorios donde se encuentran carpetas norm y docs
        self.snorm = norm
        self.sdocs = docs
        # obtiene archivos normalizados y de documentos
        self.norm = glob.glob(norm+"/*.txt")
        self.docs = glob.glob(docs+"/*.*")
        # guarda n
        self.n = len(self.norm)

        
    def create(self):
        # calcula el indice de los documentos
        self.createIndex()
        self.calcWeight()
        self.normcIndex()
        self.save()
        
        
    #Crea el indice con las palabras ya normalizadas originadas por Scrapy. El indice devuelto contiene los tf's
    def createIndex(self):
        self.index = dict()
        #Itera sobre cada archivo
        for fname in self.norm:
            self.addToIndex(fname)
        #Devuelve el indice creado
        return self.index

    #Agrega el documento @fname al indice @self.index con solo los tf's
    def addToIndex(self, fname):
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
                if token in self.index:
                    #Si ya esta
                    if id in self.index[token]:
                        #Si el documento ya lo tenia, le suma
                        self.index[token][id] += 1
                    else:
                        #Si el documento no lo tenia, coloca el primero
                        self.index[token][id] = 1
                else:
                    #Si no estaba, agrega la entrada al indice
                    tokenmap = dict()
                    tokenmap[id] = 1
                    self.index[token] = tokenmap 

    #Calcula los pesos tf-idf del indice @self.index que contiene los tf's recorriendo el mismo. Devuelve el indice con los pesos tf-idf
    def calcWeight(self):
        windex = dict()
        for token,tokenmap in self.index.items():
            windex[token] = dict()
            for id, count in tokenmap.items():
                windex[token][id] = self.calcTfIdf(len(self.index[token]), count)
        self.index = windex
        return windex

    #Calcula los pesos tf-idf con el valor df @df y el valor tf @count.
    def calcTfIdf(self, df, count):
        tf = 1+math.log(count,10)
        idf = math.log((self.n)/df, 10)
        return tf*idf

    def sumcDocs(self):
        sumDict = dict()
        for token,tokenmap in self.index.items():
            for id, weight in tokenmap.items():
                if id not in sumDict:
                    sumDict[id] = weight **2
                else:
                    sumDict[id] += weight **2
        for id in sumDict:
            sumDict[id] = math.sqrt(sumDict[id])
        return sumDict

    def normcIndex(self):
        normIndex = dict()
        sumDict = self.sumcDocs()
        for token,tokenmap in self.index.items():
            normTokenmap = dict()
            for id, weight in tokenmap.items():
                weight = weight/sumDict[id]
                normTokenmap[id] = weight
            normIndex[token] = normTokenmap    
        self.index = normIndex
        return normIndex

    #Guarda el indice @self.index recibido como argumento en el archivo llamado @fname
    def save(self, fname = "./index.dat"):
        with open(fname, "w+") as file:
            for token, tokenmap in self.index.items():
                line = token+":"
                for id, count in tokenmap.items():
                    line += id + "=" + str(count) + ","
                line = line[:-1]
                #print (line)
                line += "\n"
                file.write(line)

    #Carga el indice guardado en el archivo llamado @fname y lo devuelve
    def load(self, fname = "./index.dat"):
        self.index = dict()
        with open(fname) as file:
            content = file.readlines()
            for line in content:
                keyvalued = line.split(":")
                tokenmap = dict()
                ids = keyvalued[1].split(",")
                for id in ids:
                    vals = id.split("=")
                    tokenmap[vals[0]] = float(vals[1])
                self.index[keyvalued[0]] = tokenmap
        return self.index

    def calcCosinesDists(self, queryDict):
        qisdis = dict()
        for token in queryDict:
            if token in self.index:
                for id in self.index[token]:
                    if id in qisdis:
                        qisdis[id] += queryDict[token]*self.index[token][id]
                    else:
                        qisdis[id] = queryDict[token]*self.index[token][id]
        return qisdis    

    def calcDists(self, query):
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
            if token in self.index:
                queryDict[token] = self.calcTfIdf(len(self.index[token]), count[token])
            else:
                queryDict[token] = self.calcTfIdf(1, count[token])
            wsum += queryDict[token] **2
        wsum = math.sqrt(wsum)
        for token in queryDict:
            queryDict[token] = queryDict[token] / wsum
        return self.calcCosinesDists(queryDict)

    def calcOrderedDists(self, query):
        dists = self.calcDists(query)
        return sorted(dists.items(), key=operator.itemgetter(1), reverse=True)
    
    def query(self, query):
        return self.calcOrderedDists(query)
