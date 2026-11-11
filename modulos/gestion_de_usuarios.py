import json
import registro_de_eventos
from datos import ARCHIVO_USUARIOS, cargar_json, guardar_json, siguiente_id, encriptar_contraseña

MODULO = "gestion_de_usuarios"
CARGOS_VALIDOS = ("admin", "residente")


def crear_usuarios():
    try:
        datos_actuales = cargar_json(ARCHIVO_USUARIOS)

        usuario = input("ingrese el nombre de usuario (para iniciar sesion): ").strip().lower()
        if not usuario:
            print("el nombre de usuario es obligatorio")
            return
        if any(u.get("usuario") == usuario for u in datos_actuales):
            print("ese nombre de usuario ya existe")
            return
        nombre = input("ingrese el nombre del usuario: ").strip().capitalize()
        apellidos = input("ingrese el apellido del usuario: ").strip().capitalize()
        telefono = input("ingrese el telefono de usuario: ").strip()
        if not telefono.isdigit():
            print("solo se pueden ingresar numeros")
            return
        direccion = input("ingrese la direccion del usuario: ").strip()
        tipo_de_usuario = input("cual es el cargo de este usuario (admin/residente): ").strip().lower()
        if tipo_de_usuario not in CARGOS_VALIDOS:
            print("cargo invalido, debe ser admin o residente")
            return
        contraseña = input("ingrese la contraseña: ")
        if not contraseña:
            print("la contraseña es obligatoria")
            return

        datos_usuarios = {
            "usuario": usuario,
            "nombre": nombre,
            "apellidos": apellidos,
            "telefono": telefono,
            "direccion": direccion,
            "cargo": tipo_de_usuario,
            "contraseña": encriptar_contraseña(contraseña),
            "id": siguiente_id(datos_actuales)}

        datos_actuales.append(datos_usuarios)
        guardar_json(ARCHIVO_USUARIOS, datos_actuales)
        print("usuario creado exitosamente!")

    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "usuarios.json esta corrupto", je)
        print("el archivo usuarios.json esta corrupto, revise su contenido")
    except PermissionError as pe:
        registro_de_eventos.registrar_error(MODULO, "Sin permisos para escribir usuarios.json", pe)
        print("no cuenta con los permisos necesarios para agregar usuarios.")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al crear usuario", e)
        print(f"se produjo un error inesperado: {e}")


def listar_usuarios():
    try:
        usuarios = cargar_json(ARCHIVO_USUARIOS)
        if not usuarios:
            print("no hay usuarios registrados")
            return
        for usuario in usuarios:
            datos_visibles = {k: v for k, v in usuario.items() if k != "contraseña"}
            print(datos_visibles)
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "usuarios.json esta corrupto", je)
        print(f"Error al leer el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al listar usuarios", e)
        print(f"Error inesperado en lectura JSON: {e}")


def buscar_usuario():
    try:
        busqueda = input("ingrese lo que quiere buscar: ").lower()
        usuarios = cargar_json(ARCHIVO_USUARIOS)
        encontrado = False
        for usuario in usuarios:
            for campo, valor in usuario.items():
                if campo != "contraseña" and busqueda in str(valor).lower():
                    print({k: v for k, v in usuario.items() if k != "contraseña"})
                    encontrado = True
                    break

        if not encontrado:
            print("no se encontraron coincidencias")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "usuarios.json esta corrupto", je)
        print(f"error en el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al buscar usuario", e)
        print(f"se produjo un error inesperado: {e}")


def actualizar_usuarios():
    try:
        id_buscar = int(input("ingrese el ID del usuario a actualizar: "))
        campo = input("ingrese el campo a modificar (usuario, nombre, apellidos, telefono, direccion, cargo, contraseña): ").strip().lower()
        if campo == "id":
            print("el ID no se puede modificar")
            return
        nuevo_valor = input("ingrese el nuevo valor: ").strip()

        usuarios = cargar_json(ARCHIVO_USUARIOS)

        usuario_objetivo = next((u for u in usuarios if u["id"] == id_buscar), None)
        if usuario_objetivo is None:
            print("usuario no encontrado")
            return
        if campo not in usuario_objetivo:
            print("el campo no existe")
            return

        # Validar y convertir el valor segun el campo
        if campo == "telefono" and not nuevo_valor.isdigit():
            print("solo se pueden ingresar numeros")
            return
        if campo == "cargo":
            nuevo_valor = nuevo_valor.lower()
            if nuevo_valor not in CARGOS_VALIDOS:
                print("cargo invalido, debe ser admin o residente")
                return
        if campo == "usuario":
            nuevo_valor = nuevo_valor.lower()
            if any(u.get("usuario") == nuevo_valor and u["id"] != id_buscar for u in usuarios):
                print("ese nombre de usuario ya existe")
                return
        if campo in ("nombre", "apellidos"):
            nuevo_valor = nuevo_valor.capitalize()
        if campo == "contraseña":
            nuevo_valor = encriptar_contraseña(nuevo_valor)

        usuario_objetivo[campo] = nuevo_valor
        guardar_json(ARCHIVO_USUARIOS, usuarios)
        print("usuario actualizado correctamente")

    except ValueError as ve:
        registro_de_eventos.registrar_error(MODULO, "ID no numerico al actualizar", ve)
        print("el ID debe ser numerico")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "usuarios.json esta corrupto", je)
        print(f"error en el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al actualizar usuario", e)
        print(f"se produjo un error inesperado: {e}")


def eliminar_usuarios():
    try:
        id_buscar = int(input("ingrese el ID del usuario a eliminar: "))

        usuarios = cargar_json(ARCHIVO_USUARIOS)

        usuarios_filtrados = []
        eliminado = False

        for usuario in usuarios:
            if usuario["id"] == id_buscar:
                eliminado = True
            else:
                usuarios_filtrados.append(usuario)

        if eliminado:
            guardar_json(ARCHIVO_USUARIOS, usuarios_filtrados)
            print("usuario eliminado correctamente")
        else:
            print("usuario no encontrado")

    except ValueError as ve:
        registro_de_eventos.registrar_error(MODULO, "ID no numerico al eliminar", ve)
        print("el ID debe ser numerico")
    except json.JSONDecodeError as je:
        registro_de_eventos.registrar_error(MODULO, "usuarios.json esta corrupto", je)
        print(f"error en el archivo JSON: {je}")
    except Exception as e:
        registro_de_eventos.registrar_error(MODULO, "Error inesperado al eliminar usuario", e)
        print(f"se produjo un error inesperado: {e}")
