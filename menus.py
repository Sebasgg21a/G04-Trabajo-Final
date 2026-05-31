"""Módulo para manejar los menús del juego de póker."""
import logging
import iniciar_sesion
import registro_usuarios
import funciones_administrador

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('poker_app.log'),
    ]
)

logger = logging.getLogger(__name__)

def menu_admin():
    """Menú de administración."""
    try:
        while True:
            print("\n===== MENÚ ADMINISTRADOR =====")
            print("1. Consultar resultados")
            print("2. Bloquear usuario")
            print("3. Desbloquear usuario")
            print("4. Consultar usuarios")
            print("5. Eliminar usuario")
            print("6. Jugar partida") #jugar partida no implementada aún
            print("7. Cerrar sesión")

            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                print("Función de consultar resultados no implementada aún.")
                logger.info("Administrador seleccionó consultar resultados.")
            elif opcion == 2:
                funciones_administrador.bloquear_usuario()
                logger.info("Administrador seleccionó bloquear usuario.")
            elif opcion == 3:
                funciones_administrador.desbloquear_usuario()
                logger.info("Administrador seleccionó desbloquear usuario.")
            elif opcion == 4:
                funciones_administrador.consultar_usuarios()
                logger.info("Administrador seleccionó consultar usuarios.")
            elif opcion == 5:
                funciones_administrador.eliminar_usuario()
                logger.info("Administrador seleccionó eliminar usuario.")
            elif opcion == 6:
                print("Función de jugar partida no implementada aún.")
                logger.info("Administrador seleccionó jugar partida.")
            elif opcion == 7:
                print("Cerrando sesión...")
                logger.info("Administrador cerró sesión.")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 7.")

    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número.")
        logger.warning("Administrador ingresó una opción no numérica en el menú de administración.")

def menu_usuario():
    """Menú para usuarios."""
    logger.info("Usuario accedió al menú de usuario.")
    while True:
        try:
            print("====POKER====")
            print("1. Jugar partida") #jugar partida no implementada aún
            print("2. Ver estadísticas") #ver estadísticas no implementada aún
            print("3. Cerrar sesión")
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                print("Función de jugar partida no implementada aún.")
                logger.info("Jugador seleccionó jugar partida.")
            elif opcion == 2:
                print("Función de ver estadísticas no implementada aún.")
                logger.info("Jugador seleccionó ver estadísticas.")
            elif opcion == 3:
                print("Cerrando sesión...")
                logger.info("Jugador cerró sesión.")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 3.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")
            logger.warning("Jugador ingresó una opción no numérica en el menú de usuario.")

def menu_principal():
    """Función para mostrar el menú principal y manejar la selección del usuario."""
    while True:
        print("=== MENÚ PRINCIPAL ===")
        print("Seleccione una opción:")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        try:
            opcion = int(input("Ingrese el número de la opción: "))
            if opcion == 1:
                rol = iniciar_sesion.iniciar_sesion()
                if rol == "administrador":
                    menu_admin()
                elif rol == "usuario":
                    menu_usuario()
                elif rol == "general":
                    #menu_general() #pendiente de implementación
                    print("pendiente de implementación.")
                else:
                    pass
            elif opcion == 2:
                registro_usuarios.registrar_usuario()
            elif opcion == 3:
                print("¡Gracias por jugar! ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, ingrese un número entre 1 y 3.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")
            logger.warning("Usuario ingresó una opción no numérica en el menú principal.")

menu_principal()
