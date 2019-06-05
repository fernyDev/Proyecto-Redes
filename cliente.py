import socket
import sys
import threading
import os
from os.path import expanduser

HOST = '192.168.4.30'  # The server's hostname or IP address
PORT1 = '3030'         # The port used by the server
PORT2 = '3031'
PORT3 = '3032'
dirInicial = expanduser("~") + '/DATA'

def create_folder(nombre_carpeta):
    carpeta = expanduser("~") +'/'+ nombre_carpeta
    if not os.path.exists(carpeta):
        os.mkdir(carpeta)
    return carpeta

def largo_archivo(path):
    f=open(path, "rb")
    tamano_archivo=1
    byte=f.read(1)
    while byte:
        tamano_archivo+=1
        byte = f.read(1)
        #print(byte,end=" ")
    print("")
    print("Largo del archivo: "+str(tamano_archivo))
    f.close()
    return(tamano_archivo)

def recibir():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", int(PORT1)))
    s.listen()
    print("Esperando conexion")
    con,direccion = s.accept()
    print("Conexion establecida con " + direccion[0])
    while(True):
        estado = str(con.recv(5),encoding="utf-8")
        if estado == "True":
            con.send(bytes("1","utf-8"))
            tam = int(str(con.recv(20),encoding="utf-8"))

            con.send(bytes("1","utf-8"))
            nombre_archivo = str(con.recv(200),encoding="utf-8")

            con.send(bytes("1","utf-8"))
            archivo_nuevo = open(dirInicial + "/" + nombre_archivo)
            info = con.recv(tam)
            if len(info)==tam:
                print("Ahuevo, si lo recibio enterito")
            else:
                print("No es igual :'v info= " + str(len(info)) + "\ttam= " + str(tam))
            archivo_nuevo.write(info)
            del(info)
            archivo_nuevo.close()
            del(archivo_nuevo)

            con.send(bytes("1","utf-8"))

    s.close()

def enviar():#ensamblado de archivos y envio de pc1 al servidor http
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("the sockets have been created")
    try:
        s.bind((HOST, int(PORT3)))
        s2.bind((HOST, int(PORT2)))
    except Exception as e:
        print(e)
        #sys.exit()
    print("the sockets have been bounded >:c")
    s.listen()
    s2.listen()
    print("The sockets are listening")

    #conexión y recibido del nombre del archivo del servidor http
    conni,addri=s2.accept()
    data=conni.recv(1024)
    nombre_archivo = str(conni.recv(200),encoding='utf-8')

    #crear el folder para el envío
    directorio = create_folder("archivos_para_enviar")

    #leo pedazo 1 de archivo
    f = open(dirInicial + "/" + nombre_archivo,'rb')#
    buffer=f.read()
    f.close()

    #escribo pedazo 1 de archivo
    archivo_nuevo = open(directorio+"/"+nombre_archivo,'ab')
    archivo_nuevo.write(buffer)
    archivo_nuevo.close()

    connections=[None]*3
    addresses=[None]*3
    for i in range(3):
        try:
            connections[i+1], addresses[i+1] = s.accept()
            connections[i+1].sendall(nombre_archivo.encode())#envio nombre del archivo
            data = connections[i+1].recv(1024)#recibo tamaño del pedazo de archivo
            connections[i+1].sendall(1)#envio un 1
            

            #ensamblar los put*s archivos
            
            f2=open(directorio+"/"+nombre_archivo,'ab')
            paquete = connections[i+1].recv(1024)
            f2.write(paquete)
            while paquete:
                paquete = connections[i+1].recv(1024)
                f2.write(paquete)
            f2.close()
        except Exception as e:
            print(e)
            print("Error en PC: "+str(i+2))
            s.shutdown(socket.SHUT_RDWR)#mato al socket? D:

    #elimino el archivo en la carpeta inicial ... rmtree() para eliminar una carpeta >:P     
    os.remove(dirInicial + "/" + nombre_archivo)

    #EL ENVIO DE LA PORKERIA AL SERVIDOR HTTP

    #enviar tamaño del put* archivo
    tamanio = largo_archivo(directorio+"/"+nombre_archivo)
    conni.sendall(tamanio.encode())

    #le envío al http el tamaño del put* archivo
    f3=open(directorio+"/"+nombre_archivo,'rb')
    paquete = f3.read()
    conni.sendall(paquete)
    f3.close()


    
    

    



def main():
    create_folder("DATA")
    hilo_recibir=threading.Thread(target=recibir, args=())
    hilo_recibir.start()
    hilo_enviar=threading.Thread(target=enviar, args=())
    hilo_enviar.start()


main()
