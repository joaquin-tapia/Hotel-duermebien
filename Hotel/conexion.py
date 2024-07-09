import mysql.connector

class Conexion:
    def __init__(self):
        self.__connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hotel3"
        )
        self.__cursor = self.__connection.cursor(buffered=True)

    def commit(self):
        self.__connection.commit()

    @property
    def connection(self):
        if not self.__connection.is_connected():
           
            self.__connection.reconnect(attempts=3, delay=5)
            self.__cursor = self.__connection.cursor(buffered=True)
           
        return self.__connection

    @property
    def cursor(self):
        if not self.__connection.is_connected():
            
            self.__connection.reconnect(attempts=3, delay=5)
            self.__cursor = self.__connection.cursor(buffered=True)
          
        return self.__cursor

    def rollback(self):
        self.__connection.rollback()

    def close(self):
        self.__cursor.close()
        self.__connection.close()