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
RECORD_SECONDS = 1

def conectarCliente1(puerto):
    global ip
    cliente1_5002 = context.socket(zmq.REQ)
    cliente1_5002.connect("tcp://{}:{}".format(ip, puerto))

    cliente1_5003 = context.socket(zmq.REQ)
    cliente1_5003.connect("tcp://{}:{}".format(ip, puerto))

def conectarCliente2(puerto):
    global ip
    cliente2_6001 = context.socket(zmq.REQ)
    cliente2_6001.connect("tcp://{}:{}".format(ip, puerto))

    cliente2_6003 = context.socket(zmq.REQ)
    cliente2_6003.connect("tcp://{}:{}".format(ip, puerto))

def conectarCliente3(puerto):
    global ip
    cliente3_7001 = context.socket(zmq.REQ)
    cliente3_7001.connect("tcp://{}:{}".format(ip, puerto))

    cliente3_7002 = context.socket(zmq.REQ)
    cliente3_7002.connect("tcp://{}:{}".format(ip, puerto))

def escucharC6001():
    print("escuchar c6001")
    stream6001 = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True, output = True,
                frames_per_buffer = CHUNK)
    while True:
        msg = c6001.recv_multipart()
        for frame in msg:
            stream6001.write(frame, CHUNK)
        c6001.send_multipart(msg)

def escucharC5002():
    print("escuchar c5002")
    stream5002 = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True, output = True,
                frames_per_buffer = CHUNK)
    while True:
        msg = c5002.recv_multipart()
        for frame in msg:
            stream5002.write(frame, CHUNK)
        c5002.send_multipart(msg)



def grabarCliente1():
    global stream1,cliente1_5001
    while True:
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            frames.append(stream1.read(CHUNK))
        cliente1_5001.send_multipart(frames)
        audio = cliente1_5001.recv_multipart()
        #for frame in audio:                       #-----------ACTIVAR PARA ESCUCHARSE A SI MISMO----------#
        #    stream1.write(frame, CHUNK)           #-----------ACTIVAR PARA ESCUCHARSE A SI MISMO----------#

def grabarCliente2():
    global stream2,cliente2_6002
    while True:
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            frames.append(stream2.read(CHUNK))
        cliente2_6002.send_multipart(frames)
        audio = cliente2_6002.recv_multipart()
        #for frame in audio:                    #-----------ACTIVAR PARA ESCUCHARSE A SI MISMO----------#
        #    stream2.write(frame, CHUNK)        #-----------ACTIVAR PARA ESCUCHARSE A SI MISMO----------#

def grabarCliente3():
    global stream3,cliente3_7003
    while True:
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            frames.append(stream2.read(CHUNK))
        cliente2_6002.send_multipart(frames)
        audio = cliente2_6002.recv_multipart()
        #for frame in audio:                    #-----------ACTIVAR PARA ESCUCHARSE A SI MISMO----------#
        #    stream2.write(frame, CHUNK)        #-----------ACTIVAR PARA ESCUCHARSE A SI MISMO----------#

def main():
    if len(sys.argv) != 2:
        print("Error!!!")
        exit()

    global ip,p,context,cliente1_5001,cliente2_6002,cliente3_7003,stream1,stream2,stream3, c5002, c6001
    ip = sys.argv[1] #Server's ip
    #port = sys.argv[2] #Server's port    
    context = zmq.Context()

    #---------------------------------SOCKET PARA ENVIAR REGISTRO-----------------------------#
    s = context.socket(zmq.REQ)
    s.connect("tcp://{}:{}".format(ip, 8000))

    #---------------------------------SOCKETS PARA RECIBIR GRABACIÓNES-----------------------------#
    c5002 = context.socket(zmq.REP)
    c5002.bind("tcp://*:{}".format(5002))

    c6001 = context.socket(zmq.REP)
    c6001.bind("tcp://*:{}".format(6001))





    p = pyaudio.PyAudio()
    stream3 = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True, output = True,
                frames_per_buffer = CHUNK)


    ipaddr = input("Escribe tu ip -> ")
    alias  = input("Escribe tu alias -> ")
    registro = []
    registro.append(bytes("registro",'utf-16'))
    registro.append(bytes(ipaddr,'utf-16'))
    registro.append(bytes(alias,'utf-16'))
    s.send_multipart(registro)
    msg = s.recv_multipart()
    print(msg[0].decode('utf-16'))
    if msg[0].decode('utf-16') == "NO SOPORTA MAS CLIENTES":
        sys.exit()
    
    if msg[0].decode('utf-16') == "5001":
        cliente1_5001 = context.socket(zmq.REQ)
        cliente1_5001.connect("tcp://{}:{}".format(ip, 5001))
        stream1 = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True, output = True,
                    frames_per_buffer = CHUNK)
        hilo1 = threading.Thread(target = grabarCliente1, args = ())
        hilo1.start()
        hilo1_escucharc5002 = threading.Thread(target = escucharC5002, args = ())
        hilo1_escucharc5002.start()

    elif msg[0].decode('utf-16') == "6002":
        cliente2_6002 = context.socket(zmq.REQ)
        cliente2_6002.connect("tcp://{}:{}".format(ip, 6002))
        stream2 = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True, output = True,
                    frames_per_buffer = CHUNK)
        hilo2 = threading.Thread(target = grabarCliente2, args = ())
        hilo2.start()
        hilo2_escucharc6001 = threading.Thread(target = escucharC6001, args = ())
        hilo2_escucharc6001.start()

    elif msg[0].decode('utf-16') == "7003":
        cliente3_7003 = context.socket(zmq.REQ)
        cliente3_7003.connect("tcp://{}:{}".format(ip, 7003))
        grabarCliente3()
    else:
        print("system error")
        sys.exit()








if __name__ == '__main__':
    main()