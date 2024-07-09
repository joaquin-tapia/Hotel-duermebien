
from conexion import Conexion
from orientacionDao import OrientacionDao
from usuarioDAO import UsuarioDao
from pasajeroDAO import PasajeroDAO
from habitacionDao import HabitacionDao
from beautifultable import BeautifulTable
import os
import mysql.connector

conexion = Conexion()
usuario_dao = UsuarioDao(conexion)
habitacion_dao = HabitacionDao(conexion)
pasajero_dao = PasajeroDAO(conexion)
orientacion_dao = OrientacionDao(conexion)

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')


def crear_administrador_si_no_existe():
    print("=== Hotel Duerme Bien ===")
    conexion = Conexion()
    try:
        usuario_dao = UsuarioDao(conexion)
        if not usuario_dao.check_administrador():
            print("| No hay un administrador en el sistema. Por favor cree uno |")
            nombre = input("Ingrese el nombre del administrador: ")
            contraseña = input("Ingrese una contraseña: ")
            usuario_dao.crear_administrador(nombre, contraseña)
            print("Administrador creado exitosamente.")
        else:
            print("Ya existe un administrador en el sistema.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()
        input("Presione Enter para continuar...")

def menu_administrador():
    while True:
        limpiar_consola()
        table = BeautifulTable()
        table.columns.header =["=== Menu Administrador ==="]
        table.rows.append(["1. Ver usuarios"])
        table.rows.append(["2. Crear usuario"])
        table.rows.append(["3. Modificar permisos"])
        table.rows.append(["4. Eliminar usuario"])
        table.rows.append(["5. Administrar orientaciones"])
        table.rows.append(["6. Menu Habitaciones"])
        table.rows.append(["7. Menu Pasajeros"])
        table.rows.append(["8. Cerrar sesion"])

        print(table)

        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            ver_usuarios()

        elif opcion == "2":
            crear_usuario()
        
        elif opcion == "3":
            modificar_permisos()

        elif opcion == "4":
            eliminar_usuario()
        
        elif opcion == "5":
            administrar_orientacion()

        elif opcion == "6":
            menu_habitaciones()

        elif opcion == "7":
            menu_pasajeros()

        elif opcion == "8":
            print("Sesion Cerrada")
            break

        else:
            print("Opcion Invalida. Intente Nuevamente")

def ver_usuarios():

        limpiar_consola()
        usuarios = usuario_dao.obtener_usuarios()
        table = BeautifulTable()
        table.columns.header = ["ID", "Nombre", "Cargo"]
        for usuario in usuarios:
            table.rows.append([usuario[0], usuario[1], usuario[2]])
        print(table)

        input("Enter para volver. ")
   


def crear_usuario():
  
    while True:
        limpiar_consola()

        nombre = input("Ingrese el nombre del nuevo usuario: ")
        contraseña = input("Ingresa la contraseña del nuevo usuario: ")
        cargo_opcion = input("Ingrese el cargo del nuevo usuario (1. Administrador, 2. Encargado) ")
    
        if cargo_opcion == "1":
          cargo = "Administrador"
        elif cargo_opcion == "2":
            cargo = "Encargado"

        else:
            print("Opcion Invalida. Intente Nuevamente")
            return
    
        usuario_dao.crear_usuario(nombre, contraseña, cargo)
        print(f"Usuario {nombre} creado con exito como {cargo}.")

        opcion = input("0. Para volver. ")
        if opcion == "0":
            break
   

def modificar_permisos():
    usuario_dao = UsuarioDao(conexion)
    
    while True:
        limpiar_consola()

        # Obtener y mostrar la lista de usuarios
        usuarios = usuario_dao.obtener_usuarios()
        if usuarios:
            table = BeautifulTable()
            table.columns.header = ["ID", "Nombre", "Cargo"]

            for usuario in usuarios:
                table.rows.append([usuario[0], usuario[1], usuario[2]])

            print("\nLista de Usuarios:")
            print(table)
        else:
            print("No hay usuarios registrados.")
            break

        try:
            id_usuario = int(input("\nIngrese el ID del usuario que desea modificar (0 para cancelar): "))
            if id_usuario == 0:
                break

            usuario = next((u for u in usuarios if u[0] == id_usuario), None)
            if usuario:
                print(f"El usuario {usuario[1]} tiene actualmente el cargo de {usuario[2]}.")
                print("Seleccione el nuevo cargo del usuario:")
                print("1. Administrador")
                print("2. Encargado")
                nuevo_cargo_opcion = input("Seleccione una opción: ")
                nuevo_cargo = "Administrador" if nuevo_cargo_opcion == "1" else "Encargado"
                
                if usuario[2] == nuevo_cargo:
                    print(f"El usuario ya es {nuevo_cargo}. No se realizaron cambios.")
                else:
                    usuario_dao.modificar_permisos(id_usuario, nuevo_cargo)
                    print("Permisos modificados correctamente.")
            else:
                print("Usuario no encontrado.")

            # Mostrar la lista de usuarios actualizada
            limpiar_consola()
            usuarios = usuario_dao.obtener_usuarios()
            table = BeautifulTable()
            table.columns.header = ["ID", "Nombre", "Cargo"]

            for usuario in usuarios:
                table.rows.append([usuario[0], usuario[1], usuario[2]])

            print("\nLista de Usuarios Actualizada:")
            print(table)

        except ValueError:
            print("Error: Ingrese un ID válido.")
        
        opcion = input("\n¿Desea modificar otro usuario? (s/n): ").lower()
        if opcion != 's':
            break

        


                    
def administrar_orientacion():
    while True:
        limpiar_consola()
        table = BeautifulTable()
        table.columns.header =["=== Menu Administrador ==="]
        table.rows.append(["1. Ver orientaciones"])
        table.rows.append(["2. Agregar orientacion"])
        table.rows.append(["3. Modificar orientacion"])
        table.rows.append(["4. Eliminar orientacion"])
        table.rows.append(["5. Cerrar Sesion"])
        print(table)
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            ver_orientaciones()

        elif opcion == "2":
            agregar_orientacion()

        elif opcion == "3":
            modificar_orientacion()
        
        elif opcion == "4":
            eliminar_orientacion()

        elif opcion == "5":
            print("Sesion Cerrada")
            break

        else:
            print("Opcion Invalida. Intente Nuevamente")

def ver_orientaciones():

    while True:
        limpiar_consola()
        orientaciones = orientacion_dao.obtener_orientaciones()
        table = BeautifulTable()
        table.columns.header = ["ID", "Orientacion"]
        for orientacion in orientaciones:
            table.rows.append([orientacion[0], orientacion[1]])
        print(table)

        opcion = input("0. Para volver. ")
        if opcion == "0":
            break

def agregar_orientacion():
    while True:
        limpiar_consola()

        orientacion = input("Ingrese la orientacion: ")
        orientacion_dao.registrar_orientacion(orientacion)
        print(f"La orientacion {orientacion} fue creada con exito.")

        opcion = input("0. Para volver. ")
        if opcion == "0":
            break

def modificar_orientacion():
    while True:
        limpiar_consola()
        id_orientacion = input("Ingrese el ID de la orientación que desea modificar: ")
        nueva_orientacion = input("Ingrese la nueva orientación: ")
        confirmacion = input(f"¿Está seguro que desea modificar la orientación {id_orientacion} a '{nueva_orientacion}'? (S/N) ").upper()

        if confirmacion == "S":
            orientacion_dao.modificar_orientacion(nueva_orientacion, id_orientacion)
            print(f"Orientación {id_orientacion} modificada correctamente a '{nueva_orientacion}'.")

        else:
            print("Operación cancelada.")

        opcion = input("0. Para volver. ")
        if opcion == "0":
            break


def eliminar_orientacion():
    
    while True:
        limpiar_consola()
        id_orientacion = input("Ingrese el ID del usuario que desea eliminar: ")
        confirmacion = input(f"Esta seguro que desea eliminar al usuario {id_orientacion} (S/N?) ").upper()

        if confirmacion == "S":
            orientacion_dao.eliminar_orientacion(id_orientacion)
            print(f"Usuario {id_orientacion} eliminado correctamente.")

        else:
            print("Operacion cancelada.")

        opcion = input("0. Para volver. ")
        if opcion == "0":
            break
    


def eliminar_usuario():
    while True:
        limpiar_consola()

        # Obtener la lista de usuarios
        usuario_dao = UsuarioDao(conexion)
        usuarios = usuario_dao.obtener_usuarios()

        if usuarios:
            table = BeautifulTable()
            table.columns.header = ["ID", "Nombre", "Cargo"]

            for usuario in usuarios:
                id_usuario, nombre, cargo = usuario[:3]  # Tomamos solo los primeros tres elementos
                table.rows.append([id_usuario, nombre, cargo])

            print("\nLista de Usuarios:")
            print(table)

            try:
                id_usuario = int(input("Ingrese el ID del usuario que desea eliminar (0 para cancelar): "))

                if id_usuario == 0:
                    break

                confirmacion = input(f"¿Está seguro que desea eliminar al usuario con ID {id_usuario}? (S/N): ").upper()

                if confirmacion == "S":
                    # Verificar si el ID del usuario existe
                    usuario_existe = any(usuario[0] == id_usuario for usuario in usuarios)
                    if not usuario_existe:
                        print(f"El usuario con ID {id_usuario} no existe. Por favor, ingrese un ID válido.")
                        continue

                    usuario_dao.eliminar_usuario(id_usuario)
                    print(f"Usuario con ID {id_usuario} eliminado correctamente.")

                else:
                    print("Operación cancelada.")

                opcion = input("\n¿Desea eliminar otro usuario? (sí/no): ").lower()
                if opcion != 'sí' and opcion != 'si':
                    break

            except ValueError:
                print("Error: Ingrese un ID válido.")
                continue

        else:
            print("No hay usuarios registrados.")
            break

    
    

def menu_encargado():
    while True:
        limpiar_consola()
        table = BeautifulTable()
        table.columns.header = ["=== Menu Encargado ==="]
        table.rows.append(["1. Gestionar Habitaciones"])
        table.rows.append(["2. Gestionar Pasajeros"])
        table.rows.append(["3. Cerrar Sesion"])

        print(table)

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_habitaciones()
        
        elif opcion == "2":
            menu_pasajeros()
        
        elif opcion == "3":
            print("Sesión Cerrada")
            break

        else:
            print("Opción inválida. Intente nuevamente")


def menu_habitaciones():
    while True:
        limpiar_consola()
        table = BeautifulTable()
        table.columns.header = ["=== Menu Habitaciones ==="]
        table.rows.append(["1. Ver Habitaciones"])
        table.rows.append(["2. Registrar Habitación"])
        table.rows.append(["3. Modificar Habitación"])
        table.rows.append(["4. Eliminar Habitación"])
        table.rows.append(["5. Volver al Menú Encargado"])

        print(table)

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_habitaciones()

        elif opcion == "2":
            registrar_habitacion()

        elif opcion == "3":
            modificar_habitacion()

        elif opcion == "4":
            eliminar_habitacion()

        elif opcion == "5":
            break

        else:
            print("Opción inválida. Intente nuevamente")


def menu_pasajeros():
    while True:
        limpiar_consola()
        table = BeautifulTable()
        table.columns.header = ["=== Menu Pasajeros ==="]
        table.rows.append(["1. Ver Pasajeros"])
        table.rows.append(["2. Registrar Pasajero"])
        table.rows.append(["3. Modificar Pasajero"])
        table.rows.append(["4. Eliminar Pasajero"])
        table.rows.append(["5. Volver al Menú Encargado"])

        print(table)

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_pasajeros()

        elif opcion == "2":
            registrar_pasajero()

        elif opcion == "3":
            modificar_pasajero()

        elif opcion == "4":
            eliminar_pasajero()

        elif opcion == "5":
            break

        else:
            print("Opción inválida. Intente nuevamente")


def registrar_habitacion():
    limpiar_consola()
    
    while True:
        try:
            numero_habitacion = int(input("Ingrese el número de la habitación (1-100): "))
            if numero_habitacion < 1 or numero_habitacion > 100:
                print("Error: El número de la habitación debe estar entre 1 y 100.")
                continue
        except ValueError:
            print("Error: Ingrese un número válido.")
            continue
        
        habitaciones_existentes = habitacion_dao.obtener_habitaciones()
        if any(habitacion["numero_habitacion"] == numero_habitacion for habitacion in habitaciones_existentes):
            print(f"Error: La habitación con número {numero_habitacion} ya está registrada.")
            continue
        
        break

    while True:
        try:
            pasajeros_admitidos = int(input("Capacidad de la habitación (1-3): "))
            if pasajeros_admitidos < 1 or pasajeros_admitidos > 3:
                print("Error: La capacidad de la habitación debe estar entre 1 y 3.")
                continue
            break
        except ValueError:
            print("Error: Ingrese un número válido para la capacidad de la habitación.")

    # Mostrar tabla de orientaciones disponibles
    orientaciones = orientacion_dao.obtener_orientaciones()
    
    if orientaciones:
        table = BeautifulTable()
        table.columns.header = ['ID', 'Orientación']
        
        for orientacion in orientaciones:
            table.rows.append([orientacion[0], orientacion[1]])

        print("\nOrientaciones Disponibles:")
        print(table)
        
        while True:
            try:
                id_orientacion = int(input("Ingrese el ID de la orientación de la habitación: "))
                if any(orientacion[0] == id_orientacion for orientacion in orientaciones):
                    break
                else:
                    print("Error: ID de orientación no válido.")
            except ValueError:
                print("Error: Ingrese un ID válido.")
    else:
        print("No hay orientaciones disponibles.")
        id_orientacion = None

    estado = "vacante"
    habitacion_dao.registrar_habitacion(numero_habitacion, pasajeros_admitidos, id_orientacion, estado)
    
    while True:
        opcion = input("\n¿Desea registrar otra habitacion? (s/n): ").lower()
        if opcion == 's':
            registrar_habitacion()
            break
        elif opcion == 'n':
            break
        else:
            print("Opción inválida. Por favor, ingrese 's' o 'n'.")


def registrar_pasajero():
    print("=== Registrar Pasajero ===")
    conexion = Conexion()
    try:
        habitacion_dao = HabitacionDao(conexion)
        pasajero_dao = PasajeroDAO(conexion)

        # Mostrar habitaciones vacantes
        habitaciones_vacantes = habitacion_dao.obtener_habitaciones_vacantes()
        if not habitaciones_vacantes:
            print("No hay habitaciones vacantes disponibles para registrar pasajeros.")
            return

        table = BeautifulTable()
        table.columns.header = ["ID", "Número", "Pasajeros Admitidos", "Orientación"]
        for habitacion in habitaciones_vacantes:
            table.rows.append([habitacion[0], habitacion[1], habitacion[2], habitacion[3]])
        print("Habitaciones vacantes:")
        print(table)

        # Ingresar los datos del pasajero responsable
        while True:
            print("\nIngrese los datos del pasajero responsable:")
            nombre_responsable = input("Nombre: ")
            apellido_responsable = input("Apellido: ")
            rut_responsable = input("RUT: ")

            # Verificar si el RUT ya está registrado
            if pasajero_dao.verificar_rut_existente(rut_responsable):
                print("Error: Este RUT ya está registrado para otro pasajero. Intente con otro.")
                continue
            else:
                break

        cantidad_pasajeros = int(input("\nCantidad de pasajeros (incluido el responsable): "))

        id_responsable = None
        pasajeros_restantes = cantidad_pasajeros
        habitaciones_reservadas = []

        # Seleccionar la primera habitación para el responsable
        id_habitacion_responsable = int(input("\nIngrese el ID de la habitación para el pasajero responsable: "))
        habitacion_disponible = next((h for h in habitaciones_vacantes if h[0] == id_habitacion_responsable), None)

        if not habitacion_disponible:
            print(f"No se encontró una habitación vacante con ID {id_habitacion_responsable}.")
            return

        capacidad_habitacion = habitacion_disponible[2]
        if pasajeros_restantes <= capacidad_habitacion:
            pasajeros_a_registrar = pasajeros_restantes
        else:
            pasajeros_a_registrar = capacidad_habitacion

        habitaciones_reservadas.append(id_habitacion_responsable)

        # Registrar el pasajero responsable en la primera habitación
        print("Registrando pasajero responsable...")
        id_responsable = pasajero_dao.registrar_pasajero(nombre_responsable, apellido_responsable, rut_responsable, id_habitacion_responsable, responsable=True)
        pasajeros_restantes -= 1

        if capacidad_habitacion > 1:
            # Registrar los demás pasajeros en la primera habitación
            print("Registrando otros pasajeros en la primera habitación...")
            for i in range(pasajeros_a_registrar - 1):
                print(f"\nIngrese los datos del pasajero {i + 1}:")
                while True:
                    nombre = input("Nombre: ")
                    apellido = input("Apellido: ")
                    rut = input("RUT: ")
                    if pasajero_dao.verificar_rut_existente(rut):
                        print(f"Error: El RUT {rut} ya está registrado. Intente con otro.")
                    else:
                        break
                pasajero_dao.registrar_pasajero(nombre, apellido, rut, id_habitacion_responsable, responsable=False)
            pasajeros_restantes -= pasajeros_a_registrar - 1
            print(f"{pasajeros_a_registrar} pasajeros registrados en la habitación {id_habitacion_responsable}.")
        else:
            print(f"1 pasajero registrado en la habitación {id_habitacion_responsable}.")

        # Registrar los pasajeros restantes en otras habitaciones
        while pasajeros_restantes > 0:
            print(f"\nQuedan {pasajeros_restantes} pasajeros por registrar.")
            id_habitacion = int(input("Ingrese el ID de la siguiente habitación: "))
            habitacion_disponible = next((h for h in habitaciones_vacantes if h[0] == id_habitacion), None)

            if not habitacion_disponible:
                print(f"No se encontró una habitación vacante con ID {id_habitacion}.")
                continue

            capacidad_habitacion = habitacion_disponible[2]
            if pasajeros_restantes <= capacidad_habitacion:
                pasajeros_a_registrar = pasajeros_restantes
            else:
                pasajeros_a_registrar = capacidad_habitacion

            habitaciones_reservadas.append(id_habitacion)

            for i in range(pasajeros_a_registrar):
                print(f"\nIngrese los datos del pasajero {i + 1}:")
                while True:
                    nombre = input("Nombre: ")
                    apellido = input("Apellido: ")
                    rut = input("RUT: ")
                    if pasajero_dao.verificar_rut_existente(rut):
                        print(f"Error: El RUT {rut} ya está registrado. Intente con otro.")
                    else:
                        break
                pasajero_dao.registrar_pasajero(nombre, apellido, rut, id_habitacion, responsable=False)

            pasajeros_restantes -= pasajeros_a_registrar
            print(f"{pasajeros_a_registrar} pasajeros registrados en la habitación {id_habitacion}.")

        # Asignar responsable a todas las habitaciones reservadas
        print("Asignando responsable a las habitaciones reservadas...")
        for habitacion in habitaciones_reservadas:
            pasajero_dao.asignar_responsable_habitacion(id_responsable, habitacion)

        print(f"Registro completado. Habitaciones reservadas: {habitaciones_reservadas}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()
        input("Presione Enter para continuar...")


def ver_habitaciones(id_habitacion=None):
    limpiar_consola()

    habitaciones = habitacion_dao.obtener_habitaciones(id_habitacion)
    table = BeautifulTable()
    table.columns.header = ["ID", "Numero_Habitacion", "Pasajero_Admitidos", "Orientacion", "Estado", "Responsable"]
    
    for habitacion in habitaciones:
        responsable = f"{habitacion['responsable_nombre']} {habitacion['responsable_apellido']}" if habitacion['responsable_nombre'] and habitacion['responsable_apellido'] else ""
        table.rows.append([habitacion["id"], habitacion["numero_habitacion"], habitacion["pasajeros_admitidos"], habitacion["orientacion"], habitacion["estado"], responsable])
    
    print(table)
    input("Enter para volver. ")



def ver_pasajeros():
    limpiar_consola()
    try:
        conexion = Conexion()
        pasajero_dao = PasajeroDAO(conexion)
        pasajeros = pasajero_dao.obtener_pasajeros()

        if pasajeros:
            table = BeautifulTable()
            table.columns.header = ['ID', 'Nombre', 'Apellido', 'Rut', 'Habitación']

            for pasajero in pasajeros:
                id_pasajero, nombre, apellido, rut, id_habitacion = pasajero
                habitacion = id_habitacion 
                table.rows.append([id_pasajero, nombre, apellido, rut, habitacion])

            print("\nLista de Pasajeros:")
            print(table)
            input("Presiona Enter para salir.")

        else:
            print("No hay pasajeros registrados.")
            input("Presiona Enter para salir.")
    except Exception as e:
        print(f"Error al mostrar pasajeros: {e}")



def modificar_habitacion():
    limpiar_consola()
    try:
        habitacion_dao = HabitacionDao(conexion)
        habitaciones = habitacion_dao.obtener_habitaciones()

        if habitaciones:
            while True:
                table = BeautifulTable()
                table.columns.header = ['ID', 'Número Habitación', 'Capacidad', 'Orientación', 'Estado', 'Responsable']

                for habitacion in habitaciones:
                    table.rows.append([
                        habitacion['id'],
                        habitacion['numero_habitacion'],
                        habitacion['pasajeros_admitidos'],
                        habitacion['orientacion'],
                        habitacion['estado'],
                        f"{habitacion['responsable_nombre']} {habitacion['responsable_apellido']}" if habitacion['responsable_nombre'] else '-'
                    ])

                print("\nLista de Habitaciones Disponibles:")
                print(table)

                id_habitacion = input("\nIngrese el ID de la habitación que desea modificar (0 para cancelar): ")
                id_habitacion = int(id_habitacion)

                if id_habitacion == 0:
                    return

                while True:
                    try:
                        nuevo_numero = int(input("Nuevo número de habitación (1-100): "))
                        if nuevo_numero < 1 or nuevo_numero > 100:
                            print("Error: El número de la habitación debe estar entre 1 y 100.")
                            continue
                        # Verificar que el nuevo número no esté en uso por otra habitación
                        habitaciones_existentes = habitacion_dao.obtener2_habitaciones()
                        if any(habitacion['numero_habitacion'] == nuevo_numero and habitacion['id'] != id_habitacion for habitacion in habitaciones_existentes):
                            print(f"Error: El número de la habitación {nuevo_numero} ya está registrado.")
                            continue
                        break
                    except ValueError:
                        print("Error: Ingrese un número válido.")

                while True:
                    try:
                        nueva_capacidad = int(input("Nueva capacidad de la habitación (1-3): "))
                        if nueva_capacidad < 1 or nueva_capacidad > 3:
                            print("Error: La capacidad de la habitación debe estar entre 1 y 3.")
                            continue
                        break
                    except ValueError:
                        print("Error: Ingrese un número válido.")

                # Mostrar tabla de orientaciones disponibles
                orientaciones = habitacion_dao.obtener_orientaciones()
                orientaciones_table = BeautifulTable()
                orientaciones_table.columns.header = ['ID', 'Orientación']
                for orientacion in orientaciones:
                    orientaciones_table.rows.append([orientacion[0], orientacion[1]])

                print("\nOrientaciones Disponibles:")
                print(orientaciones_table)

                while True:
                    try:
                        id_orientacion = int(input("\nIngrese el ID de la nueva orientación: "))
                        if any(orientacion[0] == id_orientacion for orientacion in orientaciones):
                            break
                        else:
                            print("Error: ID de orientación no válido.")
                    except ValueError:
                        print("Error: Ingrese un ID válido.")

                habitacion_dao.modificar_habitacion(id_habitacion, nuevo_numero, nueva_capacidad, id_orientacion)

                print(f"Habitación con ID {id_habitacion} modificada correctamente.")

                opcion = input("\n¿Desea modificar otra habitación? (s/n): ").lower()
                if opcion != 's':
                    break

        else:
            print("No hay habitaciones registradas.")

    except ValueError:
        print("Error: Ingrese un ID válido.")
    except Exception as e:
        print(f"Error al modificar habitación: {e}")
        
        


def modificar_pasajero():
    limpiar_consola()
    try:
        pasajero_dao = PasajeroDAO(conexion)
        pasajeros = pasajero_dao.obtener_pasajeros()

        if pasajeros:
            while True:
                table_pasajeros = BeautifulTable()
                table_pasajeros.columns.header = ['ID', 'Nombre', 'Apellido', 'Rut', 'Habitación']

                for pasajero in pasajeros:
                    id_pasajero, nombre, apellido, rut, id_habitacion = pasajero
                    table_pasajeros.rows.append([id_pasajero, nombre, apellido, rut, id_habitacion])

                print("\nLista de Pasajeros Disponibles:")
                print(table_pasajeros)

                id_pasajero = input("\nIngrese el ID del pasajero que desea modificar (0 para cancelar): ")
                id_pasajero = int(id_pasajero)

                if id_pasajero == 0:
                    return

                nuevo_nombre = input("Nuevo nombre: ")
                nuevo_apellido = input("Nuevo apellido: ")
                nuevo_rut = input("Nuevo rut: ")

                pasajero_dao.modificar_pasajero(id_pasajero, nuevo_nombre, nuevo_apellido, nuevo_rut)
                conexion.connection.commit()

                print(f"Pasajero con ID {id_pasajero} modificado correctamente.")

                opcion = input("\n¿Desea modificar otro pasajero? (s/n): ").lower()
                if opcion != 's':
                    break

        else:
            print("No hay pasajeros registrados.")
    
    except ValueError:
        print("Error: Ingrese un ID válido.")
    except Exception as e:
        print(f"Error al modificar pasajero: {e}")

def eliminar_habitacion():
    limpiar_consola()
    
    try:
        habitacion_dao = HabitacionDao(conexion)  # Asegúrate de tener `conexion` definido adecuadamente
        habitaciones = habitacion_dao.obtener_habitaciones()

        if habitaciones:
            table = BeautifulTable()
            table.columns.header = ['ID', 'Número Habitación', 'Capacidad', 'Orientación', 'Estado']

            for habitacion in habitaciones:
                table.rows.append([habitacion["id"], habitacion["numero_habitacion"],
                                   habitacion["pasajeros_admitidos"], habitacion["orientacion"],
                                   habitacion["estado"]])

            print("\nLista de Habitaciones Disponibles:")
            print(table)

            id_habitacion = input("\nIngrese el ID de la habitación que desea eliminar (0 para cancelar): ")
            id_habitacion = int(id_habitacion)

            if id_habitacion == 0:
                return

            # Verificar si hay un pasajero asignado a esta habitación
            query_pasajero = "SELECT id FROM pasajero WHERE id_habitacion = %s"
            conexion.cursor.execute(query_pasajero, (id_habitacion,))
            pasajero = conexion.cursor.fetchone()

            if pasajero:
                id_pasajero = pasajero[0]
                # Si hay pasajero, eliminarlo
                delete_pasajero_query = "DELETE FROM pasajero WHERE id = %s"
                conexion.cursor.execute(delete_pasajero_query, (id_pasajero,))
                conexion.connection.commit()
                print(f"Pasajero con ID {id_pasajero} eliminado correctamente.")

            # Eliminar la habitación
            delete_habitacion_query = "DELETE FROM habitacion WHERE id = %s"
            conexion.cursor.execute(delete_habitacion_query, (id_habitacion,))
            conexion.connection.commit()

            print(f"Habitación con ID {id_habitacion} eliminada correctamente.")
            
            while True:
                opcion = input("\n¿Desea eliminar otra habitación? (s/n): ").lower()
                if opcion == 's':
                    eliminar_habitacion()
                else:
                    break

        else:
            print("No hay habitaciones registradas.")
        
    except mysql.connector.Error as err:
        print(f"Error al eliminar habitación: {err}")


def eliminar_pasajero():
    limpiar_consola()
    try:
        pasajero_dao = PasajeroDAO(conexion)
        pasajeros = pasajero_dao.obtener_pasajeros()

        if pasajeros:
            while True:
                table = BeautifulTable()
                table.columns.header = ['ID', 'Nombre', 'Apellido', 'Rut', 'Habitación']

                for pasajero in pasajeros:
                    id_pasajero, nombre, apellido, rut, id_habitacion = pasajero
                    habitacion = id_habitacion 
                    table.rows.append([id_pasajero, nombre, apellido, rut, habitacion])

                print("\nLista de Pasajeros:")
                print(table)

                id_pasajero = input("\nIngrese el ID del pasajero que desea eliminar (0 para cancelar): ")
                id_pasajero = int(id_pasajero)

                if id_pasajero == 0:
                    return

                # Verificar si el ID del pasajero existe
                pasajero_existe = any(pasajero[0] == id_pasajero for pasajero in pasajeros)
                if not pasajero_existe:
                    print(f"El pasajero con ID {id_pasajero} no existe. Por favor, ingrese un ID válido.")
                    continue

                pasajero_dao.eliminar_pasajero(id_pasajero)
                print(f"Pasajero con ID {id_pasajero} eliminado correctamente.")

                opcion = input("\n¿Desea eliminar otro pasajero? (s/n): ").lower()
                if opcion == 's':
                    eliminar_pasajero
                else:
                    break

                # Actualizar la lista de pasajeros después de la eliminación
                pasajeros = pasajero_dao.obtener_pasajeros()

        else:
            print("No hay pasajeros registrados.")
    except ValueError:
        print("Error: Ingrese un ID válido.")
    except Exception as e:
        print(f"Error al eliminar pasajero: {e}")








crear_administrador_si_no_existe()

while True:
        table = BeautifulTable()
        table.columns.header = ["=== Menu Principal ==="]
        table.rows.append(["1. Administrador"])
        table.rows.append(["2. Encargado"])
        table.rows.append(["3. Salir"])
        print(table)
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            menu_administrador()
        elif opcion == "2":
            menu_encargado()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente nuevamente.")