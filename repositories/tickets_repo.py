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
        visitante_instancia = VisitantesModel.get_by_id(visitante_id)
        atraccion_instancia = AtraccionesModel.get_by_id(atraccion_id)
        
        datos_ticket = {
            'visitante': visitante_instancia,
            'atraccion': atraccion_instancia,
            'fecha_visita': fecha_visita,
            'tipo_ticket': tipo_ticket,
            'detalles_compra': detalles_compra_json, 
            'fecha_emision': datetime.now()
        }
        
        return TicketsModel.create(**datos_ticket)
        
    except VisitantesModel.DoesNotExist:
        print(f"Error: El visitante con ID {visitante_id} no existe.")
        return None
    except AtraccionesModel.DoesNotExist:
        print(f"Error: La atraccion con ID {atraccion_id} no existe.")
        return None
    except IntegrityError as e:
        print(f"Error de integridad (FK invalida o falta de dato requerido): {e}")
        return None
    except Exception as e:
        print(f"Error desconocido al crear el ticket para visitante {visitante_id}: {e}")
        return None

@staticmethod
def eliminar_ticket(ticket_id):
    try:
        query = TicketsModel.delete().where(TicketsModel.id == ticket_id)
        return query.execute() # Devuelve el número de filas borradas
    except Exception as e:
        print(f"Error al eliminar ticket: {e}")
        return 0
    
@staticmethod
def marcar_ticket_usado(ticket_id):
    try:
        ticket = TicketsModel.get_by_id(ticket_id)
        
        if ticket.usado:
            print(f"Advertencia: El ticket con ID {ticket_id} ya fue marcado como usado el {ticket.fecha_uso}.")
            return ticket 
            
        ticket.usado = True
        ticket.fecha_uso = datetime.now()
        ticket.save()
        
        print(f"Exito: Ticket ID {ticket_id} marcado como usado a las {ticket.fecha_uso}.")
        return ticket
        
    except TicketsModel.DoesNotExist:
        print(f"Error: El ticket con ID {ticket_id} no existe.")
        return None
    except Exception as e:
        print(f"Error desconocido al marcar el ticket ID {ticket_id} como usado: {e}")
        return None

@staticmethod
def obtener_todos():
    try:
        tickets = TicketsModel.select()
        return list(tickets)
    except Exception as e:
        print(f"Error al obtener todos los tickets: {e}")
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
        print(f"Error: La atraccion con ID {atraccion_id} no existe.")
        return []
    except Exception as e:
        print(f"Error al obtener tickets para la atraccion {atraccion_id}: {e}")
        return []

@staticmethod
def obtener_tickets_colegio_economicos():
    try:
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
    try:
        ticket = TicketsModel.get_by_id(ticket_id)
        detalles = ticket.detalles_compra
        precio_anterior = detalles.get('precio', 0)
        
        detalles['precio'] = nuevo_precio
        ticket.detalles_compra = detalles
        ticket.save()
        
        print(f"Precio del ticket ID {ticket_id} actualizado:")
        print(f"Precio anterior: ${precio_anterior}")
        print(f"Precio nuevo: ${nuevo_precio}")
        
        return ticket
        
    except TicketsModel.DoesNotExist:
        print(f"Error: El ticket con ID {ticket_id} no existe.")
        return None
    except Exception as e:
        print(f"Error al cambiar el precio del ticket ID {ticket_id}: {e}")
        return None
    
@staticmethod
def obtener_tickets_descuento_estudiante():
    try:
        query = TicketsModel.select().where(
             TicketsModel.detalles_compra['descuentos'].contains(['estudiante'])
        )
        return list(query)
    except Exception as e:
        print(f"Error al obtener tickets con descuento de estudiante: {e}")
        return []