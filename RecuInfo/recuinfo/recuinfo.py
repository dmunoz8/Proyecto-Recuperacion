# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import time

from index import Index
from comicindex import ComicIndex

#Metodo principal del proyecto
if __name__ == "__main__":
    index = ComicIndex("../recuscrapy/norm","../recuscrapy/docs")
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
    q = "./imgs/Marvel-comic-heroes-cover-014.jpg"
    res = index.queryImg(q)
    print("Resultado de consulta: \""+q+"\":")
    print(" "+str(res))


from tkinter import *
from tkinter import ttk

def query(*args):
    try:
        q = squery.get()
        res = index.query(q)
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

mainframe = ttk.Frame(root, padding="40 40 40 40")
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
listbox = Listbox(root)
listbox.grid(column=6, row=0,columnspan=2)

listbox.insert(END, "a list entry")

for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

query_entry.focus()
root.bind('<Return>', query)

root.mainloop()
