# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import rarfile
import os

def extractFirstFile(src, dest):
	with rarfile.RarFile(src) as rf:
		portada = rf.infolist()[0].filename
		rf.extract(portada, path=dest, pwd=None)  


def getComicsCovers(srcPath):
	carpetas = os.listdir(srcPath)
	for titulo in carpetas:
		for filename in os.listdir(srcPath+"/"+titulo):
			extractFirstFile(srcPath+"/"+titulo+"/"+filename,"./imgs")
		print(titulo+"/ procesado...")

if __name__ == "__main__":
	getComicsCovers('../../Comics')