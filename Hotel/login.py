import getpass
from conexion import Conexion
from usuarioDAO import UsuarioDao

class Login:
    @staticmethod
    def login():
        conexion = Conexion()
        usuario_dao = UsuarioDao(conexion)
        acceso_concedido = False

        while not acceso_concedido:
            print("=== Inicio de sesión ===")
            nombre = input("Nombre de usuario: ")
            contraseña = getpass.getpass("Contraseña: ")

            if usuario_dao.verificar_credenciales(nombre, contraseña):
                print("Acceso concedido")
                acceso_concedido = True
            else:
                print("Acceso denegado. Intente nuevamente.")
                salir = input("¿Intentar de nuevo? (s/n): ")

                if salir.lower() == 'n':
                    print("Saliendo del sistema...")
                    exit()  # Salir del programa

        return nombre

    @staticmethod
    def registrar_usuario():
        conexion = Conexion()
        usuario_dao = UsuarioDao(conexion)
        
        print("=== Registrar nuevo usuario ===") #regitro para nuevo usuario
        nombre = input("Nombre de usuario: ")
        contraseña = getpass.getpass("Contraseña: ")
        print("Seleccione el cargo del usuario:")
        print("1. Administrador")
        print("2. Encargado")
        cargo_opcion = input("Seleccione una opción: ")
        cargo = "Administrador" if cargo_opcion == "1" else "Encargado"

        usuario_dao.crear_usuario(nombre, contraseña, cargo)
        print("Usuario registrado exitosamente.")

    @staticmethod
    def cerrar_sesion():
        print("Cerrando sesión...")
        while True:
            opcion = input("¿Desea iniciar sesión de nuevo? (s/n): ")
            if opcion.lower() == 's':
                return 'login'
            elif opcion.lower() == 'n':
                print("Saliendo del sistema...")
                exit()
            else:
                print("Opción no válida. Por favor, intente de nuevo.")
