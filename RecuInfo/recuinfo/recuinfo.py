# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import time

from index import Index
from comicindex import ComicIndex

#Metodo principal del proyecto
if __name__ == "__main__":
    index = ComicIndex()
    inicio = time.time()
    index.create()
    fin = time.time()
    total = fin - inicio
    print("Duracion de creacion de indice normalizado (metodo 1): ")
    print(" "+str(total))
    #index.load()
    
    print("Cantidad de terminos: ")
    print(" "+str(len(index.indextxt)))
    print("Indice tf-idf normalizados: ")
    print(" "+str(index.indextxt))
    q = "video games development"
    res = index.queryTxt(q)
    print("Resultado de consulta: \""+q+"\":")
    print(" "+str(res))
    
    print("Cantidad de imagenes: ")
    print(" "+str(len(index.indeximg)))
    print("Indice de imagenes normalizado: ")
    print(" "+str(index.indeximg))
    q = "./imgs/Batman Vol2 00.jpg"
    res = index.queryImg(q)
    print("Resultado de consulta: \""+q+"\":")
    print(" "+str(res))


from tkinter import *
from tkinter import ttk
import webbrowser
from PIL import Image,ImageTk
	 
def show_image(selection):
    image = Image.open("C:\\Users\\Marco\\Downloads\\Proyecto Recuperacion\\Proyecto-Recuperacion\\RecuInfo\\recuinfo\\imgs\\Marvel-comic-heroes-cover-014.jpg") #listbox.get(ACTIVE))
    image.show()
    
def querytxt(*args):
    try:
        q = squerytxt.get()
        res = index.queryTxt(q)
        files = []
        listbox.delete(0, END)
        for doc in res:
            f = "./docs/"+doc[0]
            files += [f]
            listbox.insert(END, f)
        
    except ValueError:
        pass
    
def queryimg(*args):
    try:
        q = squeryimg.get()
        res = index.queryImg(q)
        files = []
        listbox.delete(0, END)
        for doc in res:
            f = "./docs/"+doc[0]
            files += [f]
            listbox.insert(END, f)
        
    except ValueError:
        pass
    
    
root = Tk()
root.title("CDR - Comics Document Recovery")

mainframe = ttk.Frame(root, padding="40 40 40 40")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

squerytxt = StringVar()
squeryimg = StringVar()

ttk.Label(mainframe, text="Type your query:").grid(column=0, row=0, sticky=E)
query_entry = ttk.Entry(mainframe, width=20, textvariable=squerytxt)
query_entry.grid(column=1, row=0, rowspan=2, columnspan=2)
ttk.Button(mainframe, text="Search Text!", command=querytxt).grid(column=6, row=0, sticky=W)

ttk.Label(mainframe, text="Type your path for image").grid(column=0, row=2, sticky=E)
query_entry = ttk.Entry(mainframe, width=20, textvariable=squeryimg)
query_entry.grid(column=1, row=2, rowspan=2, columnspan=2)
ttk.Button(mainframe, text="Search Image!", command=queryimg).grid(column=6, row=2, sticky=W)

#ttk.Label(mainframe, textvariable=result).grid(column=1, row=3, sticky=(W, E))
listbox = Listbox(root, width=60)
listbox.grid(column=0, row=3, columnspan=5)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

query_entry.focus()
listbox.bind("<Double-Button-1>",show_image)
root.bind('<Return>', querytxt)

root.mainloop()