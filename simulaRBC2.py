#!/usr/bin/python
import random
import time
import os
import sys
import csv
from datetime import datetime
import fileinput
import socket
import re
import thread
from array import array
import messaggi
import xmlconfReader

receive_UDP_IP = "127.0.0.1"  #ASCOLTO TRENI
UDP_PORT = 1111
confitinerari = "ConfigurazioneItinerari.xml"
	
def date_key(row):
    return datetime.strptime(row[2].strip(), "%d-%m-%Y %H:%M")

   
def sendUDP(message, _UDP_PORT):
	UDP_IP = "192.168.1.213" #send IP ATS
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.sendto( message, (UDP_IP, _UDP_PORT))

def sendTCP(MESSAGE):
	TCP_IP = "127.0.0.1"
	TCP_PORT = 13000
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # UDP
	sock.connect((TCP_IP, TCP_PORT))
	sock.send(MESSAGE)
	sock.close()

	
def scarta(buffold,buffnew):
	scarta = False
	for i in xrange(8,len(buff),2):
		biteA = buffold[i]
		biteB = buffnew[i]
		if(biteA==biteB):
			scarta = True
		else:
			scarta = False
			break
	return scarta

def scarta2(buffold,buffnew):
	scarta = False
	result1 = messaggi.deserializzaStatoLineaIXL2(buffold)
	result2 = messaggi.deserializzaStatoLineaIXL2(buffnew)
	for i in range(0,len(result1)):
		if( result1[i] == result2[i]):
			scarta = True
		else:
			scarta = False
			break
	return scarta
	
def serverUDP(host, port):
	x=0
	old = bytearray()
	sock = socket.socket( socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
	sock.bind( (host,port) )
	#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	while 1:
		data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
		buff = map(ord,data)
		ifd = len(buff)
		if(len(buff)>1300):
			buf = buff[28:1353]
			if x==0:
				old = buf
				result = messaggi.deserializzaStatoLineaIXL(buf)
				#print "qui",result
			else:
				risp  = scarta2(old, buf)
				if(not risp):
					result = messaggi.deserializzaStatoLineaIXL(buf)
					#print result
					old = buf
			x+=1
			
			
			
#dictxmli = xmlconfReader.readXml(confitinerari)
#print dictxmli
#thread.start_new_thread(serverUDP, ("192.168.1.213", 4010))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((receive_UDP_IP, UDP_PORT))
sock.setblocking(0)



resultixl = {}
result=[0,0,0]
addr = []
lista={0:[0,0,0],1:[0,0,0],2:[0,0,0],3:[0,0,0],4:[0,0,0],5:[0,0,0]}


# 	
# while 1:	
# 	data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
# 	buff = map(ord,data)
# 	if(len(buff)>1300 and len(buff)<1400):
# 		#buf = buff#[28:1353]#[51:]
# 		#print buf
# 		#exit(0)
# 		if x==0:
# 			old = buff
# 			result = messaggi.deserializzaStatoLineaIXL(buff)
# 			print "qui",result
# 		else:
# 			risp  = scarta2(old, buff)
# 			if(not risp):
# 				result = messaggi.deserializzaStatoLineaIXL(buff)
# 				print result
# 				old = buff
# 		x+=1
	#print "list ", lista 
# 	for pronti in lista.values():
# 		xcdb= str(pronti[2])
# 		if dictxmli.has_key(xcdb):
# 			#print "dict ",dictxmli[xcdb]
# 			for element in dictxmli[xcdb]:
# 				bandiera = False
# 				sendmdg =[]
# 				for tupla in element:
# 					fcdb = int(tupla[0])
# 					qdev = int(tupla[1])
# 					if resultixl.has_key(fcdb):
# 						triscdb = resultixl[fcdb]
# 						if triscdb[1]==2 and qdev==triscdb[2]:
# 							bandiera = True
# 							sendmdg.append(fcdb)
# 							#manda il tris element
# 				if bandiera:
# 					print "tris ",triscdb
# 					sendUDP(str(sendmdg),pronti[1])
# 					print "element ", str(sendmdg)
# 					bandiera = False
# 						
# 					
	#print lista				
	#buffi = messaggi.messageRBC1(lista)
	#sendUDP(buffi,4010)
#	time.sleep(2)
	#raw_input("-->> PRESS ENTER <<<--- ")
x=0
old = bytearray()
sockx = socket.socket( socket.AF_INET, socket.SOCK_DGRAM) # UDP, socket.SOCK_RAW, socket.IPPROTO_UDP)
sockx.bind( ("192.168.1.101", 4010) )

#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
while 1:
	try:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		buff = map(ord,data)
		#print addr
		result = messaggi.des_messageRBC_new(buff)
		if (result[0]==65280) or (result[0]==7732):
			lista[0]=result
		if (result[0]==65615) or (result[0]==7723):
			lista[1]=result
		if (result[0]==65315) or (result[0]==7237):
			lista[2]=result
		if (result[0]==65316) or (result[0]==7327):
			lista[3]=result
		if result[0]==65282:
			lista[4]=result
		if result[0]==65551:
			lista[5]=result
		#print "received message:", data
		print "result ",result
		
				
	except socket.error as msg:
		p=0
		#sock.close() 
		#print "nessun messaggio ricevuto"
	data, addr = sockx.recvfrom(2048) # buffer size is 1024 bytes
	buff = map(ord,data)
	#print buff
	ifd = len(buff)
	#print ifd
	if(len(buff)>1300 and len(buff)<1400):
		buf = buff#[28:1353]#[51:]
		#print buf
		#exit(0)
		if x==0:
			old = buf
			result = messaggi.deserializzaStatoLineaIXL(buf)
			print "qui",result
		else:
			risp  = scarta2(old, buf)
			if(not risp):
				result = messaggi.deserializzaStatoLineaIXL(buf)
				print result
				old = buf
		x+=1
	#print lista				
	buffi = messaggi.messageRBC1(lista)
	sendUDP(buffi,4010)
#	time.sleep(2)
		


	
exit(0)
