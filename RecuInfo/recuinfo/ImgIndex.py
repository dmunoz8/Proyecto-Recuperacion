# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import rarfile
import os
import shutil

def extractFirstFile(src, dest, titulo, normalizado):
	with rarfile.RarFile(src) as rf:
		lista = rf.infolist()
		portada = lista[0].filename #.jpg que contiene la portada
		dirPadre = lista[-1].filename
		rf.extract(portada, path=dest, pwd=None)
		#Se cambia nombre de la portada
		origName = "./imgs/"+portada
		newName = "./imgs/"+dirPadre+"/"+normalizado+".jpg"
		os.rename(origName,newName)
		shutil.move(newName,"./imgs")
		os.rmdir("./imgs/"+dirPadre)

def getComicsCovers(srcPath):
	carpetas = os.listdir(srcPath)
	for titulo in carpetas:
		for filename in os.listdir(srcPath+"/"+titulo):
			normalizado = filename[:-4]
			fullSrc = srcPath+"/"+titulo+"/"+filename
			extractFirstFile(fullSrc,"./imgs",titulo,normalizado)

		print(titulo+"/ procesado...")

if __name__ == "__main__":
	getComicsCovers('../../Comics')