import os
import sys

# Permite importar los modulos de la carpeta /modulos
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "modulos"))

from permisos_a_manejar import menu

if __name__ == "__main__":
    menu()
