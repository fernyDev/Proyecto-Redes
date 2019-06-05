import socket
import sys
import threading
import os
from os.path import expanduser

HOST = '192.168.4.30'  # The server's hostname or IP address
HOST2 = '192.168.5.2'
PORT1 = '3030'      # The port used by the server
PORT2 = '3032'
dirInicial = expanduser("~")


def create_folder(nombre_carpeta):
    dirInicial = dirInicial + "/" + nombre_carpeta
    if not os.path.exists(dirInicial):
        os.mkdir(dirInicial)


def recibir():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", int(PORT1)))
    s.listen()
    print("Esperando conexion")
    con, direccion = s.accept()
    print("Conexion establecida con " + direccion[0])
    while(True):
        estado = str(con.recv(5), encoding="utf-8")
        if estado == "True":
            con.send(bytes("1", "utf-8"))
            tam = int(str(con.recv(20), encoding="utf-8"))

            con.send(bytes("1", "utf-8"))
            nombre_archivo = str(con.recv(200), encoding="utf-8")

            con.send(bytes("1", "utf-8"))
            archivo_nuevo = open(dirInicial + "/" + nombre_archivo)
            info = con.recv(tam)
            if len(info) == tam:
                print("Ahuevo, si lo recibio enterito")
            else:
                print("No es igual :'v info= " +
                    str(len(info)) + "\ttam= " + str(tam))
            archivo_nuevo.write(info)
            del(info)
            archivo_nuevo.close()
            del(archivo_nuevo)

            con.send(bytes("1", "utf-8"))

    s.close()


def enviar():  # envio de ...
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("the socket has been created")
    try:
        s.bind((HOST2, int(PORT2)))
    except Exception as e:
        print(e)
        sys.exit()
    print("the socket has been bounded >:c")
    s.listen()
    print("The socket is listening")
    conn, address=s.accept()
    print("Si se conecto")
    while(True):
        try:
            nombre_archivo=str(conn.recv(200), encoding = "utf-8")
            archivo=open(dirInicial + '/' + nombre_archivo, "br")
            conn.send(bytes(str(len(archivo)), "utf-8"))

            con.recv(1)
            conn.send(bytes(archivo.read(), "utf-8"))
            del(archivo)

        except Exception as e:
            print(e)
            s.shutdown(socket.SHUT_RDWR)






def main():
    create_folder("DATA")
    hilo_recibir=threading.Thread(target = recibir, args = ())
    hilo_recibir.start()
    hilo_enviar=threading.Thread(target = enviar, args = ())
    hilo_enviar.start()


main()
