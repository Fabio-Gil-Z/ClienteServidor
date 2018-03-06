import zmq
import sys
import os
import pyaudio
import socket
import wave
import threading
import time

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 0.5


def escucharCliente1():
    global c5001,c6001,numeroCliente,audioCliente1,switch1
    while True:
        audioCliente1 = c5001.recv_multipart()
        c5001.send_multipart(audioCliente1)
        if switch1 == 1:
            print("MWAHAHAHAAHAHAH SWITCH1 == 1")
            hilo_cliente1_redirigir_6001.start()
            switch1 = 0
        if switch1 == 2:
            print("MWAHAHAHAAHAHAH SWITCH1 == 2")
            hilo_cliente1_redirigir_7001.start()
            switch1 = 0





def redirigirCliente1_6001(audio):
    global c6001,audioCliente1
    while True:
        c6001.send_multipart(audioCliente1)
        c6001.recv_multipart()

def redirigirCliente1_7001(audio):
    global c7001,audioCliente1
    while True:
        c7001.send_multipart(audioCliente1)
        c7001.recv_multipart()

def escucharCliente2():
    global c6002,c5002,numeroCliente,audioCliente1,switch2,audioCliente2
    while True:
        audioCliente2 = c6002.recv_multipart()
        c6002.send_multipart(audioCliente2)
        if switch2 == 1:
            print("HOHOHOHOHOHOHO SWITCH2 == 1")
            hilo_cliente2_redirigir_5002.start()
            switch2 = 0
        if switch2 == 2:
            print("HOHOHOHOHOHOHO SWITCH2 == 2")
            hilo_cliente2_redirigir_7002.start()
            switch2 = 0

def redirigirCliente2_5002(audio):
    global c5002,audioCliente2
    while True:
        c5002.send_multipart(audioCliente2)
        c5002.recv_multipart()

def redirigirCliente2_7002(audio):
    global c7002,audioCliente2
    while True:
        print("soy redirigirCliente2_7002  antes de RECV")
        c7002.send_multipart(audioCliente2)
        c7002.recv_multipart()
        print("soy redirigirCliente2_7002  despues de RECV")

def escucharCliente3():
    global c7003,c6003,c5003,numeroCliente,audioCliente1,switch1,switch2,audioCliente3
    switch3 = 1
    while True:
        audioCliente3 = c7003.recv_multipart()
        c7003.send_multipart(audioCliente2)
        if switch3 == 1:
            hilo_cliente3_redirigir_5003.start()
            hilo_cliente3_redirigir_6003.start()
            switch3 = 0


def redirigirCliente3_5003(audio):
    global c5002,audioCliente3
    while True:
        c5003.send_multipart(audioCliente3)
        c5003.recv_multipart()

def redirigirCliente3_6003(audio):
    global c6003,audioCliente3
    while True:
        c6003.send_multipart(audioCliente3)
        c6003.recv_multipart()




def cliente1connect(ipaddr):
    #---------------------------------SOCKETS DE SALIDA---------------------------------#
    #------------------------------SOCKETS DEl CLIENTE 1  5000--------------------------#
    global c5002, c5003
    c5002 = context.socket(zmq.REQ)
    c5002.connect("tcp://{}:{}".format(ipaddr, 5002))
    c5003 = context.socket(zmq.REQ)
    c5003.connect("tcp://{}:{}".format(ipaddr, 5003))

def cliente2connect(ipaddr):
    #------------------------------SOCKETS DEl CLIENTE 2  6000--------------------------#
    global c6001,c6003
    c6001 = context.socket(zmq.REQ)
    c6001.connect("tcp://{}:{}".format(ipaddr, 6001))
    c6003 = context.socket(zmq.REQ)
    c6003.connect("tcp://{}:{}".format(ipaddr, 6003))
    print("CLIENTE CONNECT 2")

def cliente3connect(ipaddr):
     #------------------------------SOCKETS DEl CLIENTE 3  7000--------------------------#
    global c7001,c7002
    c7001 = context.socket(zmq.REQ)
    c7001.connect("tcp://{}:{}".format(ipaddr, 7001))
    c7002 = context.socket(zmq.REQ)
    c7002.connect("tcp://{}:{}".format(ipaddr, 7002))

