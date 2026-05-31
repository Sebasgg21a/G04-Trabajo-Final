"""Funciones de administrador."""

import csv
import logging
import registro_usuarios

CSV_FILE = "registro_usuarios.csv"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def consultar_usuarios():
    """Función para consultar los usuarios registrados."""
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
            lector = csv.DictReader(csvfile)

            print("="*9 + " USUARIOS REGISTRADOS " + "="*9)
            print(f"{'|USUARIO':<16}{'|ROL':<16}{'|ESTADO|'}")
            for fila in lector:
                print(
                f"|{fila['USUARIO']:<14} "
                f"|{fila['ROL']:<14} "
                f"|{fila['ESTADO']:<10}|"
                )

        logger.info("Se han consultado los usuarios registrados.")
    except FileNotFoundError:
        print("No hay usuarios registrados.")
        logger.warning("Intento de consultar usuarios pero el archivo no existe.")
    except PermissionError:
        print("Error: Permiso denegado al acceder al archivo de usuarios.")
        logger.error("Permiso denegado al leer el archivo de usuarios: %s", CSV_FILE)

def bloquear_usuario():
    """Función para bloquear un usuario."""
    logger.info("Administrador seleccionó bloquear usuario.")

    usuario = input("Ingrese el nombre de usuario a bloquear: ").strip()

    usuario_existe = registro_usuarios.usuario_existe(usuario)

    if not usuario_existe:
        print(f"El usuario '{usuario}' no existe.")
        logger.warning("Intento de bloquear usuario inexistente: %s", usuario)
        return

    filas = []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            if fila.get("USUARIO") == usuario:
                if fila.get("ROL") == "administrador":
                    print("No se puede modificar el estado de un administrador.")
                    logger.warning("Intento de modificar el estado de un admin: %s", usuario)
                    return
                if fila.get("ESTADO") == "bloqueado":
                    print(f"El usuario '{usuario}' ya está bloqueado.")
                    logger.warning("Intento de bloquear un usuario ya bloqueado: %s", usuario)
                    return
                fila["ESTADO"] = "bloqueado"
                fila["INTENTOS_FALLIDOS"] = "0"
                logger.info("Estado cambiado a bloqueado para usuario: %s",usuario)
                logger.info("Intentos fallidos reseteados para usuario: %s",usuario)
            filas.append(fila)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        escritor = csv.DictWriter(csvfile, fieldnames=lector.fieldnames)
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"El usuario '{usuario}' ha sido bloqueado.")
    logger.info("Usuario '%s' bloqueado con éxito:", usuario)

def desbloquear_usuario():
    """Función para desbloquear un usuario."""
    logger.info("Administrador seleccionó desbloquear usuario.")

    usuario = input("Ingrese el nombre de usuario a desbloquear: ").strip()

    usuario_existe = registro_usuarios.usuario_existe(usuario)

    if not usuario_existe:
        print(f"El usuario '{usuario}' no existe.")
        logger.warning("Intento de desbloquear usuario inexistente: %s", usuario)
        return

    filas = []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            if fila.get("USUARIO") == usuario:
                if fila.get("ROL") == "administrador":
                    print("No se puede modificar el estado de un administrador.")
                    logger.warning("Intento de modificar el estado de un admin: %s", usuario)
                    return
                if fila.get("ESTADO") == "activo":
                    print(f"El usuario '{usuario}' ya está activo.")
                    logger.warning("Intento de desbloquear un usuario ya activo: %s", usuario)
                    return
                fila["ESTADO"] = "activo"
                fila["INTENTOS_FALLIDOS"] = "0"
                logger.info("Estado cambiado a activo para usuario: %s",usuario)
            filas.append(fila)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        escritor = csv.DictWriter(csvfile, fieldnames=lector.fieldnames)
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"El usuario '{usuario}' ha sido desbloqueado.")
    logger.info("Usuario '%s' desbloqueado con éxito:", usuario)

def eliminar_usuario():
    """Función para eliminar un usuario."""
    logger.info("Administrador seleccionó eliminar usuario.")

    usuario = input("Ingrese el nombre de usuario a eliminar: ").strip()
    usuario_existe = registro_usuarios.usuario_existe(usuario)
    if not usuario_existe:
        print(f"El usuario '{usuario}' no existe.")
        logger.warning("Intento de eliminar usuario inexistente: %s", usuario)
        return

    filas = []
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            if fila.get("USUARIO") == usuario:
                if fila.get("USUARIO") == "admin":
                    print("No se puede eliminar al administrador por defecto.")
                    logger.warning("Intento de eliminar al admin por defecto: %s", usuario)
                    return
                logger.info("Usuario '%s' eliminado con éxito:", usuario)
                print(f"El Usuario '{usuario}' ha sido eliminado con éxito.")
                continue

            filas.append(fila)
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        escritor = csv.DictWriter(csvfile, fieldnames=lector.fieldnames)
        escritor.writeheader()
        escritor.writerows(filas)

def consultar_resultados():
    """Función para consultar resultados de partidas (no implementada aún)."""
    #Pendinete despues de desarrollar la función de jugar partida
    print("Función de consultar resultados no implementada aún.")
    logger.info("Administrador seleccionó consultar resultados (función no implementada).")
