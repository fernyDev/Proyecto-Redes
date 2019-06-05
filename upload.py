import socket
import os
import threading
import sys
import fnmatch
from os.path import expanduser
import time
from progress.bar import Bar, ChargingBar

"""
API sockets UDP
Diagrama de conexcion para UDP
Caracteristicas y diferencias en TCP y UDP 
"""
#Variable que guarda la ruta de donde empezara a buscar
dirInicial = expanduser("~")

print("Direccion Inicial :"+dirInicial)
dirInicial = dirInicial + "/Archivos a Enviar"
print("Direccion Inicial :"+dirInicial)
#time.sleep(2)
#Array global que guardara las rutas de las imagenes encontradas
path = []

#Funcion que realiza la busqueda de imagenes en el arboles
def busqueda():
    for r, d, f in os.walk(dirInicial):
        d[:] = [dirs for dirs in d if not dirs.startswith('.')]
        d[:] = [dirs for dirs in d if not dirs.startswith('Library')]
        d[:] = [dirs for dirs in d if not dirs.startswith('AppData')]
        f[:] = [files for files in f if not files.startswith('.')]
        for files in f:
            path.append(os.path.join(r,files))
            print(path[-1])

def envio(archivo,tam,con):
    dato = archivo.read(tam)
    con.sendall(dato)


def main(path):

    puerto = int(input("Ingrese el puerto del servidor "))
    #ip = "localhost"
    ip = input("Escriba la IP del servidor: ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, puerto))
    #nombre_archivo = "3040_20.mp4"
    #nombre_archivo = input("Escriba el nombre del archivo: ")
    for i in range(len(path)):
        try:
            archivo = open(path[i], "br")
            if(len(archivo.read())>=4):
                print('Ruta: '+path[i])

                s.send(bytes("True","utf-8"))

                numero = s.recv(1)

                ruta, nombre_archivo = os.path.split(path[i])
                archivo.seek(0)
                tam = len(archivo.read())
                print("Enviando el tamano", tam)
                bar = ChargingBar("Subiendo:",max=tam)
                s.send(bytes(str(tam), "utf-8"))
                
                numero = s.recv(1)

                print("Enviando el nombre del archivo " + nombre_archivo)
                s.send(bytes(nombre_archivo, "utf-8"))

                numero = s.recv(1)

                #Se envia la ruta de la carpeta
                s.send(bytes(ruta,"utf-8"))

                numero = s.recv(1)

                tamano = []
                tamano.append(int(tam/4))
                tamano.append(tamano[0]*2)
                tamano.append(tamano[0]*3)
                tamano.append(int(tam)-(tamano[0]*3))
                print("Enviando archivo")

                archivo.seek(0)
                envio(archivo,tamano[0],s)
                bar.next(tamano[0])
                #print("Ya termino de enviar la primera parte")

                numero = s.recv(1)
                archivo.seek(tamano[0])
                envio(archivo,tamano[0],s)
                bar.next(tamano[0])
                #print("Ya termino de enviar la segunda parte")

                numero = s.recv(1)
                archivo.seek(tamano[1])
                envio(archivo,tamano[0],s)
                #print("Ya termino de enviar la tercera parte")
                bar.next(tamano[0])

                numero = s.recv(1)
                archivo.seek(tamano[2])
                envio(archivo,tamano[3],s)
                #print("Ya termino de enviar la tercera parte")
                bar.next(tamano[3])
                bar.finish()
                numero = s.recv(1)

                print("Ya me sali")
                archivo.close()
                del (archivo)
        except PermissionError:
            print("No se tiene acceso al archivo")

    s.send(bytes("False","utf-8"))
    print("Termine")
    return 0

busqueda()
main(path)
