import json
import os
import hashlib

# Carpeta raiz del proyecto (un nivel arriba de /modulos), para que los JSON
# se encuentren sin importar desde donde se ejecute el programa.
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARCHIVO_USUARIOS = os.path.join(RUTA_BASE, "usuarios.json")
ARCHIVO_HERRAMIENTAS = os.path.join(RUTA_BASE, "herramientas.json")
ARCHIVO_PRESTAMOS = os.path.join(RUTA_BASE, "prestamos.json")
ARCHIVO_LOG = os.path.join(RUTA_BASE, "errores.log")

FORMATO_FECHA = "%d/%m/%y"


def cargar_json(ruta):
    """Devuelve la lista guardada en el archivo, o [] si no existe o esta vacio.
    Si el archivo esta corrupto lanza json.JSONDecodeError para no sobreescribirlo."""
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
    if not contenido:
        return []
    return json.loads(contenido)


def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def siguiente_id(datos):
    if not datos:
        return 1
    return max(registro["id"] for registro in datos) + 1


def encriptar_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode("utf-8")).hexdigest()
