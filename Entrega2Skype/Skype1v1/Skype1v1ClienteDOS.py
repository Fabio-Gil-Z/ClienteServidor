import zmq
import sys
import os
import pyaudio
import socket
import wave
import threading
import time

#EJECUTAR EL CLIENTE UNO PRIMERO. GRACIAS
#EJECUTAR EL CLIENTE UNO PRIMERO. GRACIAS
#EJECUTAR EL CLIENTE UNO PRIMERO. GRACIAS
#EJECUTAR EL CLIENTE UNO PRIMERO. GRACIAS
#EJECUTAR EL CLIENTE UNO PRIMERO. GRACIAS
#EJECUTAR EL CLIENTE UNO PRIMERO. GRACIAS
#EJECUTAR EL CLIENTE UNO PRIMERO. GRACIAS
#EJECUTAR EL CLIENTE UNO PRIMERO. GRACIAS



FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 0.5

def escuchar():
	streamEscuchar = p.open(format = FORMAT,
	            channels = CHANNELS,
	            rate = RATE,
	            input = True, output = True,
	            frames_per_buffer = CHUNK)
	while True:
	    audio = socketEscuchar.recv_multipart()
	    for frame in audio:
	        streamEscuchar.write(frame, CHUNK)
	    socketEscuchar.send_multipart(audio)

def grabar():
	streamEnviar = p.open(format = FORMAT,
	            channels = CHANNELS,
	            rate = RATE,
	            input = True, output = True,
	            frames_per_buffer = CHUNK)
	while True:
	    frames = []
	    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	        frames.append(streamEnviar.read(CHUNK))
	    socketEnviar.send_multipart(frames)
	    socketEnviar.recv_multipart()

def main():
    if len(sys.argv) != 2:
        print("Error!!!")
        exit()

    ip = sys.argv[1] #Server's ip
    global p,socketEnviar,socketEscuchar
    context = zmq.Context()
    p = pyaudio.PyAudio()

    socketEnviarIP = context.socket(zmq.REQ)
    socketEnviarIP.connect("tcp://{}:{}".format(ip, 8002))

    listaIP = []
    ipaddr = input("Porfavor escribe tu IP -> ")
    listaIP.append(bytes(ipaddr, 'utf-16'))
    socketEnviarIP.send_multipart(listaIP)
    socketEnviarIP.recv_multipart()

    socketEscuchar = context.socket(zmq.REP)
    socketEscuchar.bind("tcp://*:{}".format(8001))

    socketEnviar = context.socket(zmq.REQ)
    socketEnviar.connect("tcp://{}:{}".format(ip, 8000))

    hilo_escuchar = threading.Thread(target = escuchar, args = ())
    hilo_escuchar.start()
    hilo_grabar = threading.Thread(target = grabar, args = ())
    hilo_grabar.start()

if __name__ == '__main__':
	main()
