import scrapy
import re
import string
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import nltk
from nltk.corpus import stopwords
from nltk import PorterStemmer

#Se debe correr la arana desde el directorio principal de la misma (donde esta el scrapy.cfg)
class MySpider(scrapy.Spider):
	name = "recuinfo"
	#Primeras 6 paginas de resultados de google de la consulta: "computing and informatics"
	start_urls = [	"https://www.google.com/search?q=computing%20and%20informatics&rct=j",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=10",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=20",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=30",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=40",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=50"
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=60",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=70",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=80",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=90",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=100",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=110",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=120",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=130",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=140",
					"https://www.google.com/search?q=computing%20and%20informatics&rct=j&start=150"]

	#Define la forma en que se obtienen y navegan los enlaces de los resultados de google
	def parse(self, response):
		hxs = Selector(response)
		google_search_links_list = hxs.xpath('//h3/a/@href').extract()
		google_search_links_list = [re.search('q=(.*)&sa',n).group(1) for n in google_search_links_list if re.search('q=(.*)&sa',n)]
		#Cada url es un resultado, se debe parsear con parse_items
		for url in google_search_links_list:
			yield scrapy.Request(url, callback=self.parse_items)

	#Define la forma en que cada resultado se parsea y se obtienen los tokens normalizados
	def parse_items(self, response):
		#Obtiene el nombre del documento
		listUrl = response.url.split("/")
		#Archivo con terminos normalizados
		normname = "norm/"+listUrl[2]+"_Computing.txt"
		#Documento original	
		docname = "docs/"+listUrl[2]+"_Computing.txt"
		#No se analizan pdf's
		if ".pdf" not in response.url:
			soup = BeautifulSoup(response.body)
			#Extrae scripts, encabezados, pies de paginas, hojas de estilos...
			for script in soup(["script", "style", "header", "footer","header-fixed"]):
				script.extract()    # rip it out
			#Elimina tags
			text = soup.get_text()
			#Elimina signos de puntuacion
			remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
			tokens=text.translate(remove_punctuation_map).encode(encoding='UTF-8',errors='strict').split()
			#Obtiene stopwords con la misma codificacion
			sws = []
			for sw in stopwords.words("english"):
				sws = sws + [sw.encode(encoding='UTF-8',errors='strict')]
			#Elimina stopwords
			for token in tokens:
				if token in sws:
					tokens.remove(token)
			#Guarda palabras normalizadas con stemming
			open(normname, 'wb').write('\n'.join(PorterStemmer().stem_word(e) for e in tokens if e.isalnum()))
			#Guarda palabras normalizadas sin stemming
			#open(normname, 'wb').write('\n'.join(e for e in tokens if e.isalnum()))
			#Guarda documento original
			open(docname, 'wb').write(BeautifulSoup(response.body).prettify().encode(encoding='UTF-8',errors='strict'))
