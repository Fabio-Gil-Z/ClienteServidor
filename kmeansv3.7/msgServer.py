import zmq
import sys
import os
import socket
import threading
import time
import random
import math


NUMEROUSUARIOS = 100

def calcularPendienteSig(k,dist,arrayErrorCuadratico):
	numerador =  abs(arrayErrorCuadratico[0]-dist)
	denominador = abs(arrayDeK[0] - k)
	resultado = numerador / denominador
	return resultado
def calcularPendienteAnt(k,dist,arrayErrorCuadratico):
	numerador =  abs(arrayErrorCuadratico[1] - dist )
	denominador = abs(arrayDeK[1] - k )
	resultado = numerador / denominador
	return resultado

def coneccionCliente1():
	while True:
		a = 0
		global k,arrayErrorCuadratico,switch,CONTADOR
		if len(arrayErrorCuadratico) == 2:
			k = str(math.ceil(random.uniform(arrayDeK[0],arrayDeK[1])))
			print("Array de K: {}".format(arrayDeK))
			print("Array de ErrorCuadratico: {}".format(arrayErrorCuadratico))
			print("\n")
			print("k: {}".format(k))
			cliente1.send(bytes(k,'utf-8'))			
			msg = cliente1.recv()			
			dist = float(msg.decode('utf-8'))
			print("La distancia es: {}".format(dist))
			try:		
				sig = calcularPendienteSig(int(k),dist,arrayErrorCuadratico)
				print("pendiente: entre k: {} y k: [{}]".format(k,arrayDeK[0]))
				print("Pendiente sig: {}\n".format(sig))			
			except:
				switch = 1
				break;
			try:
				ant = calcularPendienteAnt(int(k),dist,arrayErrorCuadratico)
			except:
				switch = 1
				break
			print("pendiente: entre k: {} y k: [{}]".format(k,arrayDeK[1]))		
			print("Pendiente ant: {}".format(ant))
			print("\n")
			if sig > ant:
				arrayDeK[1] = int(k)
				arrayErrorCuadratico[1] = dist
				arrayPendientes.append(sig)
				arrayDeKFinal.append(k)
			else:
				arrayDeK[0] = int(k)
				arrayErrorCuadratico[0] = dist
				arrayPendientes.append(ant)
				arrayDeKFinal.append(k)
		elif CONTADOR == 0:
			k = str(math.ceil(NUMEROUSUARIOS/2))
			CONTADOR+=1			
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente1.send(bytes(k,'utf-8'))
			msg = cliente1.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)
			
		elif CONTADOR == 1:
			k = str(1)
			CONTADOR+=1				
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente1.send(bytes(k,'utf-8'))
			msg = cliente1.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)
			
		elif CONTADOR > 1:
			k = str(math.ceil(random.uniform(1,NUMEROUSUARIOS/2)))
			CONTADOR+=1				
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente1.send(bytes(k,'utf-8'))
			msg = cliente1.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)
			
			


