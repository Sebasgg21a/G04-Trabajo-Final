"""Registro de usuarios en un archivo CSV con manejo de errores y logging."""

import csv
import os
import logging

CSV_FILE = "registro_usuarios.csv"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('poker_app.log')
    ]
)

logger = logging.getLogger(__name__)


def usuario_existe(nombre_usuario):
    """Verifica si un usuario ya existe en el archivo CSV."""
    if not os.path.exists(CSV_FILE):
        return False

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            if fila.get("USUARIO") == nombre_usuario:
                return True
    logger.debug(
        "Usuario %s no encontrado en %s",
        nombre_usuario,
        CSV_FILE
    )
    return False


def registrar_usuario():
    """Registra un nuevo usuario en el archivo CSV."""
    while True:
        print("=== REGISTRO DE USUARIOS ===")
        usuario = input("Nombre de usuario: ").strip()
        if not usuario:
            logger.warning("Intento de registro con usuario vacío")
            print("El nombre de usuario no puede estar vacío.")
            continue
        if usuario_existe(usuario):
            logger.warning(
                "Registro rechazado - Usuario duplicado: %s",
                usuario
            )
            print(f"El usuario '{usuario}' ya existe.")
            print("Por favor, elija un nombre de usuario diferente.")
        else:
            break

    while True:
        contrasena = input("Contraseña: ").strip()
        if not contrasena:
            logger.warning(
                "Intento de registro sin contraseña para usuario: %s",
                usuario
            )
            print("La contraseña no puede estar vacía.")
        elif len(contrasena) < 6:
            logger.warning(
                "Contraseña demasiado corta, min: 6 caracteres, para usuario: %s",
                usuario
            )
            print("La contraseña debe tener al menos 6 caracteres.")
        elif not any(caracter.isdigit() for caracter in contrasena):
            logger.warning(
                "Contraseña sin dígitos, min: 1 número, para usuario: %s",
                usuario
            )
            print("La contraseña debe contener al menos un número.")
        else:
            break

    while True:
        print("Seleccione el rol del usuario:")
        print("1. Usuario")
        print("2. General")
        rol = input("Ingrese: ").strip()
        if rol in ["1", "2"]:
            break
        else:
            logger.warning(
                "Selección de rol inválida: %s para usuario: %s",
                rol,
                usuario
            )
            print("Selección de rol inválida. Por favor, ingrese 1 o 2.")

    if rol == "1":
        rol = "usuario"
    elif rol == "2":
        rol = "general"

    encabezados = ["USUARIO", "CONTRASEÑA","ROL","ESTADO","INTENTOS_FALLIDOS"]
    archivo_existe = os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as csvfile:
        escritor = csv.writer(csvfile)
        if not archivo_existe:
            escritor.writerow(encabezados)
        escritor.writerow([usuario, contrasena, rol, "activo", 0])

    logger.info(
        "Usuario registrado exitosamente: %s : %s",
        usuario,
        rol
    )
    print(f"Usuario '{usuario}' registrado exitosamente como {rol}.")


if __name__ == "__main__":
    registrar_usuario()
