import json
import psycopg2
from peewee import *
from playhouse.postgres_ext import *
from models.atracciones_model import AtraccionesModel
from models.visitantes_model import VisitantesModel
from models.tickets_model import TicketsModel

class VisitantesRepo:

    def __init__(self, conn):
        self.conn = conn

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
    @staticmethod
    def obtener_todos():
        try:
            visitantes = VisitantesModel.select()
            return list(visitantes)
        except Exception as e:
            print(f"Error al listar todos los visitantes: {e}")
            return []
    @staticmethod
    def obtener_visitantes_con_ticket_para_atraccion(self, atraccion_id):
        try:
            query = (VisitantesModel
                     .select()
                     .join(TicketsModel)
                     .where(TicketsModel.atraccion == atraccion_id)
                    )
            return list(query)
        except Exception as e:
            print(f"Error al obtener visitantes con ticket para la atracción {atraccion_id}: {e}")
            return []
