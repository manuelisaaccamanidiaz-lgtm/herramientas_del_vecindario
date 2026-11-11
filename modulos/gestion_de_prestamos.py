import json
from datetime import datetime
import registro_de_eventos
from datos import (ARCHIVO_PRESTAMOS, ARCHIVO_HERRAMIENTAS, ARCHIVO_USUARIOS,
                   FORMATO_FECHA, cargar_json, guardar_json, siguiente_id)

MODULO = "gestion_de_prestamos"
ESTADO_EN_USO = "en uso"
ESTADO_DEVUELTO = "devuelto"


def _pedir_fecha(mensaje):
    """Pide una fecha en formato DD/MM/AA. Lanza ValueError si es invalida."""
    texto = input(mensaje).strip()
    return datetime.strptime(texto, FORMATO_FECHA)


def crear_prestamos(usuario_sesion=None):
    """Registra un prestamo. Si se pasa usuario_sesion (residente) el prestamo
    queda a su nombre; si no, se pregunta el usuario (admin)."""
    try:
        datos_actuales = cargar_json(ARCHIVO_PRESTAMOS)
        herramientas = cargar_json(ARCHIVO_HERRAMIENTAS)
        usuarios = cargar_json(ARCHIVO_USUARIOS)

        if usuario_sesion:
            usuario = usuario_sesion
        else:
            usuario = input("ingrese el usuario: ").strip().lower()
            if not any(u.get("usuario") == usuario for u in usuarios):
                print("el usuario no existe")
                return

        nombre_herramienta = input("ingrese la herramienta deseada: ").strip().lower()
        herramienta = next((h for h in herramientas if h["nombre"] == nombre_herramienta), None)
        if herramienta is None:
            print("la herramienta no existe")
            return

        cantidad = int(input("ingrese la cantidad deseada: "))
        if cantidad <= 0:
            print("la cantidad debe ser mayor a 0")
            return
        if herramienta["cantidad"] < cantidad:
            print(f"no hay stock suficiente, disponibles: {herramienta['cantidad']}")
            return

        fecha_de_inicio = _pedir_fecha("ingrese la fecha de inicio del prestamo(formato DD/MM/AA): ")
        fecha_estimada_devolucion = _pedir_fecha("ingrese la fecha estimada de devolucion(formato DD/MM/AA): ")
        if fecha_estimada_devolucion < fecha_de_inicio:
            print("la fecha de devolucion no puede ser anterior a la de inicio")
            return
        observaciones = input("ingrese alguna observacion que desea hacer(esta campo no es obligatorio): ")

        datos_prestamos = {
            "usuario": usuario,
            "herramienta": nombre_herramienta,
            "cantidad": cantidad,
            "fecha de inicio": fecha_de_inicio.strftime(FORMATO_FECHA),
            "fecha estimada de devolucion": fecha_estimada_devolucion.strftime(FORMATO_FECHA),
            "estado": ESTADO_EN_USO,
            "observaciones": observaciones,
            "id": siguiente_id(datos_actuales)}

        # Descontar del stock y guardar ambos archivos
        herramienta["cantidad"] -= cantidad
        datos_actuales.append(datos_prestamos)
        guardar_json(ARCHIVO_HERRAMIENTAS, herramientas)
        guardar_json(ARCHIVO_PRESTAMOS, datos_actuales)
        print(f"prestamo creado exitosamente! ID del prestamo: {datos_prestamos['id']}")

    except ValueError as ve:
        registro_de_eventos.registrar_error(MODULO, "Valor invalido al crear prestamo", ve)
        print("se introdujo un valor invalido (cantidad numerica y fechas DD/MM/AA) intente de nuevo")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "Archivo JSON corrupto al crear prestamo", je)
        print("uno de los archivos JSON esta corrupto, revise su contenido")
    except PermissionError as pe:
        registro_de_eventos.registrar_error(MODULO, "Sin permisos para escribir prestamos.json", pe)
        print("no cuenta con los permisos necesarios para registrar prestamos.")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al crear prestamo", e)
        print(f"se produjo un error inesperado: {e}")


def Disponibilidad_stock():
    try:
        herramienta_deseada = input("ingrese la herramienta que necesita: ").strip().lower()
        cantidad_deseada = int(input("ingrese la cantidad que necesita: "))
        herramientas = cargar_json(ARCHIVO_HERRAMIENTAS)

        herramienta = next((h for h in herramientas if h["nombre"] == herramienta_deseada), None)
        if herramienta is None:
            print("la herramienta no existe")
        elif herramienta["cantidad"] >= cantidad_deseada:
            print(f"Sí hay stock (disponibles: {herramienta['cantidad']})")
        else:
            print(f"No hay stock suficiente (disponibles: {herramienta['cantidad']})")

    except ValueError as ve:
        registro_de_eventos.registrar_error(MODULO, "Cantidad no numerica en disponibilidad", ve)
        print("la cantidad debe ser numerica")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "herramientas.json esta corrupto", je)
        print(f"error en el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado en disponibilidad", e)
        print(f"se produjo un error inesperado: {e}")


def devoluciones(usuario_sesion=None):
    """Marca un prestamo como devuelto y regresa la cantidad al stock.
    Un residente (usuario_sesion) solo puede devolver sus propios prestamos."""
    try:
        prestamos = cargar_json(ARCHIVO_PRESTAMOS)
        herramientas = cargar_json(ARCHIVO_HERRAMIENTAS)

        pendientes = [p for p in prestamos
                      if p["estado"] == ESTADO_EN_USO
                      and (usuario_sesion is None or p["usuario"] == usuario_sesion)]
        if not pendientes:
            print("no hay prestamos pendientes por devolver")
            return

        print("prestamos pendientes:")
        for p in pendientes:
            print(f"ID {p['id']}: {p['herramienta']} x{p['cantidad']} - {p['usuario']} "
                  f"(devolver antes de {p['fecha estimada de devolucion']})")

        id_buscar = int(input("ingrese el ID del prestamo a devolver: "))
        prestamo = next((p for p in pendientes if p["id"] == id_buscar), None)
        if prestamo is None:
            print("prestamo no encontrado o ya devuelto")
            return

        prestamo["estado"] = ESTADO_DEVUELTO
        prestamo["fecha de devolucion"] = datetime.now().strftime(FORMATO_FECHA)

        herramienta = next((h for h in herramientas if h["nombre"] == prestamo["herramienta"]), None)
        if herramienta is not None:
            herramienta["cantidad"] += prestamo["cantidad"]
            guardar_json(ARCHIVO_HERRAMIENTAS, herramientas)
        else:
            print("aviso: la herramienta ya no existe en el inventario, no se actualizo el stock")

        guardar_json(ARCHIVO_PRESTAMOS, prestamos)
        print("devolucion registrada correctamente")

    except ValueError as ve:
        registro_de_eventos.registrar_error(MODULO, "ID no numerico en devolucion", ve)
        print("el ID debe ser numerico")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "Archivo JSON corrupto en devolucion", je)
        print(f"error en el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado en devolucion", e)
        print(f"se produjo un error inesperado: {e}")
