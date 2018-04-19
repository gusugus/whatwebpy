'''DEPERCATED'''






from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import os

import commands

import sys, select




TIME_INPUT = 10
TIEMPO_RECARGA = 20

LIMITE_MENSAJES = 20
XPATH_CAJA_MENSAJES = "/html/body/div/div/div/div[3]/div/footer/div[1]/div[2]/div/div[2]"
'''El nombre (div) con el que se debe buscar los nombres'''
CLASE_NOMBRE = "'_2wP_Y'"

CLASE_MENSAJE_NO_LEIDO = "'vW7d1'"
#CLASE_MENSAJE = "'vW7d1 _1nHRW'"
CLASE_MENSAJE = "'vW7d1'"
CLASE_CONTENEDOR_MENSAJES = "'RLfQR'"

CLASE_DERECHA = "'_2nmDZ'"
#/html/body/div/div/div/div[2]/div/div[3]/div/div/div/div[1]/div/div/div[2]/div[1]/div[2]
#/html/body/div/div/div/div[2]/div/div[3]/div/div/div/div[13]/div/div/div[2]/div[1]/div[2]
XPATH_TIEMPO_LLEGADA_1 = "/html/body/div/div/div/div[2]/div/div[3]/div/div/div/div["
XPATH_TIEMPO_LLEGADA_2 = "]/div/div/div[2]/div[1]/div[2]"

XPATH_NOMBRE_1 = "/html/body/div/div/div/div[2]/div/div[3]/div/div/div/div["
XPATH_NOMBRE_2 = "]/div/div/div[2]/div[1]/div[1]"

XPATH_NO_LEIDO_1 = "/html/body/div/div/div/div[2]/div/div[3]/div/div/div/div["
XPATH_NO_LEIDO_2 = "]/div/div/div[2]/div[2]/div[2]"

XPATH_MENSAJES_RECIBIDOS_1 = "/html/body/div/div/div/div[3]/div/div[2]/div/div/div[3]/div["




class Chat:
	def __init__(self, nombre, numero_xpath, no_leido, tiempo_llegada):
		'''Nombre del chat'''
		self.nombre = nombre
		'''En que numero del actual xpath esta'''
		self.numero_xpath = numero_xpath
		'''Numero de mensajes no leidos'''
		self.no_leido = no_leido
		self.tiempo_llegada = tiempo_llegada
		
	'''***GETTERS***'''
	def get_nombre(self):
		return self.nombre
	def get_numero_xpath(self):
		return self.numero_xpath
	def get_no_leido(self):
		return self.no_leido
	def get_tiempo_llegada(self):
		try:
			self.tiempo_llegada.split(":")
			return self.tiempo_llegada
		except :
			return "00:00"
	'''
	return int(tmp[0])*60+int(tmp[1])
	*ValueError: invalid literal for int() with base 10: 'Martes'
	'''
	def get_tiempo_llegada_en_minutos(self):
		try:
			tmp = self.tiempo_llegada.split(":")
			return int(tmp[0])*60+int(tmp[1])
		except :
			return 0
	'''*****SETTERS*****'''
	'''La lista de los mensajes que tiene'''
	def set_list(self, message):
		self.message = message
	def __str__(self):
		return self.nombre.encode('utf-8')+"("+str(self.no_leido)+")"+" [-"+str(self.get_tiempo_llegada()).encode('utf-8')+"-]"

'''-  -'''
class Mensaje:
	def __init__(self, contenido, dia, hora):
		self.contenido = contenido
		self.dia = dia
		self.hora = hora
	def get_contenido(self):
		return self.contenido
	def get_dia(self):
		return self.dia
	def get_hora(self):
		return self.hora
	def __str__(self):
		return self.contenido.encode('utf-8')+"::"+self.hora

def recargar_chats(driver):
	lista_web_element = driver.find_elements_by_xpath("//div[@class="+CLASE_NOMBRE+"]")
	return lista_web_element 
	
def enviar_mensaje(driver, mensaje):
	input_box = driver.find_element_by_xpath(XPATH_CAJA_MENSAJES)
	input_box.click()
	if isinstance(mensaje, str):
			mensaje = mensaje.decode("utf-8")
	action = ActionChains(driver)
        action.send_keys(mensaje)
        action.send_keys(Keys.RETURN)
	action.perform()



