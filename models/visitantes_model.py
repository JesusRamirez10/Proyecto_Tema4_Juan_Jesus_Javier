from datetime import datetime
from peewee import *
from playhouse import postgres_ext
from models.basemodel import BaseModel

class VisitantesModel(BaseModel):
    # Peewee usa AutoField por defecto para IDs primarias autoincrementables
    id = AutoField(primary_key=True) 
    
    # CharField con longitud ilimitada 
    nombre = CharField(null=False) 
    
    # CharField con restricción de único y no nulo
    email = CharField(null=False, unique=True) 
    
    # IntegerField
    altura = IntegerField(null=False) 
    
    # fecha_registro (datetime)
    # DateTimeField con valor por defecto
    fecha_registro = DateTimeField(default=datetime.now)

    preferencias = postgres_ext.BinaryJSONField(null=True, default={
        'tipo_favorito': '',
        'restricciones': [],
        'historial_visitas': []
    })
