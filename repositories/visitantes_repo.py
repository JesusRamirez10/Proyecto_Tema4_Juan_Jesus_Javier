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

@staticmethod
def eliminar_restriccion_visitante(visitante_id, restriccion):
    """
    Elimina una restricción específica del array de restricciones de un visitante
    """
    try:
        # 1. Obtener el visitante
        visitante = VisitantesModel.get_by_id(visitante_id)
        
        # 2. Verificar que tenga preferencias
        if not visitante.preferencias:
            print(f"⚠️ El visitante ID {visitante_id} no tiene preferencias configuradas.")
            return None
        
        # 3. Obtener las preferencias actuales
        preferencias = visitante.preferencias
        
        # 4. Obtener el array de restricciones
        restricciones = preferencias.get('restricciones', [])
        
        # 5. Verificar si la restricción existe
        if restriccion not in restricciones:
            print(f"⚠️ La restricción '{restriccion}' no existe en el visitante ID {visitante_id}.")
            print(f"   Restricciones actuales: {restricciones}")
            return visitante
        
        # 6. Eliminar la restricción del array
        restricciones.remove(restriccion)
        
        # 7. Actualizar las preferencias
        preferencias['restricciones'] = restricciones
        visitante.preferencias = preferencias
        
        # 8. Guardar los cambios
        visitante.save()
        
        print(f"✅ Restricción '{restriccion}' eliminada del visitante '{visitante.nombre}' (ID {visitante_id}).")
        print(f"   Restricciones restantes: {restricciones if restricciones else 'Ninguna'}")
        
        return visitante
        
    except VisitantesModel.DoesNotExist:
        print(f"❌ Error: El visitante con ID {visitante_id} no existe.")
        return None
    except Exception as e:
        print(f"❌ Error al eliminar restricción del visitante ID {visitante_id}: {e}")
        return None


@staticmethod
def agregar_visita_historial(visitante_id, nombre_atraccion):
    """
    Añade una nueva visita al historial de visitas de un visitante
    """
    try:
        # 1. Obtener el visitante
        visitante = VisitantesModel.get_by_id(visitante_id)
        
        # 2. Verificar que tenga preferencias, si no, crearlas
        if not visitante.preferencias:
            visitante.preferencias = {
                'tipo_favorito': '',
                'restricciones': [],
                'historial_visitas': []
            }
        
        # 3. Obtener las preferencias actuales
        preferencias = visitante.preferencias
        
        # 4. Obtener el array de historial
        historial = preferencias.get('historial_visitas', [])
        
        # 5. Añadir la nueva visita con timestamp
        nueva_visita = {
            'atraccion': nombre_atraccion,
            'fecha': datetime.now().isoformat()
        }
        historial.append(nueva_visita)
        
        # 6. Actualizar las preferencias
        preferencias['historial_visitas'] = historial
        visitante.preferencias = preferencias
        
        # 7. Guardar los cambios
        visitante.save()
        
        print(f"✅ Visita agregada al historial del visitante '{visitante.nombre}' (ID {visitante_id}).")
        print(f"   Atracción visitada: {nombre_atraccion}")
        print(f"   Total visitas en historial: {len(historial)}")
        
        return visitante
        
    except VisitantesModel.DoesNotExist:
        print(f"❌ Error: El visitante con ID {visitante_id} no existe.")
        return None
    except Exception as e:
        print(f"❌ Error al agregar visita al historial del visitante ID {visitante_id}: {e}")
        return None
    

@staticmethod
def obtener_visitantes_ordenados_por_tickets():
    """
    Lista visitantes ordenados por cantidad total de tickets comprados (descendente)
    Usa JOIN con la tabla tickets y cuenta cuántos tickets tiene cada visitante
    """
    try:
        
        
        # Consulta con JOIN, GROUP BY y ORDER BY
        query = (VisitantesModel
                .select(
                    VisitantesModel,
                    fn.COUNT(TicketsModel.id).alias('total_tickets')
                )
                .join(TicketsModel, JOIN.LEFT_OUTER)  # LEFT JOIN para incluir visitantes sin tickets
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
        print(f"❌ Error al obtener visitantes ordenados por tickets: {e}")
        return []


@staticmethod
def obtener_visitantes_gasto_mayor_a(cantidad_minima=100):
    """
    Obtiene visitantes que hayan gastado más de X€ en tickets
    Suma los precios en detalles_compra->precio de todos sus tickets
    
    Args:
        cantidad_minima: Cantidad mínima gastada (default: 100€)
    """
    try:
        
        # Consulta que suma los precios del JSONB
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
        print(f"VISITANTES QUE GASTARON MÁS DE {cantidad_minima}€")
        print("="*60)
        
        for i, visitante in enumerate(query, 1):
            gasto = float(visitante.gasto_total) if visitante.gasto_total else 0
            resultados.append({
                'visitante': visitante,
                'gasto_total': gasto
            })
            print(f"{i}. {visitante.nombre} | Gasto total: {gasto:.2f}€")
        
        print("="*60)
        return resultados
        
    except Exception as e:
        print(f"❌ Error al obtener visitantes por gasto: {e}")
        return []
    
@staticmethod
def obtener_visitantes_problemas_cardiacos():
    try:
        # Accedemos al array de restrcciones dentro del JSONB preferencias
        query = (VisitantesModel.select().where(
            VisitantesModel.preferencias['restricciones'].contains(['problemas_cardiacos'])
        ))
        return list(query)
    except Exception as e:
        # Devolvemos una lista vacía en caso de error
        print(f"Error al obtener visitantes con problemas cardiacos: {e}")
        return []