def registrar():
    global registro,numeroCliente,switch1,switch2
    while True:
        msg = registro.recv_multipart()
        print(msg[1].decode('utf-16'))
        if numeroCliente == 0:
            cliente1connect(msg[1].decode('utf-16'))
            respuesta = []
            respuesta.append(bytes("5001", 'utf-16'))
            registro.send_multipart(respuesta)
        elif numeroCliente == 1:
            cliente2connect(msg[1].decode('utf-16'))
            respuesta = []
            respuesta.append(bytes("6002", 'utf-16'))
            registro.send_multipart(respuesta)
            switch1 = 1
            switch2 = 1
            print("SOY SWITCH2 YEAHHHHHH {}".format(switch2))
        elif numeroCliente == 2:
            cliente3connect(msg[1].decode('utf-16'))
            respuesta = []
            respuesta.append(bytes("7003", 'utf-16'))
            registro.send_multipart(respuesta)
            switch1 = 2
            switch2 = 2
        else:
            respuesta = []
            respuesta.append(bytes("NO SOPORTA MAS CLIENTES", 'utf-16'))
            registro.send_multipart(respuesta)
        numeroCliente += 1

def main():
    if len(sys.argv) != 1:
        print("Error!!!")
        exit()

    global context,registro,numeroCliente,c5001,c5002,c5003,c6001,c6002,c6003,c7001,c7002,c7003,switch1,switch2,audioCliente1,audioCliente2,audioCliente3
    global hilo_cliente1_redirigir_6001, hilo_cliente1_redirigir_7001 
    global hilo_cliente2_redirigir_5002, hilo_cliente2_redirigir_7002
    global hilo_cliente3_redirigir_5003, hilo_cliente3_redirigir_6003
    numeroCliente = 0
    switch1 = 0
    switch2 = 0
    audioCliente1 = []
    audioCliente2 = []
    audioCliente3 = []
    #port = sys.argv[1] #Server's port
    context = zmq.Context()

    #---------------------------------SOCKETS DE REGISTRO-------------------------------#       
    registro = context.socket(zmq.REP)
    registro.bind("tcp://*:{}".format(8000))
    #---------------------------------SOCKETS DE ENTRADA--------------------------------#	    
    c5001 = context.socket(zmq.REP)
    c5001.bind("tcp://*:{}".format(5001))

    c6002 = context.socket(zmq.REP)
    c6002.bind("tcp://*:{}".format(6002))

    c7003 = context.socket(zmq.REP)
    c7003.bind("tcp://*:{}".format(7003))


    #---------------------------------HILO REGISTRO----------------------------------#
    hilo_registro = threading.Thread(target = registrar, args = ())  
    hilo_registro.start()

    #---------------------------------HILOS CLIENTE 1--------------------------------#
    hilo_cliente1 = threading.Thread(target = escucharCliente1, args = ())
    hilo_cliente1.start()

    hilo_cliente1_redirigir_6001 = threading.Thread(target = redirigirCliente1_6001, args = (audioCliente1,))

    hilo_cliente1_redirigir_7001 = threading.Thread(target = redirigirCliente1_7001, args = (audioCliente1,))

    #---------------------------------HILOS CLIENTE 2--------------------------------#
    hilo_cliente2 = threading.Thread(target = escucharCliente2, args = ())
    hilo_cliente2.start()

    hilo_cliente2_redirigir_5002 =threading.Thread(target = redirigirCliente2_5002, args = (audioCliente2,))

    hilo_cliente2_redirigir_7002 =threading.Thread(target = redirigirCliente2_7002, args = (audioCliente2,))

    #---------------------------------HILOS CLIENTE 3--------------------------------#
    hilo_cliente3 = threading.Thread(target = escucharCliente3, args = ())
    hilo_cliente3.start()

    hilo_cliente3_redirigir_5003 = threading.Thread(target = redirigirCliente3_5003, args = (audioCliente3,))

    hilo_cliente3_redirigir_6003 = threading.Thread(target = redirigirCliente3_6003, args = (audioCliente3,))

'''
    while True:
        if switch1 == 1:
            hilo_cliente1_redirigir_6001.start()
            #hilo_cliente2_redirigir_5002.start()
            switch1 = 0
'''











if __name__ == '__main__':
    main()