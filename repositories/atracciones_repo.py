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
        
@staticmethod
def cambiar_estado_activo_atraccion(atraccion_id, nuevo_estado: bool):
        try:
            # 1. Buscar la instancia de la atracción por ID
            atraccion = AtraccionesModel.get_by_id(atraccion_id)
            
            # 2. Verificar si el estado es el mismo para evitar una operación de guardado innecesaria
            if atraccion.activa == nuevo_estado:
                estado_str = "activo" if nuevo_estado else "inactivo"
                print(f"Advertencia: La atracción '{atraccion.nombre}' (ID {atraccion_id}) ya estaba en estado {estado_str}.")
                return atraccion
            
            # 3. Actualizar el campo 'activa'
            atraccion.activa = nuevo_estado
            
            # 4. Guardar los cambios en la base de datos
            atraccion.save()
            
            estado_str = "activado" if nuevo_estado else "desactivado"
            print(f"Éxito: La atracción '{atraccion.nombre}' (ID {atraccion_id}) ha sido {estado_str}.")
            return atraccion
            
        except AtraccionesModel.DoesNotExist:
            # Captura si el ID de la atracción no existe
            print(f"Error: La atracción con ID {atraccion_id} no existe.")
            return None
        except Exception as e:
            # Captura cualquier otro error durante la actualización
            print(f"Error desconocido al cambiar el estado de la atracción ID {atraccion_id}: {e}")
            return None
        
@staticmethod
def eliminar_atraccion(atraccion_id):
        try:
            # 1. Intentar obtener el nombre antes de eliminar para un mensaje más claro
            try:
                atraccion = AtraccionesModel.get_by_id(atraccion_id)
                nombre_atraccion = atraccion.nombre
            except AtraccionesModel.DoesNotExist:
                print(f"Advertencia: La atracción con ID {atraccion_id} no existe.")
                return False

            # 2. Eliminar el registro
            # Usamos delete_instance() de la instancia de Peewee
            filas_eliminadas = atraccion.delete_instance() 
            
            if filas_eliminadas > 0:
                print(f"Éxito: La atracción '{nombre_atraccion}' (ID {atraccion_id}) fue eliminada.")
                print(f"Nota: Los tickets que referenciaban esta atracción fueron actualizados para tener atraccion=NULL.")
                return True
            else:
                # Esto solo debería ocurrir si el registro fue eliminado por otra transacción justo antes
                print(f"Advertencia: No se pudo eliminar la atracción con ID {atraccion_id}.")
                return False
                
        except Exception as e:
            print(f"Error desconocido al eliminar la atracción ID {atraccion_id}: {e}")
            return False

@staticmethod
def obtener_todas():
    try:
        atracciones = AtraccionesModel.select()
        return list(atracciones)
    except Exception as e:
        print(f"Error al obtener todas las atracciones: {e}")
        return []

@staticmethod
def obtener_atracciones_disponibles():
    try:
        query = AtraccionesModel.select().where(AtraccionesModel.activa == True)
        return list(query)
    except Exception as e:
        print(f"Error al obtener atracciones disponibles: {e}")
        return []

@staticmethod
def obtener_atracciones_intensidad_alta():
    try:
        # Accedemos a la clave 'intensidad' dentro del JSONB detalles
        query = AtraccionesModel.select().where(
            AtraccionesModel.detalles['intensidad'].cast('int') > 7
        )
        return list(query)
    except Exception as e:
        print(f"Error al obtener atracciones de alta intensidad: {e}")
        return []
    
@staticmethod
def obtener_atracciones_larga_duracion():
    try:
        # Accedemos a la clave 'duracion_segundos' dentro del JSONB detalles
        query = AtraccionesModel.select().where(
            AtraccionesModel.detalles['duracion_segundos'].cast('int') > 120
        )
        return list(query)
    except Exception as e:
        print(f"Error al obtener atracciones de larga duración: {e}")
        return []
    

