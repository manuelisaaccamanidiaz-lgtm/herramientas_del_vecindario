import json
import registro_de_eventos
from datos import ARCHIVO_HERRAMIENTAS, ARCHIVO_PRESTAMOS, cargar_json

MODULO = "consultas_y_reportes"
STOCK_MINIMO = 2


def check_stock():
    try:
        herramientas = cargar_json(ARCHIVO_HERRAMIENTAS)

        hay_bajo = False
        for herramienta in herramientas:
            if herramienta["cantidad"] <= STOCK_MINIMO:
                print(f"La herramienta {herramienta['nombre']} tiene stock bajo ({herramienta['cantidad']})")
                hay_bajo = True
        if not hay_bajo:
            print("ninguna herramienta tiene stock bajo")

    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "herramientas.json esta corrupto", je)
        print(f"Error al leer el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado en check_stock", e)
        print(f"Error inesperado: {e}")


def reporte_prestamos():
    try:
        prestamos = cargar_json(ARCHIVO_PRESTAMOS)

        activos = [p for p in prestamos if p["estado"] == "en uso"]
        if not activos:
            print("no hay prestamos activos")
        for prestamo in activos:
            print(prestamo)

    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "prestamos.json esta corrupto", je)
        print(f"Error al leer el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado en reporte_prestamos", e)
        print(f"Error inesperado: {e}")


def historial_usuario(usuario=None):
    try:
        if usuario is None:
            usuario = input("ingrese el nombre de usuario: ").strip().lower()

        prestamos = cargar_json(ARCHIVO_PRESTAMOS)

        historial = [p for p in prestamos if p["usuario"] == usuario]
        if not historial:
            print("este usuario no tiene prestamos registrados")
        for prestamo in historial:
            print(prestamo)

    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "prestamos.json esta corrupto", je)
        print(f"Error al leer el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado en historial_usuario", e)
        print(f"Error inesperado: {e}")


def herramientas_mas_prestadas():
    try:
        contador_herramientas = {}

        prestamos = cargar_json(ARCHIVO_PRESTAMOS)
        for prestamo in prestamos:
            nombre_herramienta = prestamo["herramienta"]

            if nombre_herramienta in contador_herramientas:
                contador_herramientas[nombre_herramienta] += 1
            else:
                contador_herramientas[nombre_herramienta] = 1

        herramientas_ordenadas = sorted(
            contador_herramientas.items(),
            key=lambda x: x[1],
            reverse=True
        )

        if not herramientas_ordenadas:
            print("aun no hay prestamos registrados")
            return
        print("Herramientas más prestadas:")
        for herramienta, cantidad in herramientas_ordenadas:
            print(f"{herramienta}: {cantidad} veces")

    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "prestamos.json esta corrupto", je)
        print(f"Error al leer el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado en herramientas_mas_prestadas", e)
        print(f"Error inesperado en lectura JSON: {e}")


def usuarios_que_mas_prestan():
    try:
        contador_usuarios = {}
        prestamos = cargar_json(ARCHIVO_PRESTAMOS)
        for prestamo in prestamos:
            nombre_usuario = prestamo["usuario"]
            if nombre_usuario in contador_usuarios:
                contador_usuarios[nombre_usuario] += 1
            else:
                contador_usuarios[nombre_usuario] = 1
        usuarios_ordenados = sorted(contador_usuarios.items(), key=lambda x: x[1], reverse=True)
        if not usuarios_ordenados:
            print("aun no hay prestamos registrados")
            return
        print("Usuarios que más prestan:")
        for usuario, cantidad in usuarios_ordenados:
            print(f"{usuario}: {cantidad} prestamos")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "prestamos.json esta corrupto", je)
        print(f"Error al leer el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado en usuarios_que_mas_prestan", e)
        print(f"Error inesperado en lectura JSON: {e}")
