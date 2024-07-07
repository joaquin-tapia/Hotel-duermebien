class OrientacionDao:
    def __init__(self, conexion):
        self.__conexion = conexion

    def registrar_orientacion(self,orientacion):
        query = "INSERT INTO orientacion_habitacion(orientacion) VALUES (%s)"
        self.__conexion.cursor.execute(query, (orientacion,))
        self.__conexion.connection.commit()
    
    def obtener_orientaciones(self):
        query = "SELECT id, orientacion FROM orientacion_habitacion"
        self.__conexion.cursor.execute(query)
        orientaciones = self.__conexion.cursor.fetchall()
        return orientaciones
    
    def modificar_orientacion(self,nueva_orientacion, id):
        query = "UPDATE `orientacion_habitacion` SET `orientacion` = %s WHERE `orientacion_habitacion`.`id` = %s;"
        self.__conexion.cursor.execute(query, (nueva_orientacion, id))
        self.__conexion.connection.commit()

    def eliminar_orientacion(self, id_orientacion):
        query = "DELETE FROM `orientacion_habitacion` WHERE `orientacion_habitacion`.`id` = %s"
        self.__conexion.cursor.execute(query,(id_orientacion,))
        self.__conexion.connection.commit()
