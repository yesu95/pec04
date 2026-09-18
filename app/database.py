import sqlite3
from sqlite3 import Error
from app.colors import *

DB_NAME = "mybase.db"

"""Crea y devuelve una conexión a la base de datos SQLite."""
def get_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        # Permite acceder a las columnas por nombre como si fuera un diccionario
        conn.row_factory = sqlite3.Row 
        return conn
    except Error as e:
        print(f"{R}\nError al conectar a la base de datos: {e}\n{RA}")
        return None

"""Inicia la base de datos y crea la tabla del catálogo si no existe."""
def init_db():
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Definimos la tabla "Items" para nuestro catálogo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    precio REAL NOT NULL
                );
            """)
            
            conn.commit()
            print(f"{G}\nBase de datos iniciada con éxito.\n{RA}")
        except Error as e:
            print(f"{R}\nError al crear la tabla: {e}\n{RA}")
        finally:
            conn.close()
    else:
        print(f"{R}\nError: No se pudo establecer conexión con la base de datos.\n{RA}")