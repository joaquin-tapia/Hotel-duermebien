
from conexion import Conexion
from orientacionDao import OrientacionDao
from usuarioDAO import UsuarioDao
from pasajeroDAO import PasajeroDAO
from habitacionDao import HabitacionDao
from beautifultable import BeautifulTable
from login import Login
import getpass
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
    conexion = Conexion()
    usuario_dao = UsuarioDao(conexion)

    if not usuario_dao.check_administrador():
        table = BeautifulTable()
        table.columns.header = ["Hotel Duerme Bien"]
        table.rows.append(["No hay un administrador en el sistema. Por favor cree uno"])
        print(table)

        nombre = input("Ingrese el nombre del administrador: ")
        contraseña = input("Ingrese una contreseña : ")
        usuario_dao.crear_administrador(nombre, contraseña)

        table.clear()
        table.rows.append(["Administrador creado exitosamente"])
        print(table)
        
        
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
        table.rows.append(["6. Cerrar sesion"])

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
            siguiente_paso = Login.cerrar_sesion()
            if siguiente_paso == 'login':
                return

        else:
            print("Opcion Invalida. Intente Nuevamente")


def ver_usuarios():

    while True:
        limpiar_consola()
        usuarios = usuario_dao.obtener_usuarios()
        table = BeautifulTable()
        table.columns.header = ["ID", "Nombre", "Cargo"]
        for usuario in usuarios:
            table.rows.append([usuario[0], usuario[1], usuario[2]])
        print(table)

        opcion = input("0. Para volver. ")
        if opcion == "0":
            break
   


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
    while True:
        limpiar_consola()
        id_usuario = input("Ingrese el ID del usuario que desea modificar: ")
        usuario = next((u for u in usuario_dao.obtener_usuarios() if u[0] == int(id_usuario)), None)
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
                limpiar_consola()
                usuarios = usuario_dao.obtener_usuarios()
                table = BeautifulTable()
                table.columns.header = ["ID", "Nombre", "Cargo"]
                for usuario in usuarios:
                    table.rows.append([usuario[0], usuario[1], usuario[2]])
                print(table)
        else:
             print("Usuario no encontrado")

        opcion = input("0. Para volver. ")
        if opcion == "0":
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
        id_usuario = input("Ingrese el ID del usuario que desea eliminar: ")
        confirmacion = input(f"Esta seguro que desea eliminar al usuario {id_usuario} (S/N?) ").upper()

        if confirmacion == "S":
            usuario_dao.eliminar_usuario(id_usuario)
            print(f"Usuario {id_usuario} eliminado correctamente.")

        else:
            print("Operacion cancelada.")

        opcion = input("0. Para volver. ")
        if opcion == "0":
            break


def eliminar_usuario():
    
    while True:
        limpiar_consola()
        id_usuario = input("Ingrese el ID del usuario que desea eliminar: ")
        confirmacion = input(f"Esta seguro que desea eliminar al usuario {id_usuario} (S/N?) ").upper()

        if confirmacion == "S":
            usuario_dao.eliminar_usuario(id_usuario)
            print(f"Usuario {id_usuario} eliminado correctamente.")

        else:
            print("Operacion cancelada.")

        opcion = input("0. Para volver. ")
        if opcion == "0":
            break
    

# main.py

def menu_encargado():
    while True:
        limpiar_consola()
        table = BeautifulTable()
        table.columns.header = ["=== Menu Encargado ==="]
        table.rows.append(["1. Ver Habitaciones "])
        table.rows.append(["2. Registrar Habitacion"])
        table.rows.append(["3. Modificar Habitacion"])
        table.rows.append(["4. Ver Pasajeros "])
        table.rows.append(["5. Registrar Pasajero"])
        table.rows.append(["6. Modificar Pasajero "])
        table.rows.append(["7. Cerrar Sesion"])

        print(table)

        opcion = int(input("Selecione una opcion:"))

        if opcion == 1:
            ver_habitaciones()
        
        elif opcion == 2:
            registrar_habitacion()
        
        elif opcion == 3:
            modificar_habitacion()

        elif opcion == 4:
            ver_pasajeros()
        
        elif opcion == 5:
            registrar_pasajero()
        
        elif opcion == 6:
            modificar_pasajero()

        elif opcion == 7:
            siguiente_paso = Login.cerrar_sesion()
            if siguiente_paso == 'login':
                return

        else:
            print("Opcion invalida. Intente nuevamente")


    
def registrar_habitacion():
    limpiar_consola()
    numero_habitacion = input("Ingrese el numero de la habitacion: ")
    pasajeros_admitidos = int(input("Capacidad de la habitacion: "))
    orientacion = input("Ingrese la orientacion de la habitacion: ")
    estado = "vacante"
    habitacion_dao.registrar_habitacion(numero_habitacion, pasajeros_admitidos, orientacion, estado)
    
    print("Habitacion Registrada Correctamente.")


