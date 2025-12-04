import json
from peewee import *
from playhouse.postgres_ext import *
from models.atracciones_model import AtraccionesModel
from models.visitantes_model import VisitantesModel
from models.tickets_model import TicketsModel

class VisitantesRepo:
    @staticmethod
    def crear_visitante(nombre, email, preferencias_json=None):
        try:
            # Los datos principales
            datos_visitante = {
                'nombre': nombre,
                'email': email
            }
            # Si se ponen preferencias, las añadimos. El campo es 'preferencias'.
            if preferencias_json is not None:
                datos_visitante['preferencias'] = preferencias_json
            
            #'altura' es un campo requerido 
            # Este método asume que el campo 'altura' se proporcionará en el JSON si no se incluye aquí.
            # Solo incluiremos los campos que se especifican.
            
            return VisitantesModel.create(**datos_visitante)
            
        except Exception as e:
            print(f"Error insertando al visitante {nombre}: {e}")
            return None
