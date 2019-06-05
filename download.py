import socket
import os
import threading
import sys
from progress.bar import Bar, ChargingBar

#bar2 = ChargingBar('Instalando:', max=100)
#for num in range(100):
#    time.sleep(random.uniform(0, 0.2))
#    bar2.next()
#bar2.finish()

def main():
    puerto = 3030
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("",puerto))
    s.listen()
    try:
        while(True):
            print("Esperando conexion...")
            conexion, direccion = s.accept()
            print("Conexion establecida con " + direccion[0])
            if not os.path.exists(direccion[0]):
                os.mkdir(direccion[0])
            hilo = threading.Thread(target=descargar, args=(conexion,direccion))
            hilo.start()
            print("Se salio del hilo")
    except KeyboardInterrupt:
        print("Cerrando conexiones")
        conexion.close()
        s.close()

def cargar(con,archivo,tam,bar):
    Bytes=512
    if(Bytes<tam):
        Bytes=tam
    contador=0
    while(True):
        data = con.recv(Bytes)
        contador = len(data) + contador
        
        archivo.write(data)
        bar.next(len(data))
        tam = tam-len(data)
        while(data):
            data = con.recv(tam)
            
            contador = len(data) + contador
            archivo.write(data)
            bar.next(len(data))
            tam = tam - len(data)
        break

    return archivo,contador

def descargar(con,addr):

    estado = con.recv(5)
    estado = str(estado,encoding="utf-8")
    
    while(estado=="True"):
        con.send(bytes("1","utf-8"))
        print("Esperando archivos del " + addr[0])
        tam = con.recv(20)
        tam = int(str(tam,encoding="utf-8"))
        print("Tamano del archivo",tam)
        bar = ChargingBar("Descargando:",max=tam)
        #Enviar un bit de espera
        con.send(bytes("1","utf-8"))

        contador = 0
        #Recibe el nombre del archivo
        nombre = con.recv(100)
        nombre = str(nombre,encoding="utf-8")
        print("Nombre del archivo:"+nombre)

        con.send(bytes("1","utf-8"))

        #Se recibe la ruta
        ruta = con.recv(100)
        ruta = str(ruta,encoding="utf-8")
        #if not os.path.exists(addr[0] +ruta):
        #    os.makedirs(addr[0]+ruta)
        #    print("Se creo la carpeta:"+addr[0]+ruta)

        con.send(bytes("1","utf-8"))

        #Se calcula el tamano del archivo separado
        tamano = []
        tamano.append(int(tam/4))
        tamano.append(tam-(tamano[0]*3))
        print(tamano)
        #Recibe parte del documento definido en tam
        #archivo = open(addr[0] + ruta + nombre,"wb")
        archivo = open(addr[0] + "/" + nombre,"wb")
        archivo,contador = cargar(con,archivo,tamano[0],bar)
        #print("Segun, ya se envio con un tamaño de =",contador,
        #    "Deberia ser igual a",tamano[0])

        con.send(bytes("1","utf-8"))

        archivo,contador = cargar(con,archivo,tamano[0],bar)
        #print("Segun, ya se envio con un tamaño de =",contador,
        #    "Deberia ser igual a",tamano[0])

        con.send(bytes("1","utf-8"))

        archivo,contador = cargar(con,archivo,tamano[0],bar)
        #print("Segun, ya se envio con un tamaño de =",contador,
        #    "Deberia ser igual a",tamano[0])

        con.send(bytes("1","utf-8"))

        archivo,contador = cargar(con,archivo,tamano[1],bar)
        #print("Segun, ya se envio con un tamaño de =",contador,
        #   "Deberia ser igual a",tamano[1])

        con.send(bytes("1","utf-8"))

        archivo.close()
        bar.finish()
        del (archivo)
        print("Se cerro el archivo")
        estado = con.recv(5)
        try:
            estado = str(estado,encoding="utf-8")
        except UnicodeDecodeError:
            print("Estado sin decodificar",estado)
            estado = "True"
        print("Estado = "+estado+"\tTamano =",len(estado))
        print("Ya valio")
    print("Se salio del While")
    con.close()
    exit(0)

if __name__ == "__main__":
    main()