@staticmethod
def agregar_caracteristica_atraccion(atraccion_id, nueva_caracteristica):
    """
    Añade una nueva característica al array de características de una atracción
    """
    try:
        # 1. Obtener la atracción
        atraccion = AtraccionesModel.get_by_id(atraccion_id)
        
        # 2. Verificar que tenga detalles, si no, crearlos
        if not atraccion.detalles:
            atraccion.detalles = {
                'duracion_segundos': 0,
                'capacidad_por_turno': 0,
                'intensidad': 0,
                'caracteristicas': [],
                'horarios': {
                    'apertura': '',
                    'cierre': '',
                    'mantenimiento': []
                }
            }
        
        # 3. Obtener los detalles actuales
        detalles = atraccion.detalles
        
        # 4. Obtener el array de características
        caracteristicas = detalles.get('caracteristicas', [])
        
        # 5. Verificar si la característica ya existe (evitar duplicados)
        if nueva_caracteristica in caracteristicas:
            print(f"⚠️ La característica '{nueva_caracteristica}' ya existe en la atracción '{atraccion.nombre}'.")
            return atraccion
        
        # 6. Añadir la nueva característica
        caracteristicas.append(nueva_caracteristica)
        
        # 7. Actualizar los detalles
        detalles['caracteristicas'] = caracteristicas
        atraccion.detalles = detalles
        
        # 8. Guardar los cambios
        atraccion.save()
        
        print(f"✅ Característica agregada a la atracción '{atraccion.nombre}' (ID {atraccion_id}).")
        print(f"   Nueva característica: {nueva_caracteristica}")
        print(f"   Total características: {len(caracteristicas)}")
        
        return atraccion
        
    except AtraccionesModel.DoesNotExist:
        print(f"❌ Error: La atracción con ID {atraccion_id} no existe.")
        return None
    except Exception as e:
        print(f"❌ Error al agregar característica a la atracción ID {atraccion_id}: {e}")
        return None
    
@staticmethod
def cambiar_estado_activo_atraccion(atraccion_id, nuevo_estado):
    """
    Cambia el estado activo de una atracción
    """
    try:
        # 1. Buscar la instancia de la atracción por ID
        atraccion = AtraccionesModel.get_by_id(atraccion_id)
        
        # 2. Verificar si el estado es el mismo para evitar una operación innecesaria
        if atraccion.activa == nuevo_estado:
            estado_str = "activo" if nuevo_estado else "inactivo"
            print(f"⚠️ Advertencia: La atracción '{atraccion.nombre}' (ID {atraccion_id}) ya estaba en estado {estado_str}.")
            return atraccion
        
        # 3. Actualizar el campo 'activa'
        atraccion.activa = nuevo_estado
        
        # 4. Guardar los cambios en la base de datos
        atraccion.save()
        
        estado_str = "activada" if nuevo_estado else "desactivada"
        print(f"✅ Éxito: La atracción '{atraccion.nombre}' (ID {atraccion_id}) ha sido {estado_str}.")
        return atraccion
        
    except AtraccionesModel.DoesNotExist:
        print(f"❌ Error: La atracción con ID {atraccion_id} no existe.")
        return None
    except Exception as e:
        print(f"❌ Error desconocido al cambiar el estado de la atracción ID {atraccion_id}: {e}")
        return None


# ============================================
# ATRACCIONES_REPO.PY - NUEVA FUNCIÓN PARA MANTENIMIENTO
# ============================================

