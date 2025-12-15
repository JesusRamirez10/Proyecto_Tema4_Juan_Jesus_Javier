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
        
@staticmethod
def eliminar_visitante(visitante_id):
        try:
            # 1. Intentar obtener el visitante para mostrar un mensaje más informativo
            try:
                visitante = VisitantesModel.get_by_id(visitante_id)
                nombre_visitante = visitante.nombre
            except VisitantesModel.DoesNotExist:
                print(f"Advertencia: El visitante con ID {visitante_id} no existe.")
                return False

            # 2. Eliminar el registro
            # Peewee.Model.delete_by_id() devuelve True si el registro fue eliminado.
            # O puedes usar Model.delete().where(condition).execute()
            
            # Usaremos el método de la instancia para mayor claridad
            filas_eliminadas = visitante.delete_instance(recursive=True) # recursive=True podría ser útil si tuvieras más capas
            
            if filas_eliminadas > 0:
                print(f"Éxito: El visitante '{nombre_visitante}' (ID {visitante_id}) fue eliminado.")
                # La eliminación en cascada de los tickets es automática.
                return True
            else:
                # Esto es poco probable si ya lo obtuvimos, pero es un buen control
                print(f"Advertencia: No se pudo eliminar el visitante con ID {visitante_id}.")
                return False
                
        except Exception as e:
            print(f"Error desconocido al eliminar el visitante ID {visitante_id}: {e}")
            return False
