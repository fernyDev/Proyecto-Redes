import os
import socket
import threading
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def envio(archivo, tamano, index, sock):
    if index == 0:
        archivo.seek(index)
    else:
        archivo.seek(tamano[index - 1])
    datos = archivo.read(tamano[index])
    sock.sendall(datos)

#Funcion del hilo que cargara los archivos
def upload_file(sock, ip, port, files, tamano):
    sock.connect((ip, puerto))
    for i in range(len(files)):
        for j in range(4):
            sock.send(bytes("True","utf-8"))
            numero = s.recv(1)
            sock.send(bytes(str(len(files[i])), "utf-8"))
            numero = s.recv(1)
            sock.send(bytes(files[i], "utf-8"))
            numero = s.recv(1)
            sock.send(bytes(app.config['UPLOAD_FOLDER'],"utf-8"))
            numero = s.recv(1)
            envio(files[i],tamano[i], j,sock)
            numero = s.recv(1)
    sock.send(bytes("False", "UTF-8"))

# Funcion que ayuda a iniciar los hilos para conectarse a los 
# clientes que recibirán los archivos
def upload_files(files):
    tamano = [][]
    ips = ["192.168.0.1", "192.168.2.1", "192.168.3.2", "192.168.4.2"]
    puerto = 3030
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for j in range(len(files)): 
        tam = len(files[i].read())
        for k in range(4):
            tamano[j].append(int(tam/4))
            tamano[j].append(tamano[j][0]*2)
            tamano[j].append(tamano[j][0]*3)
            tamano[j].append(int(tam)-(tamano[j][0]*3))

    for i in range(len(ips))
        t = threading.Thread(target = upload_file, args=(sock, ips[i], puerto, files, tamano))
        t.start()

# Funcion que discrimina los directorios
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Funcion que ayuda a detener el servidor cuando no se puede enviar la SIGNAL de Ctrl + C
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    uploaded_files(filenames)
    return render_template('upload.html', filenames=filenames)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == '__main__':
    app.run( host="0.0.0.0", port=int("80"), debug=True)
