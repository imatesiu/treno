#!/usr/bin/python
import httplib
import httplib2
from urllib2 import Request, urlopen
import urllib
import urllib2
import random
import time
import os
import unicodedata
import sys
import csv
from datetime import datetime
import fileinput
import re
import HTMLParser
from bs4 import BeautifulSoup

data=""

# print ""+data http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup


unicodedata.name(u'\uFB01')
unicodedata.name(u'\u0308')
unicodedata.name(u'\u2010')


def extractSchools():
	url = "scuole-specializzazione.miur.it"
	url_start_job= "/public/ssm15_cerca_scuole_graduatoria.php"
	conn = httplib.HTTPConnection(url)
	#headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
	#headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0","Cookie": "MEMGRGSRN77M53C236J=gaR6mCquBTJZ7l74t1LSREJ12vqRK1Sv","Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36", "Accept-Encoding": "gzip, deflate, sdch" , "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4", "Connection": "keep-alive"
}
	conn.request("POST", url_start_job, "", headers)
	response = conn.getresponse()
	data =response.read().decode('latin1').encode("ascii", "xmlcharrefreplace")
	conn.close()
	#p = re.compile(r'<.*?>') ris =  p.sub('', data).replace("&nbsp;"," ")
	#p = re.compile(r'\bhttp\S*?pdf\b')
	#ris =  p.findall(data)
	data1 = data.replace("&nbsp;","")
	
	return data1
	


def parsaScuole(data):
	soup = BeautifulSoup(data)
	table = soup.find_all('li')
	#rows = table.find('li')
	risultati={}
	f=0
	cols = []
	for tr in table:
		cols = tr.findAll('a')
		f+=1
		if(f>4):
			res = cols.pop()
			href = res.get("href")
			nome =  res.get_text()
			risultati[nome] = href
	return risultati


	
def contapagine(url_start_job):
	url="scuole-specializzazione.miur.it"
	#conn = httplib.HTTPConnection(url)
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding":"gzip, deflate, sdch", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36", "Accept-Encoding": "gzip, deflate, sdch" , "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4", "Connection": "keep-alive"
}
	url2 = "/public/"+url_start_job
	urrl = "http://"+url+url2
	#httplib2.debuglevel = 1
	h = httplib2.Http('.cache')
	response, content = h.request(str(urrl),"POST")
	#print response, content
	#http://scuole-specializzazione.miur.it/public/ssm15_graduatoriaAnonima.php?master=1_7
	#print response.status, response.reason
	#h.close()
	data1 = str(content).replace("&nbsp;","")
	#print response
	#print data1
	cercare = "&amp;pag="
	#Posizione = data1.find("<th colspan=\"8\" style=\"color:#ffffff; font-size:18px; font-variant:small-caps;\">")
	ris=(data1.count(cercare)+1)
	#ris2= data1[Posizione+80:Posizione+95]
	print ris
	return str(ris)
	
def parsa(data):
	soup = BeautifulSoup(data)
	table = soup.find('table')
	rows = table.findChildren(['th', 'tr'])
	risultati=[]
	f=0
	cols = []
	for y in range(10,len(rows)):
		tr = rows[y]
		cols = tr.find_all('td')
		risultatiScandidato=[]
		k=0
		for td in cols:
			testo = td.find_all(text=True)
			if(len(testo[0])==1):
				if (testo[0].isdigit()):
					risultatiScandidato.append(testo[0].strip())
			if(len(testo[0])>1):
				risultatiScandidato.append(testo[0].strip())
			else:
				sedi = td.find_all('span')
				if(len(sedi)>0):
					for sed in sedi:
						txt = sed.find_all(text=True)
						if(len(txt)>0):
							risultatiScandidato.append(txt[0].strip())
			if(k==6):
				risultati.append(risultatiScandidato)
				risultatiScandidato=[]
			k+=1
	return risultati	
	
def trasformaArrayinCSVR(matrix):
	out = ""
	out += "Posizione;Punti Titoli;Punti I Parte;Punti II Parte Area;Punti II Parte Scuola;Punti totale;Sedi scelte\r\n"
	for righe in matrix:
		i=0
		for elemento in righe:
			elemento = elemento.encode('utf-8')
			if(i<len(righe)-1):
				out+=(elemento+";")
			else:
				out+= elemento+"\n"
				#exit(0)
			i+=1
	return out
	
#Scuole = ["Allergologia+immunologia+clinica","Anatomia+Patologica","Anestesia","Audiologia","Biochimica","Chirurgia+generale","Geriatria","Ginecologia+e+ostetricia","Igiene+e+medicina+preventiva","Medicina+interna","Radiodiagnostica"]
#idscuole = ["1","2","3","4","5","9","21","22","23","30","48"]	
#pag = [2,4,41,1,1,25,15,24,15,28,42]


def generaScuole(url2,page):
	url="scuole-specializzazione.miur.it"
	urlj = "/public/"+url2
	urrl = "http://"+url+urlj
	h = httplib2.Http('.cache')
	response, content = h.request(str(urrl)+"&pag="+str(page),"POST")
	return str(content)


res = parsaScuole(extractSchools())
for key in res:
	print key
	url =  res[key]
	pag = contapagine(url)
	result_p =[]
	for x in range(1,int(pag)):
		try:
			out =  generaScuole(url,x)	
			result_p += parsa(out)
		except IndexError:
			print "Oops! Non era un numero valido. Ritenta..."
	result =  trasformaArrayinCSVR(result_p)
	out_file = open(key+".csv","w")
	out_file.write(result)
	out_file.close()

exit(0)	
for i in range(1,61):
	result_p = []
	res = contapagine(i)
	pag=res[0]
	nomescuola=res[1]
	
	print "ok"+nomescuola
	if nomescuola.count("\r")>=1:
		nomescuola= nomescuola.replace("\r","")
	if nomescuola.count("\n")>=1:
		nomescuola= nomescuola.replace("\n","")
	if nomescuola.count("/")>=1:
		omescuola= nomescuola.replace("/","")
	if nomescuola.count(">")>=1:
		omescuola=nomescuola.replace(">","")
	if nomescuola.count("<")>=1:
		omescuola=nomescuola.replace("<","")
	out_file = open(nomescuola+".csv","w")
	out_file.write(result)
	out_file.close()