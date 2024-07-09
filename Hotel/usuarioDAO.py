

class UsuarioDao:
    def __init__(self,conexion):
        self.__conexion = conexion

    def check_administrador(self):
        cursor = self.__conexion.cursor
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE cargo = 'administrador'")
        count = cursor.fetchone()[0]
        return count > 0

    def crear_administrador(self, nombre, contraseña):
        query = "INSERT INTO usuario (nombre, contraseña, cargo) VALUES (%s, %s, 'Administrador')"
        cursor = self.__conexion.cursor
        cursor.execute(query, (nombre, contraseña))
        self.__conexion.connection.commit()

    def crear_usuario(self,nombre, contraseña, cargo):
        query = "INSERT INTO usuario (nombre, contraseña, cargo) VALUES (%s, %s, %s)"
        self.__conexion.cursor.execute(query,(nombre,contraseña, cargo))
        self.__conexion.connection.commit()

    def obtener_usuarios(self):
        query = "SELECT id, nombre, cargo FROM usuario"
        self.__conexion.cursor.execute(query)
        usuarios = self.__conexion.cursor.fetchall()
        return usuarios
    
    def modificar_permisos(self,id_usuario, nuevo_cargo):
        query = "UPDATE usuario SET cargo = %s WHERE id = %s"
        self.__conexion.cursor.execute(query, (nuevo_cargo, id_usuario))
        self.__conexion.connection.commit()

    def eliminar_usuario(self, id_usuario):
        query = "DELETE FROM usuario WHERE id = %s"
        self.__conexion.cursor.execute(query,(id_usuario,))
        self.__conexion.connection.commit()
