import psycopg2
import bcrypt
from conexion import Conexion


class UsuarioDao:
    def __init__(self, conexion):
        self.__conexion = conexion

    def verificar_credenciales(self, nombre, contraseña):
        query = "SELECT contraseña FROM usuario WHERE nombre = %s"
        self.__conexion.cursor.execute(query, (nombre,))
        result = self.__conexion.cursor.fetchone()
        if result:
            contraseña_hash = result[0]
            return bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_hash.encode('utf-8'))
        return False

    def obtener_cargo(self, nombre):
        query = "SELECT cargo FROM usuario WHERE nombre = %s"
        self.__conexion.cursor.execute(query, (nombre,))
        result = self.__conexion.cursor.fetchone()
        if result:
            return result[0]
        return None

    def check_administrador(self):
        query = "SELECT COUNT(*) FROM usuario WHERE cargo = 'Administrador'"
        self.__conexion.cursor.execute(query)
        count = self.__conexion.cursor.fetchone()[0]
        return count > 0

    def crear_administrador(self, nombre, contraseña):
        contraseña_hash = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = "INSERT INTO usuario (nombre, contraseña, cargo) VALUES (%s, %s, 'Administrador')"
        self.__conexion.cursor.execute(query, (nombre, contraseña_hash))
        self.__conexion.commit()

    def crear_usuario(self, nombre, contraseña, cargo):
        contraseña_hash = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = "INSERT INTO usuario (nombre, contraseña, cargo) VALUES (%s, %s, %s)"
        self.__conexion.cursor.execute(query, (nombre, contraseña_hash, cargo))
        self.__conexion.commit()

    def obtener_usuarios(self):
        query = "SELECT id, nombre, cargo FROM usuario"
        self.__conexion.cursor.execute(query)
        usuarios = self.__conexion.cursor.fetchall()
        return usuarios

    def modificar_permisos(self, id_usuario, nuevo_cargo):
        query = "UPDATE usuario SET cargo = %s WHERE id = %s"
        self.__conexion.cursor.execute(query, (nuevo_cargo, id_usuario))
        self.__conexion.commit()

    def eliminar_usuario(self, id_usuario):
        query = "DELETE FROM usuario WHERE id = %s"
        self.__conexion.cursor.execute(query, (id_usuario,))
        self.__conexion.commit()
