# errores.py
from datetime import datetime
from datos import ARCHIVO_LOG


def registrar_error(modulo, mensaje, error=None):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    detalle = f" -> {type(error).__name__}: {error}" if error else ""

    try:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{fecha}] {modulo}: {mensaje}{detalle}\n")
    except OSError:
        # Si no se puede escribir el log no debe caerse el programa
        pass
