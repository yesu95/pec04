from fastapi import FastAPI, HTTPException, status
from app.database import init_db
from app.models import ItemCreate, ItemResponse
from app.logic import *

# Se crea una instancia de FastAPI para la app
app = FastAPI(
    title="Sistema de Catálogo Digital",
    description="API para gestionar un catálogo digital.",
)

# Iniciar la base de datos al arrncar el server
@app.on_event("startup")
def startup_db():
    init_db()

# ENDPOINTS 
"""Crear un nuevo elemento en el catálogo."""
@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def crear_elemento(item: ItemCreate):
    return createItem(item)

"""Obtener la lista completa de elementos guardados."""
@app.get("/items", response_model=list[ItemResponse])
def listar_elementos():
    return getItem()

"""Buscar un elemento específico por su ID."""
@app.get("/items/{item_id}", response_model=ItemResponse)
def obtener_elemento(item_id: int):
    elemento = getItemById(item_id)
    if not elemento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El elemento con ID {item_id} no fue encontrado."
        )
    return elemento

"""Modificar los datos de un elemento existente por su ID."""
@app.put("/items/{item_id}", response_model=ItemResponse)
def actualizar_elemento(item_id: int, item: ItemCreate):
    elemento_actualizado = updateItems(item_id, item)
    if not elemento_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede actualizar. El elemento con ID {item_id} no existe."
        )
    return elemento_actualizado

"""Eliminar un elemento del catálogo de forma definitiva."""
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_elemento(item_id: int):
    eliminado = deleteItem(item_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede eliminar. El elemento con ID {item_id} no existe."
        )
    return None