def coneccionCliente2():
	while True:
		time.sleep(1)
		global k,arrayErrorCuadratico,switch,CONTADOR
		if len(arrayErrorCuadratico) == 2:
			k = str(math.ceil(random.uniform(arrayDeK[0],arrayDeK[1])))
			print("Array de K: {}".format(arrayDeK))
			print("Array de ErrorCuadratico: {}".format(arrayErrorCuadratico))
			print("\n")
			print("k: {}".format(k))
			cliente2.send(bytes(k,'utf-8'))			
			msg = cliente2.recv()			
			dist = float(msg.decode('utf-8'))
			print("La distancia es: {}".format(dist))
			try:		
				sig = calcularPendienteSig(int(k),dist,arrayErrorCuadratico)
				print("pendiente: entre k: {} y k: [{}]".format(k,arrayDeK[0]))
				print("Pendiente sig: {}\n".format(sig))			
			except:
				switch = 1
				break;
			try:
				ant = calcularPendienteAnt(int(k),dist,arrayErrorCuadratico)
			except:
				switch = 1
				break;
			print("pendiente: entre k: {} y k: [{}]".format(k,arrayDeK[1]))		
			print("Pendiente ant: {}".format(ant))
			print("\n")
			if sig > ant:
				arrayDeK[1] = int(k)
				arrayErrorCuadratico[1] = dist
				arrayPendientes.append(sig)
				arrayDeKFinal.append(k)
			else:
				arrayDeK[0] = int(k)
				arrayErrorCuadratico[0] = dist
				arrayPendientes.append(ant)
				arrayDeKFinal.append(k)
		elif CONTADOR == 0:
			k = str(math.ceil(NUMEROUSUARIOS/2))
			CONTADOR+=1			
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente2.send(bytes(k,'utf-8'))
			msg = cliente2.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)
			
		elif CONTADOR == 1:
			k = str(1)
			CONTADOR+=1				
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente2.send(bytes(k,'utf-8'))
			msg = cliente2.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)
			
		elif CONTADOR > 1:
			k = str(math.ceil(random.uniform(NUMEROUSUARIOS/2,NUMEROUSUARIOS)))
			CONTADOR+=1				
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente2.send(bytes(k,'utf-8'))
			msg = cliente2.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)
			



def coneccionCliente3():
	while True:
		time.sleep(2)
		global k,arrayErrorCuadratico,switch,CONTADOR
		if len(arrayErrorCuadratico) == 2:
			k = str(math.ceil(random.uniform(arrayDeK[0],arrayDeK[1])))
			print("Array de K: {}".format(arrayDeK))
			print("Array de ErrorCuadratico: {}".format(arrayErrorCuadratico))
			print("\n")
			print("k: {}".format(k))
			cliente3.send(bytes(k,'utf-8'))			
			msg = cliente3.recv()			
			dist = float(msg.decode('utf-8'))
			print("La distancia es: {}".format(dist))
			try:		
				sig = calcularPendienteSig(int(k),dist,arrayErrorCuadratico)
				print("pendiente: entre k: {} y k: [{}]".format(k,arrayDeK[0]))
				print("Pendiente sig: {}\n".format(sig))			
			except:
				switch = 1
				break;
			try:
				ant = calcularPendienteAnt(int(k),dist,arrayErrorCuadratico)
			except:
				switch = 1
				break;
			print("pendiente: entre k: {} y k: [{}]".format(k,arrayDeK[1]))		
			print("Pendiente ant: {}".format(ant))
			print("\n")
			if sig > ant:
				arrayDeK[1] = int(k)
				arrayErrorCuadratico[1] = dist
				arrayPendientes.append(sig)
				arrayDeKFinal.append(k)
			else:
				arrayDeK[0] = int(k)
				arrayErrorCuadratico[0] = dist
				arrayPendientes.append(ant)
				arrayDeKFinal.append(k)
		elif CONTADOR == 0:
			k = str(math.ceil(NUMEROUSUARIOS/2))
			CONTADOR+=1			
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente3.send(bytes(k,'utf-8'))
			msg = cliente3.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)
			
		elif CONTADOR == 1:
			k = str(1)
			CONTADOR+=1				
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente3.send(bytes(k,'utf-8'))
			msg = cliente3.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)
			
		elif CONTADOR > 1:
			k = str(math.ceil(random.uniform(NUMEROUSUARIOS/2,NUMEROUSUARIOS)))
			CONTADOR+=1				
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente3.send(bytes(k,'utf-8'))
			msg = cliente3.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)

