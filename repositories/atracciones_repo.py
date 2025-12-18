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