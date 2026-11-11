import json
import registro_de_eventos
from datos import ARCHIVO_HERRAMIENTAS, cargar_json, guardar_json, siguiente_id

MODULO = "gestion_de_herramientas"


def crear_herramientas():
    try:
        datos_actuales = cargar_json(ARCHIVO_HERRAMIENTAS)

        nombre = input("ingrese el nombre de la herramienta: ").strip().lower()
        if not nombre:
            print("el nombre es obligatorio")
            return
        categoria = input("ingrese la categoria de la herramienta: ").strip().lower()
        cantidad = int(input("ingrese la cantidad de esta herramienta disponible: "))
        if cantidad < 0:
            print("la cantidad no puede ser negativa")
            return
        estado = input("ingrese el estado de la herramienta: ").strip().lower()
        valor = float(input("ingrese el valor estimado de la herramienta: "))

        datos_herramientas = {
            "nombre": nombre,
            "categoria": categoria,
            "cantidad": cantidad,
            "estado": estado,
            "valor": valor,
            "id": siguiente_id(datos_actuales)}

        datos_actuales.append(datos_herramientas)
        guardar_json(ARCHIVO_HERRAMIENTAS, datos_actuales)
        print("herramienta creada exitosamente!")

    except ValueError as ve:
        registro_de_eventos.registrar_error(MODULO, "Valor invalido al crear herramienta", ve)
        print("se introdujo un valor invalido intente de nuevo")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "herramientas.json esta corrupto", je)
        print("el archivo herramientas.json esta corrupto, revise su contenido")
    except PermissionError as pe:
        registro_de_eventos.registrar_error(MODULO, "Sin permisos para escribir herramientas.json", pe)
        print("no cuenta con los permisos necesarios para agregar herramientas.")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al crear herramienta", e)
        print(f"se produjo un error inesperado: {e}")


def listar_herramientas():
    try:
        herramientas = cargar_json(ARCHIVO_HERRAMIENTAS)
        if not herramientas:
            print("no hay herramientas registradas")
            return
        for herramienta in herramientas:
            print(herramienta)
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "herramientas.json esta corrupto", je)
        print(f"Error al leer el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al listar herramientas", e)
        print(f"Error inesperado en lectura JSON: {e}")


def buscar_herramienta():
    try:
        busqueda = input("ingrese lo que quiere buscar: ").lower()
        herramientas = cargar_json(ARCHIVO_HERRAMIENTAS)
        encontrado = False
        for herramienta in herramientas:
            for valor in herramienta.values():
                if busqueda in str(valor).lower():
                    print(herramienta)
                    encontrado = True
                    break

        if not encontrado:
            print("no se encontraron coincidencias")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "herramientas.json esta corrupto", je)
        print(f"error en el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al buscar herramienta", e)
        print(f"se produjo un error inesperado: {e}")


def actualizar_herramienta():
    try:
        id_buscar = int(input("ingrese el ID de la herramienta a actualizar: "))
        campo = input("ingrese el campo a modificar (nombre,categoria,cantidad,estado,valor): ").strip().lower()
        if campo == "id":
            print("el ID no se puede modificar")
            return
        nuevo_valor = input("ingrese el nuevo valor: ").strip()

        herramientas = cargar_json(ARCHIVO_HERRAMIENTAS)

        herramienta_objetivo = next((h for h in herramientas if h["id"] == id_buscar), None)
        if herramienta_objetivo is None:
            print("herramienta no encontrada")
            return
        if campo not in herramienta_objetivo:
            print("el campo no existe")
            return

        # Mantener el tipo de dato correcto de cada campo
        if campo == "cantidad":
            nuevo_valor = int(nuevo_valor)
            if nuevo_valor < 0:
                print("la cantidad no puede ser negativa")
                return
        elif campo == "valor":
            nuevo_valor = float(nuevo_valor)
        else:
            nuevo_valor = nuevo_valor.lower()

        herramienta_objetivo[campo] = nuevo_valor
        guardar_json(ARCHIVO_HERRAMIENTAS, herramientas)
        print("herramienta actualizada correctamente")

    except ValueError as ve:
        registro_de_eventos.registrar_error(MODULO, "Valor no numerico al actualizar herramienta", ve)
        print("el ID, la cantidad y el valor deben ser numericos")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "herramientas.json esta corrupto", je)
        print(f"error en el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al actualizar herramienta", e)
        print(f"se produjo un error inesperado: {e}")


def eliminar_herramientas():
    try:
        id_buscar = int(input("ingrese el ID de la herramienta a eliminar: "))

        herramientas = cargar_json(ARCHIVO_HERRAMIENTAS)

        herramientas_filtrados = []
        eliminado = False

        for herramienta in herramientas:
            if herramienta["id"] == id_buscar:
                eliminado = True
            else:
                herramientas_filtrados.append(herramienta)

        if eliminado:
            guardar_json(ARCHIVO_HERRAMIENTAS, herramientas_filtrados)
            print("herramienta eliminada correctamente")
        else:
            print("herramienta no encontrada")

    except ValueError as ve:
        registro_de_eventos.registrar_error(MODULO, "ID no numerico al eliminar herramienta", ve)
        print("el ID debe ser numerico")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "herramientas.json esta corrupto", je)
        print(f"error en el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al eliminar herramienta", e)
        print(f"se produjo un error inesperado: {e}")
