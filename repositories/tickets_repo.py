import json
from datetime import datetime
from peewee import *
from playhouse.postgres_ext import *
from models.atracciones_model import AtraccionesModel
from models.visitantes_model import VisitantesModel
from models.tickets_model import TicketsModel

@staticmethod
def crear_ticket(visitante_id, fecha_visita, tipo_ticket, detalles_compra_json, atraccion_id):
        try:

            # Peewee necesita las instancias de los modelos para las claves foraneas
            # Esto lanzará DoesNotExist si los IDs no existen.
            visitante_instancia = VisitantesModel.get_by_id(visitante_id)
            atraccion_instancia = AtraccionesModel.get_by_id(atraccion_id)
            
            # 2.Datos del ticket
            datos_ticket = {
                # Claves foráneas (pasando las instancias de los modelos)
                'visitante': visitante_instancia,
                'atraccion': atraccion_instancia,
                
                # Datos principales
                'fecha_visita': fecha_visita,
                'tipo_ticket': tipo_ticket,
                'detalles_compra': detalles_compra_json, 
                'fecha_emision': datetime.now() # Fecha de creación/emisión del registro
            }
            
            # 3. Creamos el registro en la base de datos
            return TicketsModel.create(**datos_ticket)
            
        #  Manejo de Errores 
            
        except VisitantesModel.DoesNotExist:
            # Captura si el ID del visitante no existe
            print(f"Error: El visitante con ID {visitante_id} no existe.")
            return None
        except AtraccionesModel.DoesNotExist:
            # Captura si el ID de la atracción no existe
            print(f"Error: La atracción con ID {atraccion_id} no existe.")
            return None
        except IntegrityError as e:
            # Captura errores de la base de datos (datos faltantes o violación de restricción)
            print(f"Error de integridad (FK inválida o falta de dato requerido): {e}")
            return None
        except Exception as e:
            # Captura cualquier otro error desconocido
            print(f"Error desconocido al crear el ticket para visitante {visitante_id}: {e}")
            return None