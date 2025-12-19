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
    
@staticmethod
def marcar_ticket_usado(ticket_id):
        try:
            # 1. Buscar el ticket
            ticket = TicketsModel.get_by_id(ticket_id)
            
            # 2. Verificar si ya fue usado
            if ticket.usado:
                print(f"Advertencia: El ticket con ID {ticket_id} ya fue marcado como usado el {ticket.fecha_uso}.")
                # Devolvemos el ticket existente para evitar una actualización innecesaria
                return ticket 
                
            # 3. Si no ha sido usado, actualizar los campos
            ticket.usado = True
            ticket.fecha_uso = datetime.now() # Registramos la fecha y hora de uso
            
            # 4. Guardar los cambios en la base de datos
            ticket.save()
            
            print(f"Éxito: Ticket ID {ticket_id} marcado como usado a las {ticket.fecha_uso}.")
            return ticket
            
        except TicketsModel.DoesNotExist:
            # Captura si el ID del ticket no existe
            print(f"Error: El ticket con ID {ticket_id} no existe.")
            return None
        except Exception as e:
            # Captura cualquier otro error durante la actualización
            print(f"Error desconocido al marcar el ticket ID {ticket_id} como usado: {e}")
            return None

@staticmethod
def obtener_todos():
        try:
            tickets = TicketsModel.select() #Realiza una consulta para obtener todos los tickets
            return list(tickets) #Convierte el resultado en una lista y lo devuelve
        except Exception as e:
            print(f"Error al obtener todos los tickets: {e}") #Captura cualquier error y lo imprime
            return []
        
@staticmethod
def obtener_un_ticket(ticket_id):
        try:
            ticket = TicketsModel.get_by_id(ticket_id)
            return ticket
        except TicketsModel.DoesNotExist:
            print(f"Error: El ticket con ID {ticket_id} no existe.")
            return None
        except Exception as e:
            print(f"Error al obtener el ticket {ticket_id}: {e}")
            return None
@staticmethod
def obtener_tickets_por_visitante(visitante_id):
        try:
            visitante_instancia = VisitantesModel.get_by_id(visitante_id)
            tickets = TicketsModel.select().where(TicketsModel.visitante == visitante_instancia)
            return list(tickets)
        except VisitantesModel.DoesNotExist:
            print(f"Error: El visitante con ID {visitante_id} no existe.")
            return []
        except Exception as e:
            print(f"Error al obtener tickets para el visitante {visitante_id}: {e}")
            return []
@staticmethod
def obtener_tickets_por_atraccion(atraccion_id): 
        try:
            atraccion_instancia = AtraccionesModel.get_by_id(atraccion_id)
            tickets = TicketsModel.select().where(TicketsModel.atraccion == atraccion_instancia)
            return list(tickets)
        except AtraccionesModel.DoesNotExist:
            print(f"Error: La atracción con ID {atraccion_id} no existe.")
            return []
        except Exception as e:
            print(f"Error al obtener tickets para la atracción {atraccion_id}: {e}")
            return []

@staticmethod
def obtener_tickets_colegio_economicos():
    try:
        # Filtramos de forma directa:
        # 1. El tipo de ticket debe ser 'colegio'
        # 2. El precio (dentro de detalles_compra) debe ser menor a 30
        query = TicketsModel.select().where(
            TicketsModel.tipo_ticket == 'colegio',
            TicketsModel.detalles_compra['precio'] < 30
        )
        return list(query)
    except Exception as e:
        print(f"Error al obtener tickets: {e}")
        return []
    

@staticmethod
def cambiar_precio_ticket(ticket_id, nuevo_precio):
    """
    Cambia el precio en detalles_compra de un ticket específico
    """
    try:
        # 1. Obtener el ticket
        ticket = TicketsModel.get_by_id(ticket_id)
        
        # 2. Obtener los detalles actuales
        detalles = ticket.detalles_compra
        
        # 3. Guardar el precio anterior para información
        precio_anterior = detalles.get('precio', 0)
        
        # 4. Modificar el precio en el diccionario
        detalles['precio'] = nuevo_precio
        
        # 5. Actualizar el campo JSONB completo
        ticket.detalles_compra = detalles
        
        # 6. Guardar los cambios
        ticket.save()
        
        print(f"✅ Precio del ticket ID {ticket_id} actualizado:")
        print(f"   Precio anterior: ${precio_anterior}")
        print(f"   Precio nuevo: ${nuevo_precio}")
        
        return ticket
        
    except TicketsModel.DoesNotExist:
        print(f"❌ Error: El ticket con ID {ticket_id} no existe.")
        return None
    except Exception as e:
        print(f"❌ Error al cambiar el precio del ticket ID {ticket_id}: {e}")
        return None
    
@staticmethod
def obtener_tickets_descuento_estudiante():
     try:
        # Accedemos al array de descuentos dentro del JSONB detalles_compra
        query = TicketsModel.select().where(
             TicketsModel.detalles_compra['descuentos'].contains(['estudiante'])
        )
        return list(query)
     except Exception as e:
          # Devolvemos una lista vacía en caso de error
          print(f"Error al obtener tickets con descuento de estudiante: {e}")
          return []
