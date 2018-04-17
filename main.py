# -*- coding: utf-8 -*-
'''
>>> x = "Hello World!"
>>> x[2:]
'llo World!'
>>> x[:2]
'He'
>>> x[:-2]
'Hello Worl'
>>> x[-2:]
'd!'
>>> x[2:-2]
'llo Worl'
'''
'''
geckodriver path
***

PATH=$PATH:/home/usuario/python/whatsapp
cd python/whatsapp/
python main.py

***
instalar python-dev
xxx
Actualizar iceweasel
llevar geckodriver a /usr/local/bin y darle permisos x
	os.environ["PATH"] += "/usr/local/bin/firefox"
xxx

http://maslinux.es/como-instalar-firefox-quantum-en-gnulinux/
$ sudo tar -xjf firefox-57.0.tar.bz2
$ sudo mv firefox /opt
$ sudo ln -s /opt/firefox/firefox /usr/bin/firefox57
$ firefox57


crear nuevo profile
firefox -p ->Nuevo Profile
'''
'''
import time
from webwhatsapi import WhatsAPIDriver


#print("waiting for QR")
driver = WhatsAPIDriver(client='Firefox', loadstyles=True, username='IFLEX')
#driver.get_qr()

list_chat = driver.view_unread()
for chat in list_chat:
	print chat
	
	
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



'''
whatsapp -p
'''
WEB = 'http://web.whatsapp.com'
PATH_FIREFOX_PROFILE = '/home/usuario/.mozilla/firefox/u31mpec6.wasap'

logging.basicConfig(filename='myapp.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)
profile = webdriver.FirefoxProfile(PATH_FIREFOX_PROFILE)
driver = webdriver.Firefox(profile)
#driver.implicitly_wait(40) # seconds
driver.get(WEB)
delay = 100 # seconds
try:
	myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'app')))
#lista_web_element = driver.find_elements_by_xpath("//div[@class='_2wP_Y']")
#print('Espero... hasta q se \"LLENE\" todos')
	scroll=0
#termino de organizar y muestro a cual quiero hacer click
	while True:	
		time.sleep(1)
		print "Buscando chats nuevos..."
		#Se actualiza cada X tiempo y si encuentra chat con mensajes no leidos los contestara
		array_chat = llenar_array_chat(driver)

		if array_chat > 6:
			try:				
				while todos_llenos(array_chat):
					print 'HaY no leidos'
					scroll_down(driver, scroll)
					time.sleep(0.5)
					scroll = scroll + 200
					time.sleep(0.5)
					array_chat = llenar_array_chat(driver)
				
				if todos_vacios(array_chat):
					print 'todos vacios'
					scroll_up(driver, scroll)
					time.sleep(0.5)
					scroll = scroll - 200
					time.sleep(0.5)
					array_chat = llenar_array_chat(driver)
			except:
				print ("Javascrit exception")
		time.sleep(1)
		chat_no_leido = get_chat_antiguo_no_leido(array_chat)
		#chat_no_leido = get_chat_no_leido(array_chat)
		'''
		os.system('clear')
		array_chat = llenar_array_chat(driver)
		print 'Tenemos los siguientes chats disponibles: '
		i=1
		for chat in array_chat:
			print "* "+str(i)+": "+str(chat)
			i=i+1
		print("Ingrese el numero al cual quiere mandar mensaje: ")
		
		opcion = str(input_time())
		print "Opcion deseada"+str(opcion)
		if (opcion!="0") and (opcion!="") and (opcion!=None) and (opcion!="\n"):
		'''
		if(chat_no_leido!=None):
			opcion = chat_no_leido.get_numero_xpath()
			seleccion = get_seleccion(driver, opcion)
			
			Hover = ActionChains(driver).move_to_element(seleccion)
			Hover.perform()
			Hover.click().perform()
			print 'click'
			time.sleep(1)
			
			'''
			driver.execute_script("document.getElementById('app').click();")
			print 'click2'
			time.sleep(1)
			driver.execute_script("document.getElementById('app').focus();")
			print 'Di Focus'
			time.sleep(1)
			'''
			a = commands.getoutput("xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) _NET_WM_NAME")
			start = a.find("\"")+1
			programa_actual = a[start:-1]
			print 'Nombre programa actual: '+programa_actual
			#Recuperar el chat q se escogio
			chat = array_chat[int(opcion)-1] # En el array es el anterior
			#El numero de mensajes totales que se reciben...
			time.sleep(1)
			#mensajes_totales = total_mensajes_recuperados(driver)
			#print str(mensajes_totales)
			#El array de mensajjes recibidos...
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
			#str1 = str1.encode('utf-8')
			print "Mensaje que llego: "+str1.encode('utf-8')
			
			#enviar_mensaje(driver, str1)
			commands.getoutput('wmctrl -a Firefox')
			time.sleep(1)
			#Pierdo el foco
			#driver.execute_script("document.getElementById('app').click();")			
			#print 'quito focus'			
			#driver.execute_script("document.getElementById('app').blur();")
			commands.getoutput("wmctrl -a '"+programa_actual+"'")
			
			time.sleep(TIEMPO_RECARGA)
except TimeoutException:
	print "Load took too much time!"

except:
	logging.exception(str(datetime.now()))
