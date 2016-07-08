import math
import operator
import string
from nltk.corpus import stopwords
from nltk import PorterStemmer
from descriptorimg import DescriptorImg
import glob

class ComicIndex:
    def __init__( self, norm = "./norm", docs = "./docs", imgs="./imgs" ):
        # guarda nombres de directorios donde se encuentran carpetas norm y docs
        self.snorm = norm
        self.sdocs = docs
        self.simgs = imgs
        # obtiene archivos normalizados y de documentos
        self.norm = glob.glob(norm+"/*.txt")
        self.docs = glob.glob(docs+"/*.*")
        self.imgs = glob.glob(imgs+"/*.jpg")
        # guarda n
        self.n = len(self.docs)
        # inicializa índices
        self.indextxt = dict()
        self.indeximg = dict()
        # inicializa descriptor
        self.descriptor = DescriptorImg((7,11,3))

        
    def create(self):
        # calcula el índice de los documentos
        self.createIndexTxt()
        self.createIndexImg()
        self.save()
        
     #Crea el indice con las palabras ya normalizadas originadas por Scrapy. El indice devuelto contiene los tf's
    def createIndexImg(self):
        self.indeximg = dict()
        #Itera sobre cada archivo
        for fname in self.imgs:
            self.addToIndexImg(fname)
        #Devuelve el indice creado
        return self.indeximg 

    #Agrega el documento @fname al indice @self.indextxt con solo los tf's
    def addToIndexImg(self, fname):
        listFname = fname.split("\\")
        id=listFname[-1]
        idext=id.split(".")
        id=idext[0]
        caracts = self.descriptor.describe(fname)
        self.indeximg[id] = caracts
        
    #Crea el indice con las palabras ya normalizadas originadas por Scrapy. El indice devuelto contiene los tf's
    def createIndexTxt(self):
        self.indextxt = dict()
        #Itera sobre cada archivo
        for fname in self.norm:
            self.addToIndexTxt(fname)
        #Devuelve el indice creado
        self.calcWeight()
        self.normcIndex()
        return self.indextxt 

    #Agrega el documento @fname al indice @self.indextxt con solo los tf's
    def addToIndexTxt(self, fname):
        #Abre el archivo
        with open(fname) as f:
            #Obtiene el identificador (nombre) del documento
            listFname = fname.split("\\")
            id=listFname[-1]
            idext=id.split(".")
            id=idext[0]
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
                windextxt[token][id] = self.calcTfIdf(len(self.indextxt[token]), count)
        self.indextxt = windextxt
        return windextxt

    #Calcula los pesos tf-idf con el valor df @df y el valor tf @count.
    def calcTfIdf(self, df, count):
        tf = 1+math.log(count,10)
        idf = math.log((self.n)/df, 10)
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
        self.indextxt = normIndex
        return normIndex

    #Guarda el indice @self.indextxt recibido como argumento en el archivo llamado @fname
    def save(self, ftxt = "./indextxt.dat", fimg = "./indeximg.dat"):
        with open(ftxt, "w+") as file:
            for token, tokenmap in self.indextxt.items():
                line = token+":"
                for id, count in tokenmap.items():
                    line += id + "=" + str(count) + ","
                line = line[:-1]
                #print (line)
                line += "\n"
                file.write(line)
        with open(fimg, "w+") as file:
            for id, features in self.indeximg.items():
                line = id+":"
                for f in features:
                    line += str(f) +","
                line = line[:-1]
                line += "\n"
                file.write(line)

    #Carga el indice guardado en el archivo llamado @fname y lo devuelve
    def load(self, ftxt = "./indextxt.dat", fimg = "./indeximg.dat"):
        self.indextxt = dict()
        with open(ftxt) as file:
            content = file.readlines()
            for line in content:
                keyvalued = line.split(":")
                tokenmap = dict()
                ids = keyvalued[1].split(",")
                for id in ids:
                    vals = id.split("=")
                    tokenmap[vals[0]] = float(vals[1])
                self.indextxt[keyvalued[0]] = tokenmap
        with open(fimg) as file:
            content = file.readlines()
            for line in content:
                idfeats = line.split(":")
                feats = idfeats[1].split(",")
                ffeats = [float(i) for i in feats]
                self.indeximg[idfeats[0]] = ffeats

    def calcCosinesDistsTxt(self, queryDict):
        qisdis = dict()
        for token in queryDict:
            if token in self.indextxt:
                for id in self.indextxt[token]:
                    if id in qisdis:
                        qisdis[id] += queryDict[token]*self.indextxt[token][id]
                    else:
                        qisdis[id] = queryDict[token]*self.indextxt[token][id]
        return qisdis  
    
    def calcCosinesDistsImg(self, queryCaracts):
        qisdis = dict()
        for id, caracts in self.indeximg.items():
            i = 0;
            for c in caracts:
                if id in qisdis:
                    qisdis[id] += queryCaracts[i]*c
                    i += 1
                else:
                    qisdis[id] = queryCaracts[i]*c
                    i += 1
                    
        return qisdis  

    def calcDistsTxt(self, query):
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
                queryDict[token] = self.calcTfIdf(len(self.indextxt[token]), count[token])
            else:
                queryDict[token] = self.calcTfIdf(1, count[token])
            wsum += queryDict[token] **2
        wsum = math.sqrt(wsum)
        for token in queryDict:
            queryDict[token] = queryDict[token] / wsum
        return self.calcCosinesDistsTxt(queryDict)
    
    def calcDistsImg(self, query):
        caracts = self.descriptor.describe(query)
        return self.calcCosinesDistsImg(caracts)

    def calcOrderedDistsTxt(self, query):
        dists = self.calcDistsTxt(query)
        return sorted(dists.items(), key=operator.itemgetter(1), reverse=True)
    
    def calcOrderedDistsImg(self, query):
        dists = self.calcDistsImg(query)
        sortd =  sorted(dists.items(), key=operator.itemgetter(1), reverse=True)
        return sortd
    
    def queryTxt(self, query):
        return self.calcOrderedDistsTxt(query)
    
    def queryImg(self, query):
        return self.calcOrderedDistsImg(query)
