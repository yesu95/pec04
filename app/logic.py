"""Archivo para la lógica de la aplicación: funciones que interactúan con la base de datos y procesan la información."""
from app.database import get_connection
from app.models import *

"""Crear un elemento nuevo en la base de datos."""
def createItem(item: ItemCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO items (titulo, descripcion, categoria, precio) 
        VALUES (?, ?, ?, ?)
        """, 
        (
            item.titulo, 
            item.descripcion, 
            item.categoria, 
            item.precio
        ))

    conn.commit()
    item_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return ItemResponse(id=item_id, **item.model_dump())

"""Obtener todos los elementos de la base de datos."""
def getItem():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()

    items = [ItemResponse(**row) for row in rows]

    cursor.close()
    conn.close()

    return items

"""Obtener un elemento por su ID."""
def getItemById(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is not None:
        return ItemResponse(**row)
    else:
        return None

"""Actualizar un elemento existente en la base de datos."""
def updateItems(item_id: int, item: ItemCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE items 
        SET titulo = ?, descripcion = ?, categoria = ?, precio = ? 
        WHERE id = ?
        """, 
        (
            item.titulo, 
            item.descripcion, 
            item.categoria, 
            item.precio, 
            item_id
        ))

    conn.commit()
    cursor.close()
    conn.close()

"""Eliminar un elemento de la base de datos."""
def deleteItem(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))

    conn.commit()
    cursor.close()
    conn.close()