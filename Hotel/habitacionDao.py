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
            query = """
            SELECT h.id, h.numero_habitacion, h.pasajeros_admitidos, o.orientacion, h.estado, p.nombre AS responsable_nombre, p.apellido AS responsable_apellido
            FROM habitacion h
            JOIN orientacion_habitacion o ON h.id_orientacion = o.id
            LEFT JOIN pasajero_habitacion ph ON h.id = ph.id_habitacion
            LEFT JOIN pasajero p ON ph.id_pasajero = p.id
            WHERE h.id = %s
            """
            self.__conexion.cursor.execute(query, (id_habitacion,))
        else:
            query = """
            SELECT h.id, h.numero_habitacion, h.pasajeros_admitidos, o.orientacion, h.estado, p.nombre AS responsable_nombre, p.apellido AS responsable_apellido
            FROM habitacion h
            JOIN orientacion_habitacion o ON h.id_orientacion = o.id
            LEFT JOIN pasajero_habitacion ph ON h.id = ph.id_habitacion
            LEFT JOIN pasajero p ON ph.id_pasajero = p.id
            """
            self.__conexion.cursor.execute(query)
        
        columns = [column[0] for column in self.__conexion.cursor.description]
        return [dict(zip(columns, row)) for row in self.__conexion.cursor.fetchall()]
        
        # Obtener todos los resultados como diccionarios
        columns = [column[0] for column in self.__conexion.cursor.description]
        return [dict(zip(columns, row)) for row in self.__conexion.cursor.fetchall()]
    
    def obtener_habitacion_por_id(self, id_habitacion):
        query = "SELECT h.id, h.numero_habitacion, h.pasajeros_admitidos, o.orientacion, h.estado FROM habitacion h JOIN orientacion_habitacion o ON h.id_orientacion = o.id WHERE h.id = %s"
        self.__conexion.cursor.execute(query, (id_habitacion,))
        return self.__conexion.cursor.fetchone()

    def modificar_habitacion(self, id_habitacion, nuevo_numero, nueva_capacidad, id_orientacion):
        try:
            query = "UPDATE habitacion SET numero_habitacion = %s, pasajeros_admitidos = %s, id_orientacion = %s WHERE id = %s"
            self.__conexion.cursor.execute(query, (nuevo_numero, nueva_capacidad, id_orientacion, id_habitacion))
            self.__conexion.connection.commit()
            print(f"Habitación con ID {id_habitacion} modificada correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al modificar habitación: {err}")

    def eliminar_habitacion(self, id_habitacion):
        try:
            # Verificar si hay un pasajero asignado a esta habitación
            query_pasajero = "SELECT id FROM pasajero WHERE id_habitacion = %s"
            self.__conexion.cursor.execute(query_pasajero, (id_habitacion,))
            pasajero = self.__conexion.cursor.fetchone()

            if pasajero:
                id_pasajero = pasajero[0]
                # Si hay pasajero, eliminarlo
                delete_pasajero_query = "DELETE FROM pasajero WHERE id = %s"
                self.__conexion.cursor.execute(delete_pasajero_query, (id_pasajero,))
                self.__conexion.connection.commit()
                print(f"Pasajero con ID {id_pasajero} eliminado correctamente.")

            # Eliminar la habitación
            delete_habitacion_query = "DELETE FROM habitacion WHERE id = %s"
            self.__conexion.cursor.execute(delete_habitacion_query, (id_habitacion,))
            self.__conexion.connection.commit()

            print(f"Habitación con ID {id_habitacion} eliminada correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al eliminar habitación: {err}")

    def obtener_habitaciones_vacantes(self):


        query = """
        SELECT h.id, h.numero_habitacion, h.pasajeros_admitidos, o.orientacion
        FROM habitacion h
        JOIN orientacion_habitacion o ON h.id_orientacion = o.id
        WHERE h.estado = 'vacante'
        """
        self.__conexion.cursor.execute(query)
        return self.__conexion.cursor.fetchall()
    
    def obtener_orientaciones(self):
        try:
            query = "SELECT id, orientacion FROM orientacion_habitacion"
            self.__conexion.cursor.execute(query)
            return self.__conexion.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener orientaciones: {err}")


    def actualizar_estado_habitacion(self, id_habitacion, estado):
        try:
            query = "UPDATE habitacion SET estado = %s WHERE id = %s"
            self.__conexion.cursor.execute(query, (estado, id_habitacion))
            self.__conexion.connection.commit()
            print(f"Estado de la habitación con ID {id_habitacion} actualizado a '{estado}'.")
        except mysql.connector.Error as err:
            print(f"Error al actualizar estado de habitación: {err}")