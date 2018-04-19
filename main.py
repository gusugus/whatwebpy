# -*- coding: utf-8 -*-
'''
***geckodriver path***
PATH=$PATH:/home/usuario/python/whatsapp
cd python/whatsapp/
python main.py

***
instalar python-dev

http://maslinux.es/como-instalar-firefox-quantum-en-gnulinux/
$ sudo tar -xjf firefox-57.0.tar.bz2
$ sudo mv firefox /opt
$ sudo ln -s /opt/firefox/firefox /usr/bin/firefox57
$ firefox57

import time
from webwhatsapi import WhatsAPIDriver	
	
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from funciones import *
import logging
import time
from datetime import datetime
import sys

MAXIMO_CHAT = 6
SCROLL_SIZE = 40


def todos_llenos(array):
	contador = 0
	for chat in array:
		if chat.get_no_leido() > 0 :
			contador = contador + 1
	if contador == len(array):
		return True
	else:
		return False
	
def todos_vacios(array):
	contador = 0
	for chat in array:
		if chat.get_no_leido() == 0 :
			contador = contador + 1
	if contador == len(array):
		return True
	else:
		return False

WEB = 'http://web.whatsapp.com'
PATH_FIREFOX_PROFILE = '/home/usuario/.mozilla/firefox/u31mpec6.wasap'

logging.basicConfig(filename='myapp.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)
profile = webdriver.FirefoxProfile(PATH_FIREFOX_PROFILE)
driver = webdriver.Firefox(profile)
driver.get(WEB)
delay = 100 # seconds
try:
	myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'app')))
	scroll=0
#termino de organizar y muestro a cual quiero hacer click
	while True:	
		time.sleep(1)
		print "Buscando chats nuevos..."
		#Se actualiza cada X tiempo y si encuentra chat con mensajes no leidos los contestara
		array_chat = llenar_array_chat(driver)

		if array_chat > MAXIMO_CHAT:
			try:				
				while todos_llenos(array_chat):
					#BAJAMOS UN POCO EL SCREEN
					#print 'HaY no leidos'
					scroll = scroll + SCROLL_SIZE
					scroll_down(driver, scroll)
					time.sleep(0.5)
					array_chat = llenar_array_chat(driver)
					time.sleep(1)
				if todos_vacios(array_chat):
					#SI ESTAMOS HASTA ABAJO... SUBIMOS UN POCO
					#print 'todos vacios'
					scroll = scroll - SCROLL_SIZE
					scroll_up(driver, scroll)
					time.sleep(0.5)
					array_chat = llenar_array_chat(driver)
					time.sleep(0.5)
			except:
				print ("Javascrit exception")
		#time.sleep(1)
		chat_no_leido = get_chat_antiguo_no_leido(array_chat)
		#time.sleep(3)
		if(chat_no_leido!=None):
			print ("*CHAT AL QUE DEBO HACER CLICK: *"+str(chat_no_leido))
			opcion = chat_no_leido.get_numero_xpath()
			seleccion = get_seleccion(driver, opcion)
			print ("Hago click")
			flag_click = False
			
			try:
				Hover = ActionChains(driver).move_to_element(seleccion)
				Hover.perform()
				Hover.click().perform()
			except :
				print ("No pude hacer click")
				flag_click = True
				
			while flag_click:
				try:
					scroll = scroll + SCROLL_SIZE
					scroll_down(driver, scroll)
					#time.sleep(0.5)
					
					Hover = ActionChains(driver).move_to_element(seleccion)
					Hover.perform()
					Hover.click().perform()
					#print ("Pude hacer click")
					flag_click = False
					#time.sleep(1)
				except :
					#print ("No pude hacer click")
					continue
			
			a = commands.getoutput("xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) _NET_WM_NAME")
			start = a.find("\"")+1
			programa_actual = a[start:-1]
			print 'Nombre programa actual: '+programa_actual
			chat = array_chat[int(opcion)-1] # En el array es el anterior
			#time.sleep(1)
			print("Ya seleccion.e. el chat")
			array_recibidos_t = recolectar_mensajes(driver, chat)
			array_recibidos_t.reverse()
			array_recibidos = [x.replace('\n', '') for x in array_recibidos_t]
			
			lista_mensajes = []
			for msg in array_recibidos:
				hora = msg[-5:]
				contenido = msg[:-5]
				dia = 'hoy'
				msg_tmp = Mensaje(contenido, dia, hora)
				lista_mensajes.append(msg_tmp)
			str1 = ""
			for mens in lista_mensajes:
				str1 = str1+" "+mens.get_contenido()
			print "Mensaje que llego: "+str1.encode('utf-8')
			scroll_down_all(driver)
			
			commands.getoutput('wmctrl -a Firefox')
			time.sleep(0.8)
			commands.getoutput("wmctrl -a '"+programa_actual+"'")
			
			time.sleep(TIEMPO_RECARGA)
except TimeoutException:
	print "Load took too much time!"

except:
	logging.exception(str(datetime.now()))
