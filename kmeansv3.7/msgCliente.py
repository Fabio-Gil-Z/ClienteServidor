import zmq
import sys
import os
import socket
import threading
import time
from subprocess import call

def respuestaComoCliente1():
	while True:
		msg = servidorSocket.recv()
		print("El k a evaluar es: {}".format(msg.decode('utf-8')))
		call(["./a.out","{}".format(msg.decode('utf-8'))])
		#call(["./a.out -5"])
		errorArchivo = open("salidaErrorCuadratico.txt")
		error = errorArchivo.read()
		errorArchivo.close()
		servidorSocket.send(bytes(error,'utf-8'))


context = zmq.Context()

servidorSocket = context.socket(zmq.REP)
servidorSocket.bind("tcp://*:{}".format(5001))



respuestaComoCliente1()