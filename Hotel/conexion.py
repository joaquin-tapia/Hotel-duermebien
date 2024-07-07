import mysql.connector


class Conexion:
    def __init__(self):
        self.__connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "hotelduermebien"
        )
        self.__cursor = self.__connection.cursor()

    @property
    def commit(self):
        self.__connection.commit()
       
    @property
    def connection(self):
        return self.__connection
    @property
    def cursor(self):
        return self.__cursor
    


