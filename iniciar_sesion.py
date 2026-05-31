"""Inicio de sesión con manejo de errores y logging."""
import csv
import os
import logging

CSV_FILE = "registro_usuarios.csv"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('poker_app.log'),
    ]
)

logger = logging.getLogger(__name__)

def intentos_fallidos(usuario):
    """Confirma la cantidad de intentos fallidos para un usuario y actualiza el contador."""
    filas = []
    intentos = 0
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
        lector = csv.DictReader(csvfile)

        for fila in lector:
            if fila.get("USUARIO") == usuario:
                intentos = int(fila.get("INTENTOS_FALLIDOS") or 0) + 1
                fila["INTENTOS_FALLIDOS"] = str(intentos)

                if intentos >= 3:
                    if usuario == "admin":
                        logger.warning(
                            "Administrador superó el límite de intentos fallidos: %s",
                            usuario)
                    else:
                        fila["ESTADO"] = "bloqueado"
                        logger.warning(
                            "Usuario bloqueado por múltiples intentos fallidos: %s",
                            usuario)

                filas.append(fila)
            else:
                filas.append(fila)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        campos = ["USUARIO", "CONTRASEÑA", "ROL", "ESTADO", "INTENTOS_FALLIDOS"]
        escritor = csv.DictWriter(csvfile, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)

    return intentos

def validar_estado(usuario):
    """Verifica el estado de un usuario."""
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            if fila.get("USUARIO") == usuario:
                return fila.get("ESTADO")

def reiniciar_intentos(usuario):
    """Reinicia el contador de intentos fallidos para un usuario."""
    filas = []
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            if fila.get("USUARIO") == usuario:
                fila["INTENTOS_FALLIDOS"] = "0"
            filas.append(fila)
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        campos = ["USUARIO", "CONTRASEÑA", "ROL", "ESTADO", "INTENTOS_FALLIDOS"]
        escritor = csv.DictWriter(csvfile, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def iniciar_sesion():
    """Valida credenciales de usuario desde el archivo CSV."""
    try:
        if not os.path.exists(CSV_FILE):
            logger.error("Archivo de usuarios no encontrado: %s", CSV_FILE)
            print(f"Error: El archivo {CSV_FILE} no existe. Registre usuarios primero.")
            return False
        print("=== INICIO DE SESIÓN ===")
        usuario = input("Usuario: ").strip()
        if not usuario:
            logger.warning("Intento de inicio de sesión con usuario vacío")
            print("El nombre de usuario no puede estar vacío.")
            return False
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
            lector = csv.DictReader(csvfile)
            for fila in lector:
                if fila.get("USUARIO") == usuario:
                    break
            else:
                logger.warning("Usuario no encontrado: %s", usuario)
                print(f"El usuario '{usuario}' no existe.")
                print("Por favor, regístrese antes de iniciar sesión.")
                return None
        estado = validar_estado(usuario)
        if estado == "bloqueado":
            logger.warning("Intento de inicio de sesión con usuario bloqueado: %s", usuario)
            print(f"El usuario '{usuario}' está bloqueado. Contacte al administrador.")
            return False

        while True:
            contrasena = input("Contraseña: ").strip()
            if not contrasena:
                logger.warning("Intento de inicio de sesión con contraseña vacía para usuario: %s",
                                usuario)
                print("La contraseña no puede estar vacía.")
                continue

            with open(CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
                lector = csv.DictReader(csvfile)
                for fila in lector:
                    if fila.get("USUARIO") == usuario:
                        if fila.get("CONTRASEÑA") == contrasena:
                            logger.info("Inicio de sesión exitoso: %s", usuario)
                            print(f"¡Bienvenido, {usuario}!")
                            reiniciar_intentos(usuario)
                            return fila.get("ROL")
                        else:
                            logger.warning("Contraseña incorrecta para usuario: %s", usuario)
                            print("Contraseña incorrecta.")
                            intentos = intentos_fallidos(usuario)
                            if usuario == "admin" and intentos >= 3:
                                print("Demasiados intentos fallidos. Regresando al menú principal.")
                                return False

                            if intentos >= 3:
                                print(f"El usuario '{usuario}' ha sido bloqueado.")
                                print("Contacte al administrador para desbloquear su cuenta.")
                                return False
    except FileNotFoundError:
        logger.error("Archivo no encontrado: %s", CSV_FILE)
        print(f"Error: No se encontró {CSV_FILE}")
        return False
    except PermissionError:
        logger.error("Permiso denegado al leer %s", CSV_FILE)
        print("Error: Permiso denegado al acceder al archivo de usuarios")
        return False


if __name__ == "__main__":
    iniciar_sesion()
