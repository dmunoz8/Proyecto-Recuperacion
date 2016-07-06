import math
import operator
import string
from nltk.corpus import stopwords
from nltk import PorterStemmer
import glob

class Index:
    indextxt = dict()
    def __init__( self, norm = ".", docs = "." ):
        # guarda nombres de directorios donde se encuentran carpetas norm y docs
        self.snorm = norm
        self.sdocs = docs
        # obtiene archivos normalizados y de documentos
        self.norm = glob.glob(norm+"/*.txt")
        self.docs = glob.glob(docs+"/*.*")
        #self.imgs = glob.glob("/*.jpg")
        # guarda n
        self.n = len(self.norm)

        
    def create(self):
        # calcula el índice de los documentos
        self.indextxt = self.createIndexTxt(self.norm)
        self.calcWeight()
        self.normcIndex()
        #self.indeximg = normcIndex(calcWeight(createIndexImg(self.imgs), self.n))
        self.save()
        
        
    #Crea el indice con las palabras ya normalizadas originadas por Scrapy. El indice devuelto contiene los tf's
    def createIndexTxt(self, files):
        #Itera sobre cada archivo
        for fname in files:
            self.addToIndexTxt(fname)
        #Devuelve el indice creado
        return self.indextxt 

    #Agrega el documento @fname al indice @self.indextxt con solo los tf's
    def addToIndexTxt(self, fname):
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
                if token in self.indextxt:
                    #Si ya esta
                    if id in self.indextxt[token]:
                        #Si el documento ya lo tenia, le suma
                        self.indextxt[token][id] += 1
                    else:
                        #Si el documento no lo tenia, coloca el primero
                        self.indextxt[token][id] = 1
                else:
                    #Si no estaba, agrega la entrada al indice
                    tokenmap = dict()
                    tokenmap[id] = 1
                    self.indextxt[token] = tokenmap 

    #Calcula los pesos tf-idf del indice @self.indextxt que contiene los tf's recorriendo el mismo. Devuelve el indice con los pesos tf-idf
    def calcWeight(self):
        windextxt = dict()
        for token,tokenmap in self.indextxt.items():
            windextxt[token] = dict()
            for id, count in tokenmap.items():
                windextxt[token][id] = Index.calcTfIdf(len(self.indextxt[token]), count, self.n)
        self.index = windextxt
        return windextxt

    #Calcula los pesos tf-idf con el valor df @df y el valor tf @count.
    @staticmethod
    def calcTfIdf(df, count, n):
        tf = 1+math.log(count,10)
        idf = math.log(n/df, 10)
        return tf*idf

    def sumcDocs(self):
        sumDict = dict()
        for token,tokenmap in self.indextxt.items():
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
        for token,tokenmap in self.indextxt.items():
            normTokenmap = dict()
            for id, weight in tokenmap.items():
                weight = weight/sumDict[id]
                normTokenmap[id] = weight
            normIndex[token] = normTokenmap    

        return normIndex

    #Guarda el indice @self.indextxt recibido como argumento en el archivo llamado @fname
    def save(self, fname = "./indextxt.dat"):
        with open(fname, "w+") as file:
            for token, tokenmap in self.indextxt.items():
                line = token+":"
                for id, count in tokenmap.items():
                    line += id + "=" + str(count) + ","
                line = line[:-1]
                #print (line)
                line += "\n"
                file.write(line)

    #Carga el indice guardado en el archivo llamado @fname y lo devuelve
    def load(self, fname = "./indextxt.dat"):
        self.indextxt = dict()
        with open(fname) as file:
            content = file.readlines()
            for line in content:
                keyvalued = line.split(":")
                tokenmap = dict()
                ids = keyvalued[1].split(",")
                for id in ids:
                    vals = id.split("=")
                    tokenmap[vals[0]] = float(vals[1])
                self.indextxt[keyvalued[0]] = tokenmap
        return self.indextxt

    def calcCosinesDists(self, queryDict):
        qisdis = dict()
        for token in queryDict:
            if token in self.indextxt:
                for id in self.indextxt[token]:
                    if id in qisdis:
                        qisdis[id] += queryDict[token]*self.indextxt[token][id]
                    else:
                        qisdis[id] = queryDict[token]*self.indextxt[token][id]
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
            if token in self.indextxt:
                queryDict[token] = Index.calcTfIdf(len(self.indextxt[token]), count[token], self.n)
            else:
                queryDict[token] = Index.calcTfIdf(1, count[token], self.n)
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
