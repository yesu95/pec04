"""Módulo de modelos de datos utilizando Pydantic para la API del catálogo."""

from pydantic import BaseModel

# Modelo base con los campos del catálogo
class ItemBase(BaseModel):
    titulo: str
    descripcion: str
    categoria: str
    precio: float

# Modelo para crear un elemento (el usuario no envía el ID, SQLite se encarga de generarlo automáticamente)
class ItemCreate(ItemBase):
    pass

# Modelo para responder al usuario cuando consulta información(incluye el ID)
class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True