def registrar_pasajero():
    limpiar_consola()

    nombre = input("Ingrese el nombre del pasajero: ")
    rut = input("Ingrese el RUT del pasajero: ")  
    id_habitacion = int(input("Ingrese el ID de la habitacion: "))

    if habitacion_dao.verificar_disponibilidad(id_habitacion):
        pasajero_dao.registrar_pasajero(nombre, rut, id_habitacion)  
        print("Pasajero registrado correctamente.")
    else:
        print("La habitacion no está disponible")

def ver_habitaciones(id_habitacion=None):
    limpiar_consola()

    habitaciones = habitacion_dao.obtener_habitaciones(id_habitacion)
    table = BeautifulTable()
    table.columns.header = ["ID", "Numero_Habitacion", "Pasajero_Admitidos", "Orientacion", "Estado"]
    for habitacion in habitaciones:
        table.rows.append(habitacion)
    
    print(table)

    input("0. para volver: ")


def ver_pasajeros():
    limpiar_consola()
    pasajeros = pasajero_dao.obtener_pasajeros()
    if pasajeros:
        table = BeautifulTable()
        table.columns.header = ["ID", "Nombre", "RUT"]
        for pasajero in pasajeros:
            table.rows.append([pasajero[0], pasajero[1], pasajero[2]])
        print(table)
    else:
        print("No hay pasajeros registrados.")
    
    input("Presione Enter para volver.")


def modificar_habitacion():
    while True:
        limpiar_consola()
        id_habitacion = int(input("Ïngrese el Id de la habitacion que desea modificar: "))
        habitacion = habitacion_dao.obtener_habitacion_por_id(id_habitacion)

        if habitacion:
            id_habitacion = input(f"Ingrese el id de la habitacion a corregir: (actual: {habitacion[0]})")
            numero_habitacion = input(f"Ingrese el numero de la habitacion: (actual: {habitacion[1]})")
            pasajeros_admitidos = input(f"Ingrese la cantidad de pasajeros admitidos: (actual: {habitacion[2]})")
            id_orientacion = input(f"Ingrese el id de la orientacion: (actual: {habitacion[3]})")
            estado = input(f"Ingrese el estado de la habitacion: (actual: {habitacion[4]})")

            habitacion_dao.modificar_habitacion(id_habitacion, numero_habitacion, pasajeros_admitidos, id_orientacion, estado)
            print("Informacion de la habitacion modificada correctamente.")
        else:
            print("Pasajero no encontrado.")
        
        


def modificar_pasajero():
    while True:
        limpiar_consola()
        id_pasajero = int(input("Ingrese el ID del pasajero que desea modificar: "))
        pasajero = pasajero_dao.obtener_pasajero(id_pasajero)

        if pasajero:
            nombre = input(f"Ingrese correcion de nombre del pasajero: (actual: {pasajero[1]}): ")
            rut = input(f"Ingrese correcion de rut del pasajero: (actual: {pasajero[2]}): ")
            id_habitacion = input(f"Ingrese nueva habitacion del pasajero: (actual: {pasajero[3]}): ")

            pasajero_dao.modificar_pasajero(id,pasajero, nombre, rut, id_habitacion)
            print("Informacion del pasajero modificada correctamente.")
        else:
            print("Pasajero no encontrado.")

        opcion = int(input("0. Para volver"))
        if opcion == 0:
            break

def eliminar_habitacion():
    limpiar_consola()
    id_habitacion = int(input("Ingrese el ID de la habitacion que desea eliminar: "))
    confirmacion = input(f"Esta seguro de que desea elimar la habitacion {id_habitacion}? (S/N): ").upper()

    if confirmacion == "S":
        habitacion_dao.eliminar_habitacion(id_habitacion)

    else: 
        print("Operacion cancelada.")


def eliminar_pasajero():
    limpiar_consola()
    id_pasajero = int(input("Ingrese el ID del pasajero que desea eliminar: "))
    confirmacion = input(f"Esta seguro de que desea elimar la habitacion {id_pasajero}? (S/N): ").upper()

    if confirmacion == "S":
        pasajero_dao.eliminar_pasajero(id_pasajero)
    
    else: 
        print("Operacion cancelada")


if __name__ == "__main__":
    crear_administrador_si_no_existe()

    while True:
        limpiar_consola()
        usuario = Login.login() #llamando al login

        if usuario:
            usuario_dao = UsuarioDao(conexion)
            cargo = usuario_dao.obtener_cargo(usuario)

            if cargo == "Administrador":
                menu_administrador()
            elif cargo == "Encargado":
                menu_encargado()
            else:
                print("Cargo no reconocido.")
  






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
        print("Opcion no valida. Intente nuevamente")




