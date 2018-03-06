import zmq
import sys
import os
import pyaudio
import socket
import wave
import threading
import time

#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.
#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.
#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.
#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.
#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.
#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.
#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.
#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.
#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.
#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.
#EL CLIENTE 1 SE TIENE QUE EJECUTAR PRIMERO.


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
    if len(sys.argv) != 1:
        print("Error!!!")
        exit()

    global p,socketEnviar,socketEscuchar
    context = zmq.Context()
    p = pyaudio.PyAudio()

    socketCapturaIP = context.socket(zmq.REP)
    socketCapturaIP.bind("tcp://*:{}".format(8002))

    socketEscuchar = context.socket(zmq.REP)
    socketEscuchar.bind("tcp://*:{}".format(8000))


    ipaddr = socketCapturaIP.recv_multipart()
    socketCapturaIP.send_multipart(ipaddr)

    ip = ipaddr[0].decode('utf-16')
    print(ip)

    socketEnviar = context.socket(zmq.REQ)
    socketEnviar.connect("tcp://{}:{}".format(ip, 8001))

    hilo_escuchar = threading.Thread(target = escuchar, args = ())
    hilo_escuchar.start()
    hilo_grabar = threading.Thread(target = grabar, args = ())
    hilo_grabar.start()


if __name__ == '__main__':
	main()
