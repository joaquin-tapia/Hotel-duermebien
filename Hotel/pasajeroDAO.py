
import mysql.connector
class PasajeroDAO:
    def __init__(self, conexion):
        self.__conexion = conexion

    def registrar_pasajero(self, nombre, rut, id_habitacion):
        try:
            query = "INSERT INTO pasajero (nombre, rut) VALUES (%s, %s)"
            self.__conexion.cursor.execute(query, (nombre, rut))
            self.__conexion.connection.commit()

            update_query = "UPDATE habitacion SET estado = 'Ocupada' WHERE id = %s"
            self.__conexion.cursor.execute(update_query, (id_habitacion,))
            self.__conexion.connection.commit()

            print(f"Pasajero {nombre} con RUT {rut} registrado correctamente en la habitación {id_habitacion}.")
        except mysql.connector.Error as err:
            print(f"Error al registrar pasajero: {err}")

    def obtener_pasajeros(self):
        try:
            query = "SELECT id, nombre, rut FROM pasajero"
            self.__conexion.cursor.execute(query)
            return self.__conexion.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener pasajeros: {err}")

    def obtener_pasajero_por_id(self, id_pasajero):
     with self.connection:
        return self.connection.execute("SELECT * FROM pasajeros WHERE id = ?", (id_pasajero,)).fetchone()

    def modificar_pasajero(self, id_pasajero, nombre, rut, id_habitacion):
        try:
            query = "UPDATE pasajero SET nombre = %s, rut = %s, id_habitacion = %s WHERE id = %s"
            self.__conexion.cursor.execute(query, (nombre, rut, id_habitacion, id_pasajero))
            self.__conexion.connection.commit()

            update_query = "UPDATE habitacion SET estado = 'Ocupada' WHERE id = %s"
            self.__conexion.cursor.execute(update_query, (id_habitacion,))
            self.__conexion.connection.commit()

            print(f"Pasajero con ID {id_pasajero} modificado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al modificar pasajero: {err}")

    def eliminar_pasajero(self, id_pasajero):
        try:
            query = "DELETE FROM pasajero WHERE id = %s"
            self.__conexion.cursor.execute(query, (id_pasajero,))
            self.__conexion.connection.commit()
            print(f"Pasajero con ID {id_pasajero} eliminado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al eliminar pasajero: {err}")