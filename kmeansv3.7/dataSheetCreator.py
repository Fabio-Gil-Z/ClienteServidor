import random
import math

numeroUsuarios = 100
peliculas = 100
calificacion = 1

dataCombinedCalificacion = open("dataCombinadoCalificacion.txt","w")


for i in range(1,numeroUsuarios+1):
	dataCombinedCalificacion.write(str(i))
	dataCombinedCalificacion.write(" ")
	for j in range(1, peliculas):
		vista = math.ceil(random.uniform(0,10))
		if vista < 8:
			dataCombinedCalificacion.write(str(j))
			dataCombinedCalificacion.write(" ")
			dataCombinedCalificacion.write(str(math.ceil(random.uniform(0,5))))
			dataCombinedCalificacion.write(" ")
		else:
			pass
	dataCombinedCalificacion.write("\n")


dataCombinedCalificacion.close()

dataCombinedCalificacion = open("dataCombinadoCalificacion.txt","r")
for line in dataCombinedCalificacion:
	print(line)

# for i in range(0,10):
# 	print(math.ceil(random.uniform(0,10)))