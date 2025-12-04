import json
from peewee import *
from playhouse.postgres_ext import *
from models.atracciones_model import AtraccionesModel
from models.visitantes_model import VisitantesModel
from models.tickets_model import TicketsModel

@staticmethod
def crear_atraccion(nombre, tipo, altura_minima, detalles_json=None):  
        try:
            # Los datos principales 
            datos_atraccion = {
                'nombre': nombre,
                'tipo': tipo,
                'altura_minima': altura_minima
            }
            
            # Campo Opcional JSONB
            if detalles_json is not None:
                datos_atraccion['detalles'] = detalles_json
            
            # Creamos el registro
            return AtraccionesModel.create(**datos_atraccion)
            
        except IntegrityError as e:
            # Captura errores como nombre duplicado o que falten 
            print(f"Error de integridad (nombre duplicado o falta de dato requerido): {e}")
            return None
        except Exception as e:
            print(f"Error desconocido al crear la atracción {nombre}: {e}")
            return None