from datetime import datetime
from peewee import *
from playhouse import postgres_ext
from models.basemodel import BaseModel

tipos_atraccion = (('extrema','Extrema'),('familiar','Familiar'),('infantil','Infantil'),('acuatica','Acuatica'),)

class AtraccionesModel(BaseModel):
     # Peewee usa AutoField por defecto para IDs primarias autoincrementables
    id = AutoField(primary_key = True)
    # CharField con longitud ilimitada 
    nombre = CharField(unique=True,null=False)
    # tipo (string) con restricción de los 4 tipos.
    tipo = CharField(choices=tipos_atraccion,null=False)
    # altura_minima que se guarda en CM
    altura_minima = IntegerField(null=False)
    #detalles(jsonb) con su estructura
    detalles = postgres_ext.BinaryJSONField(null=True,default={
        "duracion_segundos": 0,
        "capacidad_por_turno": 0,
        "intensidad": 0,
        "caracteristicas": [],
        "horarios": {
            "apertura": "",
            "cierre": "",
            "mantenimiento": []
        }
    })

    activa = BooleanField(default=True)

    fecha_inauguracion = DateField(default=datetime.now)



