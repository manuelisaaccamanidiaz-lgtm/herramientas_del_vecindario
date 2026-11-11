import json
import time
import gestion_de_herramientas
import gestion_de_usuarios
import gestion_de_prestamos
import registro_de_eventos
import consultas_y_reportes
from datos import ARCHIVO_USUARIOS, cargar_json, encriptar_contraseña

MODULO = "permisos_a_manejar"


def iniciar_sesion():
    """Pide usuario y contraseña. Devuelve el usuario encontrado o None."""
    print("---inicio de sesion---")
    usuario = input("ingrese su usuario: ").strip().lower()
    contraseña = input("ingrese su contraseña: ")

    usuarios = cargar_json(ARCHIVO_USUARIOS)
    contraseña_cifrada = encriptar_contraseña(contraseña)
    for u in usuarios:
        if u.get("usuario") == usuario and u.get("contraseña") == contraseña_cifrada:
            return u
    return None


def leer_opcion():
    return int(input("ingrese su opcion: "))


def menu_herramientas():
    print("que desea hacer: ")
    print("1. crear herramientas")
    print("2. listar herramientas")
    print("3. buscar herramientas")
    print("4. actualizar herramientas")
    print("5. eliminar herramientas")
    opcion = leer_opcion()
    if opcion == 1:
        gestion_de_herramientas.crear_herramientas()
    elif opcion == 2:
        gestion_de_herramientas.listar_herramientas()
    elif opcion == 3:
        gestion_de_herramientas.buscar_herramienta()
    elif opcion == 4:
        gestion_de_herramientas.actualizar_herramienta()
    elif opcion == 5:
        gestion_de_herramientas.eliminar_herramientas()
    else:
        print("opcion invalida")


def menu_usuarios():
    print("que desea hacer: ")
    print("1. crear usuarios")
    print("2. listar usuarios")
    print("3. buscar usuarios")
    print("4. actualizar usuarios")
    print("5. eliminar usuarios")
    opcion = leer_opcion()
    if opcion == 1:
        gestion_de_usuarios.crear_usuarios()
    elif opcion == 2:
        gestion_de_usuarios.listar_usuarios()
    elif opcion == 3:
        gestion_de_usuarios.buscar_usuario()
    elif opcion == 4:
        gestion_de_usuarios.actualizar_usuarios()
    elif opcion == 5:
        gestion_de_usuarios.eliminar_usuarios()
    else:
        print("opcion invalida")


def menu_prestamos():
    print("que desea hacer: ")
    print("1. peticion de prestamo")
    print("2. disponibilidad y stock")
    print("3. devoluciones")
    print("4. consultas y reportes")
    opcion = leer_opcion()
    if opcion == 1:
        gestion_de_prestamos.crear_prestamos()
    elif opcion == 2:
        gestion_de_prestamos.Disponibilidad_stock()
    elif opcion == 3:
        gestion_de_prestamos.devoluciones()
    elif opcion == 4:
        menu_reportes()
    else:
        print("opcion invalida")


def menu_reportes():
    print("1. reporte de prestamos")
    print("2. historial de usuario")
    print("3. herramientas mas prestadas")
    print("4. usuarios que mas prestan")
    print("5. herramientas con stock bajo")
    opcion = leer_opcion()
    if opcion == 1:
        consultas_y_reportes.reporte_prestamos()
    elif opcion == 2:
        consultas_y_reportes.historial_usuario()
    elif opcion == 3:
        consultas_y_reportes.herramientas_mas_prestadas()
    elif opcion == 4:
        consultas_y_reportes.usuarios_que_mas_prestan()
    elif opcion == 5:
        consultas_y_reportes.check_stock()
    else:
        print("opcion invalida")


def menu_admin():
    """Devuelve True cuando el usuario elige salir."""
    print("\nbienvenido al sistema Administrador")
    print("que desea hacer: ")
    print("1. gestionar herramientas")
    print("2. gestionar usuarios")
    print("3. gestionar prestamos")
    print("4. consultas y reportes")
    print("5. salir")
    opcion = leer_opcion()
    if opcion == 1:
        menu_herramientas()
    elif opcion == 2:
        menu_usuarios()
    elif opcion == 3:
        menu_prestamos()
    elif opcion == 4:
        menu_reportes()
    elif opcion == 5:
        return True
    else:
        print("opcion invalida")
    return False


def menu_residente(usuario):
    """Devuelve True cuando el usuario elige salir."""
    print("\nbienvenido al sistema Residente")
    print("que desea hacer: ")
    print("1. listar herramientas")
    print("2. buscar herramientas")
    print("3. peticion de prestamo")
    print("4. disponibilidad y stock")
    print("5. devolución de herramientas")
    print("6. salir")
    opcion = leer_opcion()
    if opcion == 1:
        gestion_de_herramientas.listar_herramientas()
    elif opcion == 2:
        gestion_de_herramientas.buscar_herramienta()
    elif opcion == 3:
        gestion_de_prestamos.crear_prestamos(usuario_sesion=usuario["usuario"])
    elif opcion == 4:
        gestion_de_prestamos.Disponibilidad_stock()
    elif opcion == 5:
        gestion_de_prestamos.devoluciones(usuario_sesion=usuario["usuario"])
    elif opcion == 6:
        return True
    else:
        print("opcion invalida")
    return False


def menu():
    try:
        while True:
            try:
                usuario_encontrado = iniciar_sesion()
            except json.JSONDecodeError as je:
                registro_de_eventos.registrar_error(MODULO, "usuarios.json esta corrupto", je)
                print("el archivo usuarios.json esta corrupto, no se puede iniciar sesion")
                break

            if not usuario_encontrado:
                print("usuario o contraseña incorrectos")
                continue

            cargo = str(usuario_encontrado.get("cargo", "")).lower()
            if cargo not in ("admin", "residente"):
                print("su usuario no tiene un cargo valido, contacte al administrador")
                continue

            salir = False
            while not salir:
                try:
                    if cargo == "admin":
                        salir = menu_admin()
                    else:
                        salir = menu_residente(usuario_encontrado)
                except ValueError as ve:
                    registro_de_eventos.registrar_error(MODULO, "Opcion no numerica en el menu", ve)
                    print("se introdujo un valor invalido intente de nuevo")
                except Exception as e:
                    registro_de_eventos.registrar_error(MODULO, "Error inesperado en el menu", e)
                    print(f"se produjo un error inesperado: {e}")

            print("saliendo del programa...")
            time.sleep(1)
            break

    except (KeyboardInterrupt, EOFError):
        registro_de_eventos.registrar_error(MODULO, "Programa cerrado forzosamente")
        print("\nse cerro el programa forzozamente")
        print("saliendo del programa...")


if __name__ == "__main__":
    menu()
