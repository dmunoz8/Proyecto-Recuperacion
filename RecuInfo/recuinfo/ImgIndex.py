# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import rarfile
import os
import shutil
import re

#Extrae el primer archivo del directorio src, en este caso la portada en formato .jpg del comic
#Guarda esa imagen en el directorio dest, usando el nombre original del comic: normalizado

def extractFirstFile(src, dest, normalizado):
	with rarfile.RarFile(src) as rf:  #se abre el archivo src que esa en formato .cbr
		lista = rf.infolist()  #lista de todas las imagenes .jpg
		portada = lista[0].filename #.jpg que contiene la portada
		dirPadre = lista[-1].filename #Directorio que contiene las imagenes en formato jpg
		rf.extract(portada, path=dest, pwd=None)

		#Se cambia nombre de la portada
		origName = "./imgs/"+portada
		newName = "./imgs/"+dirPadre+"/"+normalizado+".jpg"
		os.rename(origName,newName)
		#Se mueven a imgs/ y se eliminan el directorio vacio
		shutil.move(newName,"./imgs")
		os.rmdir("./imgs/"+dirPadre)

#Extrae la portada de cada comic que se encuentra en formato .cbr
#Para esto recibe la ruta del directorio donde se encuentran todos los comics .cbr, y se itera en esa lista de archivos
def getComicsCovers(srcPath):
	carpetas = os.listdir(srcPath)
	for titulo in carpetas:
		for filename in os.listdir(srcPath+"/"+titulo):
			normalizado = filename[:-4]
			fullSrc = srcPath+"/"+titulo+"/"+filename
			#Una vez que se obtiene el nombre del comic se abre usando UnRar
			extractFirstFile(fullSrc,"./imgs",normalizado)

def normalizeTitles(srcPath):
	comics = os.listdir(srcPath)
	for titulo in comics:
		orig = titulo[:-4]
		vector = re.split(r'[ \-,;/\\]',orig)
		doc = "./docs/"+orig+".txt"
		try:
			file = open(doc, 'w')
			for word in vector:
				if(word != ''):
					file.write(word+"\n")
			file.close()
		except:
			print('Error escribiendo en archivo: '+doc)

if __name__ == "__main__":
	#getComicsCovers('../../Comics')
	normalizeTitles("./imgs")