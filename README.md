# 🛠️ Sistema de Préstamo de Herramientas

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/Persistencia-JSON-000000?logo=json&logoColor=white)
![Consola](https://img.shields.io/badge/Interfaz-Consola-4EAA25?logo=gnubash&logoColor=white)
![Git Flow](https://img.shields.io/badge/Flujo-Git%20Flow-F05032?logo=git&logoColor=white)

Aplicación de consola desarrollada en **Python** para administrar el inventario de herramientas de una comunidad, registrar a sus usuarios y controlar los préstamos y devoluciones. Toda la información se guarda en archivos **JSON**, sin necesidad de una base de datos.

---

## 📑 Tabla de contenido

- [Contexto](#-contexto)
- [Descripción](#-descripción)
- [Funcionalidades](#-funcionalidades)
- [Roles y permisos](#-roles-y-permisos)
- [Tecnologías y herramientas](#-tecnologías-y-herramientas)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Modelo de datos](#-modelo-de-datos)
- [Requisitos](#-requisitos)
- [Instalación y despliegue](#-instalación-y-despliegue)
- [Uso](#-uso)
- [Manejo de errores y registro de eventos](#-manejo-de-errores-y-registro-de-eventos)
- [Flujo de trabajo con Git](#-flujo-de-trabajo-con-git)
- [Mejoras futuras](#-mejoras-futuras)
- [Autor](#-autor)

---

## 🌎 Contexto

En barrios, conjuntos residenciales y juntas comunitarias es común que las herramientas (taladros, escaleras, martillos, etc.) se compartan entre vecinos. Sin un registro, es difícil saber **quién tiene qué herramienta, cuántas quedan disponibles y cuándo deben devolverse**, lo que provoca pérdidas y conflictos.

Este proyecto se desarrolló como proyecto de formación en **Campuslands** (módulo de Python) para resolver ese problema con lo aprendido en el curso: estructuras de datos, funciones, módulos, manejo de archivos, manejo de excepciones y persistencia en JSON.

## 📝 Descripción

El sistema permite:

1. **Iniciar sesión** con usuario y contraseña.
2. Mostrar un **menú distinto según el cargo** del usuario (administrador o residente).
3. Llevar el **inventario de herramientas** con su cantidad disponible.
4. Registrar **préstamos** validando que haya stock, y descontarlo automáticamente.
5. Registrar **devoluciones**, que reponen el stock.
6. Generar **reportes** de uso: préstamos activos, historial por usuario, herramientas más prestadas, etc.
7. Guardar cada error en un **archivo de log** para revisarlo después.

## ✨ Funcionalidades

### 👤 Gestión de usuarios
| Función | Descripción |
|---|---|
| Crear | Registra un usuario con nombre de usuario único, datos personales, cargo (`admin` / `residente`) y contraseña cifrada. |
| Listar | Muestra todos los usuarios **sin mostrar la contraseña**. |
| Buscar | Busca coincidencias en cualquier campo (excepto la contraseña). |
| Actualizar | Modifica un campo validando su formato. El `id` no se puede cambiar. |
| Eliminar | Elimina un usuario por su ID. |

### 🔧 Gestión de herramientas
| Función | Descripción |
|---|---|
| Crear | Registra nombre, categoría, cantidad, estado y valor estimado. |
| Listar | Muestra todo el inventario. |
| Buscar | Busca coincidencias en cualquier campo. |
| Actualizar | Modifica un campo manteniendo el tipo de dato (entero para la cantidad, decimal para el valor). |
| Eliminar | Elimina una herramienta por su ID. |

### 📦 Gestión de préstamos
| Función | Descripción |
|---|---|
| Petición de préstamo | Verifica que existan el usuario y la herramienta, que haya stock suficiente y que las fechas sean válidas (`DD/MM/AA`). Descuenta el stock y marca el préstamo como `en uso`. |
| Disponibilidad y stock | Indica si hay unidades suficientes de una herramienta. |
| Devoluciones | Lista los préstamos pendientes, marca el elegido como `devuelto`, guarda la fecha de devolución y repone el stock. |

### 📊 Consultas y reportes
| Reporte | Descripción |
|---|---|
| Préstamos activos | Préstamos con estado `en uso`. |
| Historial de usuario | Todos los préstamos de un usuario. |
| Herramientas más prestadas | Ranking de herramientas según la cantidad de préstamos. |
| Usuarios que más prestan | Ranking de usuarios según la cantidad de préstamos. |
| Stock bajo | Herramientas con 2 unidades o menos. |

## 🔐 Roles y permisos

| Acción | Administrador | Residente |
|---|:---:|:---:|
| Gestionar usuarios | ✅ | ❌ |
| Crear, actualizar y eliminar herramientas | ✅ | ❌ |
| Listar y buscar herramientas | ✅ | ✅ |
| Pedir préstamos | ✅ (a nombre de cualquier usuario) | ✅ (solo a su nombre) |
| Consultar disponibilidad | ✅ | ✅ |
| Registrar devoluciones | ✅ (de cualquier préstamo) | ✅ (solo de los suyos) |
| Consultas y reportes | ✅ | ❌ |

## 🧰 Tecnologías y herramientas

| Herramienta | Uso |
|---|---|
| **Python 3.10+** | Lenguaje principal. |
| `json` | Lectura y escritura de los datos. |
| `os` | Rutas de archivos independientes de la carpeta de ejecución. |
| `datetime` | Validación de fechas y marcas de tiempo del log. |
| `hashlib` | Cifrado SHA-256 de contraseñas. |
| `time` | Pausas en la salida del programa. |
| **Visual Studio Code** | Editor de código. |
| **Git + GitHub** | Control de versiones con Git Flow, Conventional Commits y Gitmoji. |

> El proyecto usa **solo la biblioteca estándar de Python**: no hace falta instalar dependencias externas.

## 📁 Estructura del proyecto

```
proyecto/
├── main.py                        # Punto de entrada de la aplicación
├── usuarios.json                  # Datos de usuarios
├── herramientas.json              # Inventario de herramientas
├── prestamos.json                 # Registro de préstamos
├── errores.log                    # Log de errores (se genera solo, ignorado por git)
├── README.md
├── .gitignore
└── modulos/
    ├── permisos_a_manejar.py      # Inicio de sesión y menús por cargo
    ├── gestion_de_usuarios.py     # CRUD de usuarios
    ├── gestion_de_herramientas.py # CRUD de herramientas
    ├── gestion_de_prestamos.py    # Préstamos, disponibilidad y devoluciones
    ├── consultas_y_reportes.py    # Reportes
    ├── datos.py                   # Utilidades de JSON, IDs, rutas y cifrado
    └── registro_de_eventos.py     # Registro de errores en errores.log
```

### Diagrama de módulos

```
main.py
  └── permisos_a_manejar (login + menús)
        ├── gestion_de_usuarios ─────┐
        ├── gestion_de_herramientas ─┤
        ├── gestion_de_prestamos ────┼──► datos.py ──► archivos .json
        ├── consultas_y_reportes ────┤
        └── registro_de_eventos ◄────┘ (todos registran errores aquí)
```

## 🗃️ Modelo de datos

**`usuarios.json`**
```json
{
    "usuario": "isaac",
    "nombre": "Isaac",
    "apellidos": "Camaño",
    "telefono": "3001234567",
    "direccion": "calle 1 #2",
    "cargo": "admin",
    "contraseña": "<hash SHA-256>",
    "id": 1
}
```

**`herramientas.json`**
```json
{
    "nombre": "taladro",
    "categoria": "electrica",
    "cantidad": 3,
    "estado": "bueno",
    "valor": 50000.0,
    "id": 1
}
```

**`prestamos.json`**
```json
{
    "usuario": "isaac",
    "herramienta": "taladro",
    "cantidad": 1,
    "fecha de inicio": "10/11/26",
    "fecha estimada de devolucion": "15/11/26",
    "estado": "en uso",
    "observaciones": "",
    "id": 1,
    "fecha de devolucion": "14/11/26"
}
```
> El campo `fecha de devolucion` se agrega cuando el préstamo se marca como `devuelto`.

## ✅ Requisitos

- **Python 3.10** o superior ([descargar](https://www.python.org/downloads/)).
- **Git** (opcional, para clonar el repositorio).
- Una terminal: PowerShell, CMD, Git Bash o la terminal de Linux o macOS.

Para comprobar la versión instalada:
```bash
python --version
```

## 🚀 Instalación y despliegue

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/manuelisaaccamanidiaz-lgtm/herramientad_del_vecindario.git
   cd <NOMBRE-REPO>
   ```

2. **(Opcional) Crear un entorno virtual**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux / macOS
   source .venv/bin/activate
   ```
   No hay dependencias que instalar: todo pertenece a la biblioteca estándar.

3. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

4. **Iniciar sesión con el administrador inicial**

   | Usuario | Contraseña |
   |---|---|
   | `isaac` | `1234` |

   > ⚠️ Cambia esta contraseña después del primer inicio de sesión (**Gestionar usuarios → Actualizar → contraseña**).

### Reiniciar los datos
Para empezar desde cero, deja `herramientas.json` y `prestamos.json` con el contenido `[]`. En `usuarios.json`, conserva al menos un usuario `admin`.

## 🎮 Uso

### Menú de administrador
```
1. gestionar herramientas   → crear / listar / buscar / actualizar / eliminar
2. gestionar usuarios       → crear / listar / buscar / actualizar / eliminar
3. gestionar prestamos      → petición / disponibilidad / devoluciones / reportes
4. consultas y reportes     → activos / historial / más prestadas / usuarios top / stock bajo
5. salir
```

### Menú de residente
```
1. listar herramientas
2. buscar herramientas
3. petición de préstamo
4. disponibilidad y stock
5. devolución de herramientas
6. salir
```

### Ejemplo de flujo
1. El admin inicia sesión y crea la herramienta `taladro` con 3 unidades.
2. El admin crea el usuario residente `ana`.
3. `ana` inicia sesión y pide 2 taladros → el stock baja a 1.
4. El reporte de **stock bajo** muestra el taladro.
5. `ana` devuelve el préstamo → el stock vuelve a 3.

> Para salir en cualquier momento, presiona `Ctrl + C`: el programa se cierra de forma controlada.

## 🧯 Manejo de errores y registro de eventos

- Las entradas inválidas (letras donde van números, fechas mal escritas, cargos inexistentes) muestran un mensaje y el programa **sigue funcionando**.
- Si un archivo JSON no existe o está vacío, se trata como una lista vacía.
- Si un JSON está **corrupto**, se avisa al usuario y el archivo **no se sobrescribe**, para no perder información.
- Cada error se guarda en `errores.log` con la fecha, el módulo y el detalle de la excepción:
  ```
  [2026-11-10 19:35:50] permisos_a_manejar: Opcion no numerica en el menu -> ValueError: invalid literal for int() with base 10: 'x'
  ```

## 🌿 Flujo de trabajo con Git

El repositorio sigue **Git Flow**:

| Rama | Propósito |
|---|---|
| `main` | Versiones estables, marcadas con etiquetas (`v1.0.0`). |
| `develop` | Integración de nuevas funcionalidades. |
| `feature/*` | Una funcionalidad nueva, creada desde `develop`. |
| `release/*` | Preparación de una versión. |
| `hotfix/*` | Correcciones urgentes, creadas desde `main`. |

Los commits usan **Conventional Commits** con **Gitmoji**:

| Gitmoji | Tipo | Uso |
|---|---|---|
| 🎉 | `chore` | Inicio del proyecto |
| ✨ | `feat` | Nueva funcionalidad |
| 🐛 | `fix` | Corrección de errores |
| 🚑 | `fix` | Hotfix urgente |
| 📝 | `docs` | Documentación |
| ♻️ | `refactor` | Reestructuración de código |
| 🔀 | `merge` | Fusión de ramas |
| 🔖 | `release` | Nueva versión |

Ejemplo: `✨ feat(prestamos): registra devoluciones con control de stock`

## 🔮 Mejoras futuras

- Notificar los préstamos vencidos según la fecha estimada de devolución.
- Exportar los reportes a CSV.
- Agregar pruebas unitarias con `pytest`.
- Reemplazar el cifrado SHA-256 por uno con *salt* (`bcrypt` / `hashlib.pbkdf2_hmac`).
- Migrar la persistencia a SQLite.
- Crear una interfaz gráfica o una API web.

## 👨‍💻 Autor

**Manuel Isaac Camaño Diaz**
Proyecto de formación — Campuslands, módulo de Python.

- GitHub: [@manuelisaaccamanidiaz-lgtm](https://github.com/manuelisaaccamanidiaz-lgtm)
