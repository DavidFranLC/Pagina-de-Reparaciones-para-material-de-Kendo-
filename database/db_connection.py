import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # tu contraseña de MySQL si la tienes
        database="kendo_reparaciones"
    )
    return connection