def coneccionCliente4():
	while True:
		time.sleep(3)
		global k,arrayErrorCuadratico,switch,CONTADOR
		if len(arrayErrorCuadratico) == 2:
			k = str(math.ceil(random.uniform(arrayDeK[0],arrayDeK[1])))
			print("Array de K: {}".format(arrayDeK))
			print("Array de ErrorCuadratico: {}".format(arrayErrorCuadratico))
			print("\n")
			print("k: {}".format(k))
			cliente4.send(bytes(k,'utf-8'))			
			msg = cliente4.recv()			
			dist = float(msg.decode('utf-8'))
			print("La distancia es: {}".format(dist))
			try:		
				sig = calcularPendienteSig(int(k),dist,arrayErrorCuadratico)
				print("pendiente: entre k: {} y k: [{}]".format(k,arrayDeK[0]))
				print("Pendiente sig: {}\n".format(sig))			
			except:
				switch = 1
				break;
			try:
				ant = calcularPendienteAnt(int(k),dist,arrayErrorCuadratico)
			except:
				switch = 1
				break;
			print("pendiente: entre k: {} y k: [{}]".format(k,arrayDeK[1]))		
			print("Pendiente ant: {}".format(ant))
			print("\n")
			if sig > ant:
				arrayDeK[1] = int(k)
				arrayErrorCuadratico[1] = dist
				arrayPendientes.append(sig)
				arrayDeKFinal.append(k)
			else:
				arrayDeK[0] = int(k)
				arrayErrorCuadratico[0] = dist
				arrayPendientes.append(ant)
				arrayDeKFinal.append(k)
		elif CONTADOR == 0:
			k = str(math.ceil(NUMEROUSUARIOS/2))
			CONTADOR+=1			
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente4.send(bytes(k,'utf-8'))
			msg = cliente4.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)
			
		elif CONTADOR == 1:
			k = str(1)
			CONTADOR+=1				
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente4.send(bytes(k,'utf-8'))
			msg = cliente4.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)
			
		elif CONTADOR > 1:
			k = str(math.ceil(random.uniform(NUMEROUSUARIOS/2,NUMEROUSUARIOS)))
			CONTADOR+=1				
			#print(int(k))
			#sorted(k)
			#print("\n")
			cliente4.send(bytes(k,'utf-8'))
			msg = cliente4.recv()
			print(msg.decode('utf-8'))
			arrayErrorCuadratico.append(float(msg.decode('utf-8')))
			arrayDeK.append(int(k))
			#sorted(arrayErrorCuadratico)

context = zmq.Context()

ip = "127.0.0.1"
cliente1 = context.socket(zmq.REQ)
cliente1.connect("tcp://{}:{}".format(ip,5001))

cliente2 = context.socket(zmq.REQ)
cliente2.connect("tcp://{}:{}".format("192.168.0.105",6001))

#cliente3 = context.socket(zmq.REQ)
#cliente3.connect("tcp://{}:{}".format("192.168.12.25",7001))

#cliente4 = context.socket(zmq.REQ)
#cliente4.connect("tcp://{}:{}".format("192.168.12.29",8001))

global k,arrayErrorCuadratico,arrayDeK,arrayPendientes,switch,CONTADOR
arrayErrorCuadratico = []
arrayDeK = []
arrayDeKFinal = []
arrayPendientes = []
k = 1
switch = 0;
CONTADOR = 0





hiloCliente1 = threading.Thread(target = coneccionCliente1, args = ())
hiloCliente1.start()
hiloCliente2 = threading.Thread(target = coneccionCliente2, args = ())
hiloCliente2.start()
#hiloCliente3 = threading.Thread(target = coneccionCliente3, args = ())
#hiloCliente3.start()
#hiloCliente4 = threading.Thread(target = coneccionCliente4, args = ())
#hiloCliente4.start()


while(True):
	if switch == 1:
		print("\n\n")
		print("Los resultados son:\n")
		laMasPendiente = max(arrayPendientes)
		indexParaK = arrayPendientes.index(laMasPendiente)
		elMejorK = arrayDeKFinal[indexParaK]

		print(arrayPendientes)
		print("\n")
		print(arrayDeKFinal)
		print("\n")

		print("El mejor K es: {}\n".format(elMejorK))
		print("Con el maximo cambio de pendiente: {}\n".format(laMasPendiente))
		sys.exit()

