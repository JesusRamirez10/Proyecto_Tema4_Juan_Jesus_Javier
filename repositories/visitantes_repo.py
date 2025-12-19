import json
from peewee import *
from datetime import datetime
from playhouse.postgres_ext import *
from models.atracciones_model import AtraccionesModel
from models.visitantes_model import VisitantesModel
from models.tickets_model import TicketsModel

@staticmethod
def crear_visitante(nombre, email, altura, preferencias_json=None):
    try:
        datos_visitante = {
            'nombre': nombre,
            'email': email,
            'altura': altura
        }
        
        if preferencias_json is not None:
            datos_visitante['preferencias'] = preferencias_json
        
        return VisitantesModel.create(**datos_visitante)
        
    except Exception as e:
        print(f"Error insertando al visitante {nombre}: {e}")
        return None
    
@staticmethod
def eliminar_visitante(visitante_id):
    try:
        try:
            visitante = VisitantesModel.get_by_id(visitante_id)
            nombre_visitante = visitante.nombre
        except VisitantesModel.DoesNotExist:
            print(f"Advertencia: El visitante con ID {visitante_id} no existe.")
            return False

        filas_eliminadas = visitante.delete_instance(recursive=True)
        
        if filas_eliminadas > 0:
            print(f"Exito: El visitante '{nombre_visitante}' (ID {visitante_id}) fue eliminado.")
            return True
        else:
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
def obtener_visitantes_con_ticket_para_atraccion(atraccion_id):
    try:
        query = (VisitantesModel
        .select()
        .join(TicketsModel)
        .where(TicketsModel.atraccion == atraccion_id))
        return list(query)
    except Exception as e:
        print(f"Error al obtener visitantes con ticket para la atraccion {atraccion_id}: {e}")
        return []
        
@staticmethod
def obtener_visitantes_preferencia_extrema():
    try:
        query = VisitantesModel.select().where(
            VisitantesModel.preferencias['tipo_favorito'] == 'extrema'
        )
        return list(query)
    except Exception as e:
        print(f"Error al obtener visitantes con preferencia extrema: {e}")
        return []

@staticmethod
def eliminar_restriccion_visitante(visitante_id, restriccion):
    try:
        visitante = VisitantesModel.get_by_id(visitante_id)
        
        if not visitante.preferencias:
            print(f"El visitante ID {visitante_id} no tiene preferencias configuradas.")
            return None
        
        preferencias = visitante.preferencias
        restricciones = preferencias.get('restricciones', [])
        
        if restriccion not in restricciones:
            print(f"La restriccion '{restriccion}' no existe en el visitante ID {visitante_id}.")
            print(f"Restricciones actuales: {restricciones}")
            return visitante
        
        restricciones.remove(restriccion)
        preferencias['restricciones'] = restricciones
        visitante.preferencias = preferencias
        visitante.save()
        
        print(f"Restriccion '{restriccion}' eliminada del visitante '{visitante.nombre}' (ID {visitante_id}).")
        print(f"Restricciones restantes: {restricciones if restricciones else 'Ninguna'}")
        
        return visitante
        
    except VisitantesModel.DoesNotExist:
        print(f"Error: El visitante con ID {visitante_id} no existe.")
        return None
    except Exception as e:
        print(f"Error al eliminar restriccion del visitante ID {visitante_id}: {e}")
        return None

@staticmethod
def agregar_visita_historial(visitante_id, nombre_atraccion):
    try:
        visitante = VisitantesModel.get_by_id(visitante_id)
        
        if not visitante.preferencias:
            visitante.preferencias = {
                'tipo_favorito': '',
                'restricciones': [],
                'historial_visitas': []
            }
        
        preferencias = visitante.preferencias
        historial = preferencias.get('historial_visitas', [])
        
        nueva_visita = {
            'atraccion': nombre_atraccion,
            'fecha': datetime.now().isoformat()
        }
        historial.append(nueva_visita)
        
        preferencias['historial_visitas'] = historial
        visitante.preferencias = preferencias
        visitante.save()
        
        print(f"Visita agregada al historial del visitante '{visitante.nombre}' (ID {visitante_id}).")
        print(f"Atraccion visitada: {nombre_atraccion}")
        print(f"Total visitas en historial: {len(historial)}")
        
        return visitante
        
    except VisitantesModel.DoesNotExist:
        print(f"Error: El visitante con ID {visitante_id} no existe.")
        return None
    except Exception as e:
        print(f"Error al agregar visita al historial del visitante ID {visitante_id}: {e}")
        return None

@staticmethod
def obtener_visitantes_ordenados_por_tickets():
    try:
        query = (VisitantesModel
                .select(
                    VisitantesModel,
                    fn.COUNT(TicketsModel.id).alias('total_tickets')
                )
                .join(TicketsModel, JOIN.LEFT_OUTER)
                .group_by(VisitantesModel)
                .order_by(fn.COUNT(TicketsModel.id).desc()))
        
        resultados = []
        print("\n" + "="*50)
        print("VISITANTES ORDENADOS POR CANTIDAD DE TICKETS")
        print("="*50)
        
        for i, visitante in enumerate(query, 1):
            total = visitante.total_tickets
            resultados.append({
                'visitante': visitante,
                'total_tickets': total
            })
            print(f"{i}. {visitante.nombre} | Email: {visitante.email} | Tickets: {total}")
        
        print("="*50)
        return resultados
        
    except Exception as e:
        print(f"Error al obtener visitantes ordenados por tickets: {e}")
        return []

@staticmethod
def obtener_visitantes_gasto_mayor_a(cantidad_minima=100):
    try:
        query = (VisitantesModel
                .select(
                    VisitantesModel,
                    fn.SUM(TicketsModel.detalles_compra['precio'].cast('float')).alias('gasto_total')
                )
                .join(TicketsModel, JOIN.LEFT_OUTER)
                .group_by(VisitantesModel)
                .having(fn.SUM(TicketsModel.detalles_compra['precio'].cast('float')) > cantidad_minima)
                .order_by(fn.SUM(TicketsModel.detalles_compra['precio'].cast('float')).desc()))
        
        resultados = []
        print("\n" + "="*60)
        print(f"VISITANTES QUE GASTARON MAS DE {cantidad_minima} EUROS")
        print("="*60)
        
        for i, visitante in enumerate(query, 1):
            gasto = float(visitante.gasto_total) if visitante.gasto_total else 0
            resultados.append({
                'visitante': visitante,
                'gasto_total': gasto
            })
            print(f"{i}. {visitante.nombre} | Gasto total: {gasto:.2f} euros")
        
        print("="*60)
        return resultados
        
    except Exception as e:
        print(f"Error al obtener visitantes por gasto: {e}")
        return []
    
@staticmethod
def obtener_visitantes_problemas_cardiacos():
    try:
        query = (VisitantesModel.select().where(
            VisitantesModel.preferencias['restricciones'].contains(['problemas_cardiacos'])
        ))
        return list(query)
    except Exception as e:
        print(f"Error al obtener visitantes con problemas cardiacos: {e}")
        return []