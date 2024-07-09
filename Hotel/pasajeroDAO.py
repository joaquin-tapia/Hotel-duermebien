
import mysql.connector

class PasajeroDAO:
    def __init__(self, conexion):
        self.__conexion = conexion

    
    def registrar_pasajero(self, nombre, apellido, rut, id_habitacion, responsable=False):
        try:
            connection = self.__conexion.connection
            

            # Insertar el pasajero en la tabla pasajero
            sql = "INSERT INTO pasajero (nombre, apellido, rut, id_habitacion) VALUES (%s, %s, %s, %s)"
            cursor = connection.cursor()
            cursor.execute(sql, (nombre, apellido, rut, id_habitacion))
            id_pasajero = cursor.lastrowid
            print(f"Pasajero {nombre} {apellido} registrado con ID {id_pasajero}.")

            # Si es responsable, registrar en pasajero_habitacion marcando como responsable
            if responsable:
                sql_responsable = "INSERT INTO pasajero_habitacion (id_pasajero, id_habitacion, responsable) VALUES (%s, %s, %s)"
                cursor.execute(sql_responsable, (id_pasajero, id_habitacion, 1))
                print(f"Responsable asignado en la habitación {id_habitacion}.")

            # Actualizar el estado de la habitación a "ocupado"
            update_query = "UPDATE habitacion SET estado = 'ocupada' WHERE id = %s"
            cursor.execute(update_query, (id_habitacion,))
            connection.commit()  # Confirmar la transacción

            return id_pasajero

        except mysql.connector.Error as error:
            print(f"Error de MySQL: {error}")
            connection.rollback()
            raise Exception(f"Error al registrar pasajero: {error}")

        except Exception as e:
            print(f"Error general: {e}")
            raise e

        finally:
            cursor.close()  # Cerrar el cursor después de usarlo


    def asignar_responsable_habitacion(self, id_responsable, id_habitacion):
        try:
            cursor = self.__conexion.cursor
            
            # Verificar el estado de la conexión antes de ejecutar la consulta
            if not self.__conexion.connection.is_connected():
                print("La conexión se perdió. Intentando reconectar...")
                self.__conexion.connection.reconnect(attempts=3, delay=5)
                cursor = self.__conexion.cursor

            sql = "UPDATE pasajero_habitacion SET responsable = 1 WHERE id_pasajero = %s AND id_habitacion = %s"
            cursor.execute(sql, (id_responsable, id_habitacion))
            self.__conexion.commit()
            print(f"Responsable {id_responsable} asignado a la habitación {id_habitacion}.")
        except mysql.connector.Error as error:
            print(f"Error de MySQL: {error}")
            self.__conexion.rollback()
            raise Exception(f"Error al asignar responsable a la habitación: {error}")
        finally:
            cursor.close()


    def obtener_pasajeros(self):
        try:
            query = """
                SELECT p.id, p.nombre, p.apellido, p.rut, h.numero_habitacion
                FROM pasajero p
                LEFT JOIN habitacion h ON p.id_habitacion = h.id
            """
            self.__conexion.cursor.execute(query)
            return self.__conexion.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error al obtener pasajeros: {err}")

    def obtener_pasajero(self, id_pasajero):
        for pasajero in self.obtener_pasajeros():
            if pasajero.id == id_pasajero:
                return pasajero
        return None

    def modificar_pasajero(self, id_pasajero, nombre, apellido, rut):
        try:
            query = "UPDATE pasajero SET nombre = %s, apellido = %s, rut = %s WHERE id = %s"
            self.__conexion.cursor.execute(query, (nombre, apellido, rut, id_pasajero))
            self.__conexion.connection.commit()

            print(f"Pasajero con ID {id_pasajero} modificado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al modificar pasajero: {err}")
    

    
    def eliminar_pasajero(self, id_pasajero):
        try:
            # Obtener el id de la habitación del pasajero antes de eliminarlo
            query = "SELECT id_habitacion FROM pasajero WHERE id = %s"
            self.__conexion.cursor.execute(query, (id_pasajero,))
            habitacion_id = self.__conexion.cursor.fetchone()[0]

            # Eliminar referencias de la tabla pasajero_habitacion
            delete_references_query = "DELETE FROM pasajero_habitacion WHERE id_pasajero = %s"
            self.__conexion.cursor.execute(delete_references_query, (id_pasajero,))
            self.__conexion.connection.commit()

            # Eliminar el pasajero
            delete_query = "DELETE FROM pasajero WHERE id = %s"
            self.__conexion.cursor.execute(delete_query, (id_pasajero,))
            self.__conexion.connection.commit()

            # Verificar si quedan pasajeros en la habitación
            check_query = "SELECT COUNT(*) FROM pasajero WHERE id_habitacion = %s"
            self.__conexion.cursor.execute(check_query, (habitacion_id,))
            count = self.__conexion.cursor.fetchone()[0]

            # Si no quedan pasajeros, actualizar el estado de la habitación a "vacante"
            if count == 0:
                update_query = "UPDATE habitacion SET estado = 'vacante' WHERE id = %s"
                self.__conexion.cursor.execute(update_query, (habitacion_id,))
                self.__conexion.connection.commit()

            print(f"Pasajero con ID {id_pasajero} eliminado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al eliminar pasajero: {err}")

    def verificar_rut_existente(self, rut):
        try:
            query = "SELECT COUNT(*) FROM pasajero WHERE rut = %s"
            self.__conexion.cursor.execute(query, (rut,))
            count = self.__conexion.cursor.fetchone()[0]
            return count > 0
        except mysql.connector.Error as err:
            print(f"Error al verificar RUT existente: {err}")
            return False