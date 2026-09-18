"""
En MAIN se encuentra la aplicación principal y se encarga de iniciar el servidor web con FastAPI, 
preparar la base de datos al arrancar y definir las rutas (endpoints) HTTP para crear, consultar, actualizar y eliminar productos del catálogo.
"""

from fastapi import FastAPI, HTTPException, status
from app.database import init_db
from app.logic import createItem, getItem, getItemById, updateItems, deleteItem
from app.models import ItemCreate, ItemResponse

# Se crea la instancia de FastAPI para la APP

app = FastAPI(
    title="Sistema de catálogos de productos",
    description="API para gestionar un catálogo de productos utilizando FastAPI y SQLite.",
)

# Iniciar la base de datos al arrancacr el server
@app.on_event("startup")
def startup_event():
    init_db()

"""----------ENDPOINTS DE LA API----------"""

@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def createElement(item: ItemCreate):
    """Crear un nuevo elemento en el catálogo."""
    return createItem(item)

@app.get("/items/", response_model=list[ItemResponse])
def listItems():
    """Obtener todos los elementos del catálogo."""
    return getItem()

@app.get("/items/{item_id}", response_model=ItemResponse)
def getItemRoute(item_id: int):
    """Obtener un elemento por su ID."""
    elemento = getItemById(item_id)
    if not elemento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El elemento con ID {item_id} no fue encontrado."
        )
    return elemento

@app.put("/items/{item_id}", response_model=ItemResponse)
def updateItem(item_id: int, item: ItemCreate):
    """Modificar los datos de un elemento existente por su ID."""
    updatedItem = updateItems(item_id, item)
    if not updatedItem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede actualizar. El elemento con ID {item_id} no existe."
        )
    return updatedItem

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteItemRoute(item_id: int):
    """Eliminar un elemento del catálogo de forma definitiva."""
    deleted = deleteItem(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede eliminar. El elemento con ID {item_id} no existe."
        )
    return None