import mysql.connector
class HabitacionDao:
    def __init__(self, conexion):
        self.__conexion = conexion

    def registrar_habitacion(self, numero_habitacion, pasajeros_admitidos, id_orientacion, estado):
        try:
            query = "INSERT INTO habitacion (numero_habitacion, pasajeros_admitidos, id_orientacion, estado) VALUES (%s, %s, %s, %s)"
            self.__conexion.cursor.execute(query, (numero_habitacion, pasajeros_admitidos, id_orientacion, estado))
            self.__conexion.connection.commit()
            print(f"Habitación {numero_habitacion} registrada correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al registrar habitación: {err}")

    def verificar_disponibilidad(self, id_habitacion):
        try:
            query = "SELECT estado FROM habitacion WHERE id = %s"
            self.__conexion.cursor.execute(query, (id_habitacion,))
            estado = self.__conexion.cursor.fetchone()
            return estado[0] == "vacante" if estado else False
        except mysql.connector.Error as err:
            print(f"Error al verificar disponibilidad: {err}")

    def obtener_habitaciones(self, id_habitacion=None):
        if id_habitacion:
            query = "SELECT h.id, h.numero_habitacion, h.pasajeros_admitidos, o.orientacion, h.estado FROM habitacion h JOIN orientacion_habitacion o ON h.id = o.id WHERE h.id = %s"
            self.__conexion.cursor.execute(query, (id_habitacion,))
        else:
            query = "SELECT h.id, h.numero_habitacion, h.pasajeros_admitidos, o.orientacion, h.estado FROM habitacion h JOIN orientacion_habitacion o ON h.id_orientacion = o.id"
            self.__conexion.cursor.execute(query)
        return self.__conexion.cursor.fetchall()

    
    def obtener_habitacion_por_id(self, id_habitacion):
        query = "SELECT h.id, h.numero_habitacion, h.pasajeros_admitidos, o.orientacion, h.estado FROM habitacion h JOIN orientacion_habitacion o ON h.id_orientacion = o.id WHERE h.id = %s"
        self.__conexion.cursor.execute(query, (id_habitacion,))
        return self.__conexion.cursor.fetchone()

    def modificar_habitacion(self, id_habitacion, numero_habitacion, pasajeros_admitidos, id_orientacion, estado):
        try:
            query = "UPDATE habitacion SET numero_habitacion = %s, pasajeros_admitidos = %s, id_orientacion = %s, estado = %s WHERE id = %s"
            self.__conexion.cursor.execute(query, (numero_habitacion, pasajeros_admitidos, id_orientacion, estado, id_habitacion))
            self.__conexion.connection.commit()
            print(f"Habitación con ID {id_habitacion} modificada correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al modificar habitación: {err}")

    def eliminar_habitacion(self, id_habitacion):
        try:
            query = "DELETE FROM habitacion WHERE id = %s"
            self.__conexion.cursor.execute(query, (id_habitacion,))
            self.__conexion.connection.commit()
            print(f"Habitación con ID {id_habitacion} eliminada correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al eliminar habitación: {err}")