'''Traigo los X ultimos mensajes
* ERROR CUANDO TENGO DEMASIADOS MENSAJES NO LEIDOS....
'''
def recolectar_mensajes(driver, chat):
	#print "NO LEIDOS: "+str(chat.get_no_leido())
	array_recibidos = []
	
	lista_web_element_mensajes = driver.find_elements_by_xpath("//*[contains(concat(' ', @class, ' '),"+CLASE_MENSAJE+")]")
	mensajes_totales = len(lista_web_element_mensajes)
	try:
		#print("TODOS LOS NO LEIDOS")
		for i in range(mensajes_totales, mensajes_totales-chat.get_no_leido(), -1):
			#print ("*"+lista_web_element_mensajes[i-1].text)
			array_recibidos.append(lista_web_element_mensajes[i-1].text)
	except :
		print("Faltan mensajes... no puedo leer todos los mensajes de "+str(chat))
		return array_recibidos
	return array_recibidos


def get_chat_no_leido(array_chat):
	chat_retorno = None
	for chat in array_chat:
		if chat.get_no_leido()>0:
			chat_retorno = chat
			break
	return chat_retorno


#https://stackoverflow.com/questions/27009247/python-find-min-max-and-average-of-a-list-array
def get_chat_antiguo_no_leido(array_chat):
	
	chat_retorno = None
	for chat in array_chat:
		#print str(chat)
		if chat.get_no_leido()>0:
			if not chat_retorno:
				chat_retorno = chat
				#print str(chat_retorno)
			elif chat.get_tiempo_llegada_en_minutos() < chat_retorno.get_tiempo_llegada_en_minutos():
				chat_retorno = chat
				#print str(chat_retorno)
	return chat_retorno


def llenar_array_chat(driver):
	#print ('Llenando chats...')
	lista_web_element = recargar_chats(driver)
	array_chat = []
	inicio = 1
	no_leido=-1
	#Creo array con los chats que se encuentren
	#print "Son "+str(len(lista_web_element))+" elementos"
	for i in range(inicio, len(lista_web_element)+1):
		xpath_nombre = XPATH_NOMBRE_1+str(i)+XPATH_NOMBRE_2
		nombre = driver.find_element_by_xpath(xpath_nombre).text
		numero_xpath = i
		
		try:
			xpath_no_leido=XPATH_NO_LEIDO_1+str(i)+XPATH_NO_LEIDO_2
			no_leido = int(driver.find_element_by_xpath(xpath_no_leido).text)
		except Exception:
			no_leido=0
		try:
			xpath_tiempo_llegada = XPATH_TIEMPO_LLEGADA_1+str(i)+XPATH_TIEMPO_LLEGADA_2
			tiempo_llegada = driver.find_element_by_xpath(xpath_tiempo_llegada).text
		except:
			tiempo_llegada = "00:00"
		chat = Chat(nombre, numero_xpath, no_leido, tiempo_llegada)
		array_chat.append(chat)
	#print ('Fin de llenar chats')
	return array_chat

'''Recupero el numero total de mensajes que se ha traido'''
def total_mensajes_recuperados(driver):
	lista_web_element_mensajes = driver.find_elements_by_xpath("//div[@class="+CLASE_MENSAJE+"]")
	return len(lista_web_element_mensajes)

import os
import ConfigParser
def traer_configuraciones():
	global TIME_INPUT,TIEMPO_RECARGA,LIMITE_MENSAJES,XPATH_CAJA_MENSAJES,CLASE_NOMBRE,CLASE_MENSAJE_NO_LEIDO,CLASE_DERECHA,CLASE_MENSAJE,XPATH_NOMBRE_1,XPATH_NOMBRE_2,XPATH_MENSAJES_RECIBIDOS_1,PATH_FIREFOX_PROFILE,WEB
	configParser = ConfigParser.RawConfigParser()
	configParser.read(os.getcwd()+'/conf.txt')
	TIME_INPUT = configParser.get('conf','TIME_INPUT')
	
'''DEPERCATED'''
def input_time():
	i,o,e = select.select([sys.stdin],[],[],TIME_INPUT)
	if i:
		return sys.stdin.readline()
	else:
		return ""
def get_seleccion(driver, opcion):
	return driver.find_element_by_xpath(XPATH_NOMBRE_1+str(opcion)+"]")

def scroll_down(driver, scroll):
	driver.execute_script("document.getElementById('pane-side').scroll(0,"+str(scroll)+");")	

def scroll_up(driver, scroll):
	driver.execute_script("document.getElementById('pane-side').scroll(0,"+str(scroll)+");")
	
#document.getElementsByClassName('_2nmDZ')[0].scroll(document.body.scrollHeight,2*document.body.scrollHeight);
def scroll_down_all(driver):
	driver.execute_script("document.getElementsByClassName('_2nmDZ')[0].scroll(document.body.scrollHeight,2*document.body.scrollHeight);")
