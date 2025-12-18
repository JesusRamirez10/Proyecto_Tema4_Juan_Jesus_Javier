import json
from peewee import *
from playhouse.postgres_ext import *
from models.atracciones_model import AtraccionesModel
from models.visitantes_model import VisitantesModel
from models.tickets_model import TicketsModel

@staticmethod
def crear_visitante(nombre, email, altura, preferencias_json=None):
    try:
        # Los datos principales
        datos_visitante = {
            'nombre': nombre,
            'email': email,
            'altura': altura  # Valor por defecto, se puede actualizar luego
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

@staticmethod
def obtener_todos():
        try:
            visitantes = VisitantesModel.select()
            return list(visitantes)
        except Exception as e:
            print(f"Error al listar todos los visitantes: {e}")
            return []
@staticmethod
def obtener_visitantes_con_ticket_para_atraccion( atraccion_id):
        try:
            query = (VisitantesModel
            .select()
            .join(TicketsModel)
            .where(TicketsModel.atraccion == atraccion_id))
            return list(query)
        except Exception as e:
            print(f"Error al obtener visitantes con ticket para la atracción {atraccion_id}: {e}")
            return []
        
@staticmethod
def obtener_visitantes_preferencia_extrema():
    try:
        # Accedemos a la clave 'tipo_favorito' dentro del JSONB preferencias
        query = VisitantesModel.select().where(
            VisitantesModel.preferencias['tipo_favorito'] == 'extrema'
        )
        return list(query)
    except Exception as e:
        print(f"Error al obtener visitantes con preferencia extrema: {e}")
        return []

