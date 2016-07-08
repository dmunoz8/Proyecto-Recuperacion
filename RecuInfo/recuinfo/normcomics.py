# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import rarfile
import os
import shutil
import re

#Extrae el primer archivo del directorio src, en este caso la portada en formato .jpg del comic
#Guarda esa imagen en el directorio dest, usando el nombre original del comic: normalizado
class NormComics:
	def __init__( self, srccomics = "./docs", dstnorm = "./norm", dstimgs="./imgs" ):
		self.srccomics = "./docs"
		self.dstnorm = "./norm"
		self.dstimgs = "./imgs"
    
	def extractFirstFile(self, src, normalizado):
		with rarfile.RarFile(src) as rf:  #se abre el archivo src que esa en formato .cbr
			lista = rf.infolist()  #lista de todas las imagenes .jpg
			portada = lista[0].filename #.jpg que contiene la portada
			dirPadre = lista[-1].filename #Directorio que contiene las imagenes en formato jpg
			rf.extract(portada, path=self.dstimgs, pwd=None)

			#Se cambia nombre de la portada
			origName = self.dstimgs+"/"+portada
			newName = self.dstimgs+"/"+dirPadre+"/"+normalizado+".jpg"
			os.rename(origName,newName)
			#Se mueven a imgs/ y se eliminan el directorio vacio
			shutil.move(newName,self.dstimgs)
			os.rmdir(self.dstimgs+"/"+dirPadre)

    #Extrae la portada de cada comic que se encuentra en formato .cbr
    #Para esto recibe la ruta del directorio donde se encuentran todos los comics .cbr, y se itera en esa lista de archivos
	def getComicsCovers(self, srcPath):
		imgs = os.listdir(self.dstimgs)
		for i in imgs:
			os.remove(os.path.abspath(self.dstimgs+"/"+i))
		carpetas = os.listdir(srcPath)
		for titulo in carpetas:
			for filename in os.listdir(srcPath+"/"+titulo):
				normalizado = filename[:-4]
				fullSrc = srcPath+"/"+titulo+"/"+filename
				#Una vez que se obtiene el nombre del comic se abre usando UnRar
				self.extractFirstFile(fullSrc,normalizado)

	def normalizeTitles(self):
		comics = os.listdir(self.srccomics)
		for titulo in comics:
			orig = titulo[:-4]
			vector = re.split(r'[ \-,;/\\]',orig)
			doc = "./norm/"+orig+".txt"
			try:
				file = open(doc, 'w')
				for word in vector:
					if(word != ''):
						file.write(word+"\n")
				file.close()
			except:
				print('Error escribiendo en archivo: '+doc)