@staticmethod
def agregar_horario_mantenimiento(atraccion_id, horario_mantenimiento):
    """
    Agrega un horario al array de mantenimiento en detalles de una atracción
    
    Args:
        atraccion_id: ID de la atracción
        horario_mantenimiento: String con el horario (ej: "10:00-19:00")
    """
    try:
        # 1. Obtener la atracción
        atraccion = AtraccionesModel.get_by_id(atraccion_id)
        
        # 2. Asegurarse de que exista la estructura de detalles
        if not atraccion.detalles:
            atraccion.detalles = {
                'duracion_segundos': 0,
                'capacidad_por_turno': 0,
                'intensidad': 0,
                'caracteristicas': [],
                'horarios': {
                    'apertura': '',
                    'cierre': '',
                    'mantenimiento': []
                }
            }
        
        # 3. Obtener los detalles actuales
        detalles = atraccion.detalles
        
        # 4. Asegurarse de que existe la estructura de horarios
        if 'horarios' not in detalles:
            detalles['horarios'] = {
                'apertura': '',
                'cierre': '',
                'mantenimiento': []
            }
        
        # 5. Asegurarse de que existe el array de mantenimiento
        if 'mantenimiento' not in detalles['horarios']:
            detalles['horarios']['mantenimiento'] = []
        
        # 6. Hacer append del nuevo horario de mantenimiento
        detalles['horarios']['mantenimiento'].append(horario_mantenimiento)
        
        # 7. Actualizar el campo JSONB
        atraccion.detalles = detalles
        
        # 8. Guardar los cambios
        atraccion.save()
        
        print(f"✅ Horario de mantenimiento '{horario_mantenimiento}' agregado a '{atraccion.nombre}' (ID {atraccion_id}).")
        print(f"   Total horarios de mantenimiento: {len(detalles['horarios']['mantenimiento'])}")
        
        return atraccion
        
    except AtraccionesModel.DoesNotExist:
        print(f"❌ Error: La atracción con ID {atraccion_id} no existe.")
        return None
    except Exception as e:
        print(f"❌ Error al agregar horario de mantenimiento a la atracción ID {atraccion_id}: {e}")
        return None
    
def eliminar_ultimo_mantenimiento(atraccion_id):

    try:
        # 1. Obtener la atracción
        atraccion = AtraccionesModel.get_by_id(atraccion_id)
        
        # 2. Verificar que existan detalles y estructura de horarios
        if not atraccion.detalles or 'horarios' not in atraccion.detalles:
            print(f"⚠️ La atracción '{atraccion.nombre}' no tiene horarios configurados.")
            return None
        
        # 3. Obtener los detalles actuales
        detalles = atraccion.detalles
        
        # 4. Verificar que exista el array de mantenimiento
        if 'mantenimiento' not in detalles['horarios']:
            print(f"⚠️ La atracción '{atraccion.nombre}' no tiene mantenimientos programados.")
            return None
        
        # 5. Obtener el array de mantenimiento
        mantenimientos = detalles['horarios']['mantenimiento']
        
        # 6. Verificar que haya al menos un elemento
        if len(mantenimientos) == 0:
            print(f"⚠️ La atracción '{atraccion.nombre}' no tiene mantenimientos para eliminar.")
            return None
        
        # 7. Hacer pop del último elemento
        horario_eliminado = mantenimientos.pop()
        
        # 8. Actualizar el campo JSONB
        detalles['horarios']['mantenimiento'] = mantenimientos
        atraccion.detalles = detalles
        
        # 9. Guardar los cambios
        atraccion.save()
        
        print(f"✅ Horario de mantenimiento '{horario_eliminado}' eliminado de '{atraccion.nombre}' (ID {atraccion_id}).")
        print(f"   Mantenimientos restantes: {len(mantenimientos)}")
        
        return horario_eliminado
        
    except AtraccionesModel.DoesNotExist:
        print(f"❌ Error: La atracción con ID {atraccion_id} no existe.")
        return None
    except Exception as e:
        print(f"❌ Error al eliminar horario de mantenimiento de la atracción ID {atraccion_id}: {e}")
        return None
    
@staticmethod
def obtener_top_atracciones_mas_vendidas(limite=5):
    """
    Obtiene las N atracciones más vendidas (con más tickets específicos)
    
    Args:
        limite: Número de atracciones a retornar (default: 5)
    """
    try:   
        # Consulta con JOIN, GROUP BY y ORDER BY limitado
        query = (AtraccionesModel
                .select(
                    AtraccionesModel,
                    fn.COUNT(TicketsModel.id).alias('tickets_vendidos')
                )
                .join(TicketsModel, JOIN.LEFT_OUTER)
                .where(TicketsModel.atraccion.is_null(False))  # Solo tickets con atracción específica
                .group_by(AtraccionesModel)
                .order_by(fn.COUNT(TicketsModel.id).desc())
                .limit(limite))
        
        resultados = []
        print("\n" + "="*60)
        print(f"TOP {limite} ATRACCIONES MÁS VENDIDAS")
        print("="*60)
        
        for i, atraccion in enumerate(query, 1):
            tickets = atraccion.tickets_vendidos
            resultados.append({
                'atraccion': atraccion,
                'tickets_vendidos': tickets
            })
            print(f"{i}. {atraccion.nombre} | Tipo: {atraccion.tipo} | Tickets vendidos: {tickets}")
        
        print("="*60)
        return resultados
        
    except Exception as e:
        print(f"❌ Error al obtener top atracciones: {e}")
        return []    
    
@staticmethod
def obtener_atracciones_compatibles_visitante(visitante_id):
    """
    Obtiene atracciones compatibles para un visitante específico
    Criterios:
    - Atracciones activas
    - El visitante cumple con la altura mínima
    - El tipo coincide con el tipo_favorito del visitante (si tiene preferencias)
    
    Args:
        visitante_id: ID del visitante
    """
    try:
        # 1. Obtener el visitante
        visitante = VisitantesModel.get_by_id(visitante_id)
        
        # 2. Obtener su tipo favorito si tiene preferencias
        tipo_favorito = None
        if visitante.preferencias:
            tipo_favorito = visitante.preferencias.get('tipo_favorito', None)
        
        # 3. Construir la consulta base: activas y altura compatible
        query = (AtraccionesModel
                .select()
                .where(
                    (AtraccionesModel.activa == True) &
                    (AtraccionesModel.altura_minima <= visitante.altura)
                ))
        
        # 4. Si tiene tipo favorito, filtrar por tipo
        if tipo_favorito and tipo_favorito != '':
            query = query.where(AtraccionesModel.tipo == tipo_favorito)
        
        resultados = list(query)
        
        print("\n" + "="*60)
        print(f"ATRACCIONES COMPATIBLES PARA {visitante.nombre}")
        print("="*60)
        print(f"Altura del visitante: {visitante.altura} cm")
        if tipo_favorito:
            print(f"Tipo favorito: {tipo_favorito}")
        print("-"*60)
        
        if resultados:
            for i, atraccion in enumerate(resultados, 1):
                print(f"{i}. {atraccion.nombre}")
                print(f"   Tipo: {atraccion.tipo}")
                print(f"   Altura mínima: {atraccion.altura_minima} cm")
                if atraccion.detalles:
                    intensidad = atraccion.detalles.get('intensidad', 'N/A')
                    duracion = atraccion.detalles.get('duracion_segundos', 'N/A')
                    print(f"   Intensidad: {intensidad} | Duración: {duracion}s")
                print("-"*60)
        else:
            print("No hay atracciones compatibles para este visitante.")
        
        print("="*60)
        return resultados
        
    except VisitantesModel.DoesNotExist:
        print(f"❌ Error: El visitante con ID {visitante_id} no existe.")
        return []
    except Exception as e:
        print(f"❌ Error al obtener atracciones compatibles: {e}")
        return []

@staticmethod
def obtener_atracciones_looping_caida_libre():
    try:
        # Accedemos al array de características dentro del JSONB detalles
        # Usamos el operador @> de PostgreSQL para verificar que contenga ambos elementos
        query = AtraccionesModel.select().where(
            AtraccionesModel.detalles['caracteristicas'].contains(['looping', 'caída libre'])
        )
        return list(query)
    except Exception as e:
        # Devolvemos una lista vacía en caso de error
        print(f"Error al obtener atracciones con looping y caída libre: {e}")
        return []

@staticmethod
def obtener_atracciones_mantenimiento_programado():
    try:
        # Obtener todas las atracciones
        atracciones = AtraccionesModel.select()
        
        # Filtrar las que tienen al menos un mantenimiento
        atracciones_mantenimiento = []
        for atraccion in atracciones:
            if atraccion.detalles and 'horarios' in atraccion.detalles:
                mantenimientos = atraccion.detalles['horarios'].get('mantenimiento', [])
                if len(mantenimientos) > 0:
                    atracciones_mantenimiento.append(atraccion)
        
        return atracciones_mantenimiento
    except Exception as e:
        # Devolvemos una lista vacía en caso de error
        print(f"Error al obtener atracciones con mantenimiento programado: {e}")
        return []