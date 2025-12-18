import database
import ingesta
from repositories import atracciones_repo, visitantes_repo, tickets_repo
from models import atracciones_model, visitantes_model, tickets_model
from peewee import *
from datetime import datetime
def menu():
    print(f"\n{'='*50}")
    print("Bienvenido al sistema de gestión del parque de atracciones.")
    print("1. Seccion de Visitantes")
    print("2. Seccion de Atracciones")
    print("3. Seccion de Tickets")
    print("4. Funcionalidades varias")
    print("5. Cambiar precio ticket.")
    print("5. Salir")
    input_opcion = int(input("Seleccione una opcion (1-5): "))
    match input_opcion:
        case 1:
            menu_visitantes()
        case 2:
            menu_atracciones()
        case 3:
            menu_tickets()
        case 4:
            menu_consultas()
        case 5:
            ticket_id = int(input("Ingrese el numero del ticket: "))
            nuevo_precio = float(input("Ingrese el nuevo precio para el ticket general: "))
            exito = tickets_repo.cambiar_precio_ticket(ticket_id, nuevo_precio=nuevo_precio)
            if exito:
                print(f"Precio del ticket ID {ticket_id} actualizado a {nuevo_precio} exitosamente.")
            else:
                print(f"No se pudo actualizar el precio del ticket ID {ticket_id}.")
        case 6:
            print("Saliendo del sistema. ¡Hasta luego!")
            exit(0)
        case _:
            print("Opcion invalida. Por favor, intente de nuevo.")

def menu_visitantes():
    print("Sección de Visitantes")
    print("1. Crear Visitante")
    print("2. Eliminar Visitante")
    print("3. Listar todos los Visitantes")
    print("4. Volver al Menú Principal")
    input_opcion = int(input("Seleccione una opción (1-4): "))
    match input_opcion:
        case 1:
            nombre = input("Ingrese el nombre del visitante: ")
            email = input("Ingrese el email del visitante: ")
            altura = int(input("Ingrese la altura del visitante en cm: "))
            pref_input = input("Quiere ingresar preferencias? (s/n): ")
            preferencias_json = None
            
            if pref_input == 's':
                print("\n--- Configurando Preferencias ---")
                
                # 1. Tipo favorito
                print("\nTipos de atracciones disponibles:")
                print("  - extrema")
                print("  - familiar")
                print("  - infantil")
                print("  - acuatica")
                tipo_favorito = input("Ingrese el tipo de atracción favorito: ").strip()
                
                # 2. Restricciones
                print("\n¿El visitante tiene restricciones? (altura, mareos, claustrofobia, agua, etc.)")
                restricciones_input = input("Ingrese las restricciones separadas por comas (o presione Enter si no tiene): ").strip()
                
                if restricciones_input:
                    restricciones = [r.strip() for r in restricciones_input.split(',') if r.strip()]
                else:
                    restricciones = []
                
                # 3. Historial de visitas (normalmente vacío para un visitante nuevo)
                print("\n¿Desea agregar visitas previas al historial? (s/n): ")
                agregar_historial = input().strip().lower()
                
                historial_visitas = []
                if agregar_historial == 's':
                    print("Ingrese las visitas previas (nombre de atracción), una por línea.")
                    print("Escriba 'fin' cuando termine:")
                    while True:
                        visita = input("  Visita: ").strip()
                        if visita.lower() == 'fin' or visita == '':
                            break
                        if visita:
                            historial_visitas.append(visita)
                
                # Construir el JSON de preferencias
                preferencias_json = {
                    "tipo_favorito": tipo_favorito,
                    "restricciones": restricciones,
                    "historial_visitas": historial_visitas
                }
                
                print("\n--- Preferencias configuradas ---")
                print(f"Tipo favorito: {tipo_favorito}")
                print(f"Restricciones: {restricciones if restricciones else 'Ninguna'}")
                print(f"Historial: {len(historial_visitas)} visita(s) previa(s)")
            
            elif pref_input == 'n':
                print("\nNo se ingresarán preferencias.")
                preferencias_json = None
            else:
                print("\nOpción inválida. No se ingresarán preferencias.")
                preferencias_json = None
            
            # Crear el visitante
            visitante_creado = visitantes_repo.crear_visitante(nombre, email, altura, preferencias_json)
            visitantes_repo.crear_visitante(nombre, email, altura, preferencias_json)
            print(f"Visitante creado con nombre: {nombre}, email: {email}, altura: {altura}, preferencias: {preferencias_json}")
        case 2:
            visitantes = visitantes_repo.obtener_todos()
            for v in visitantes:
                print(f"ID: {v.id}, Nombre: {v.nombre}, Email: {v.email}, Altura: {v.altura}, Preferencias: {v.preferencias}")
            visitante_id = int(input("Ingrese el ID del visitante a eliminar: "))
            exito = visitantes_repo.eliminar_visitante(visitante_id)
            if exito:
                print(f"Visitante con ID {visitante_id} eliminado exitosamente.")
            else:
                print(f"No se pudo eliminar el visitante con ID {visitante_id}.")

            if exito:
                print(f"Visitante con ID {visitante_id} eliminado exitosamente.")
        case 3:
            visitantes = visitantes_repo.obtener_todos()
            for v in visitantes:
                print(f"ID: {v.id}, Nombre: {v.nombre}, Email: {v.email}, Altura: {v.altura}, Preferencias: {v.preferencias}")
                

def menu_atracciones():
    print("\n--- Sección de Atracciones ---")
    print("1. Crear Atracción")
    print("2. Cambiar Estado Activo (Activar/Desactivar)")
    print("3. Eliminar Atracción")
    print("4. Listar todas las Atracciones")
    print("5. Ver Atracciones de Alta Intensidad (>7)")
    print("6. Ver Atracciones de Larga Duración (>2min)")
    print("7. Volver al Menú Principal")
    
    input_opcion = int(input("Seleccione una opción (1-7): "))
    
    match input_opcion:
        case 1:
            print("\n--- Nueva Atracción ---")
            nombre = input("Nombre de la atracción: ")
            tipo = input("Tipo (extrema, familiar, infantil, acuatica): ")
            altura_minima = int(input("Altura minima (cm): "))
            
            # Configuración de detalles opcionales (JSONB)
            pref_detalles = input("¿Desea agregar detalles tecnicos (intensidad, duración, etc.)? (s/n): ").lower()
            detalles_json = None
            
            if pref_detalles == 's':
                intensidad = int(input("Nivel de intensidad (1-10): "))
                duracion = int(input("Duracion en segundos: "))
                capacidad = int(input("Capacidad de personas: "))
                detalles_json = {
                    "intensidad": intensidad,
                    "duracion_segundos": duracion,
                    "capacidad": capacidad
                }

            nueva_atrac = atracciones_repo.crear_atraccion(nombre, tipo, altura_minima, detalles_json)
            if nueva_atrac:
                print(f"Atracción '{nombre}' creada exitosamente.")

        case 2:
            # Primero listamos para que el usuario vea los IDs y estados actuales
            atracciones = atracciones_repo.obtener_todas()
            for a in atracciones:
                estado = "ACTIVA" if a.activa else "INACTIVA"
                print(f"ID: {a.id} | {a.nombre} | Estado: {estado}")
            
            id_mod = int(input("\nIngrese el ID de la atracción a modificar: "))
            nuevo_est_input = input("¿Desea activarla? (s) o desactivarla? (n): ").lower()
            nuevo_estado = True if nuevo_est_input == 's' else False
            
            atracciones_repo.cambiar_estado_activo_atraccion(id_mod, nuevo_estado)

        case 3:
            atracciones = atracciones_repo.obtener_todas()
            for a in atracciones:
                print(f"ID: {a.id} | {a.nombre}")
            
            id_del = int(input("\nIngrese el ID de la atracción a eliminar: "))
            confirmar = input(f"¿Está seguro de eliminar la atracción {id_del}? (s/n): ").lower()
            if confirmar == 's':
                atracciones_repo.eliminar_atraccion(id_del)

        case 4:
            print("\n--- Listado Completo ---")
            atracciones = atracciones_repo.obtener_todas()
            for a in atracciones:
                print(f"ID: {a.id} | {a.nombre} | Tipo: {a.tipo} | Altura Min: {a.altura_minima} | Activa: {a.activa}")
                if a.detalles:
                    print(f"   Detalles: {a.detalles}")

        case 5:
            print("\n--- Atracciones de Alta Intensidad ---")
            intensas = atracciones_repo.obtener_atracciones_intensidad_alta()
            if intensas:
                for a in intensas:
                    print(f"- {a.nombre} (Intensidad: {a.detalles.get('intensidad')})")
            else:
                print("No se encontraron atracciones con intensidad > 7.")

        case 6:
            print("\n--- Atracciones de Larga Duración ---")
            largas = atracciones_repo.obtener_atracciones_larga_duracion()
            if largas:
                for a in largas:
                    print(f"- {a.nombre} (Duración: {a.detalles.get('duracion_segundos')} seg)")
            else:
                print("No se encontraron atracciones con duración > 120 segundos.")

        case 7:
            return # Regresa al menú principal
            
        case _:
            print("Opción no válida.")

def menu_tickets():
    print("Sección de Tickets")
    print("1. Crear Ticket")
    print("2. Volver al Menú Principal")
    input_opcion = input("Seleccione una opción (1-2): ")

def menu_consultas():
    print("\n--- FUNCIONALIDADES VARIAS / CONSULTAS ---")
    print("1. Ver atracciones de alta intensidad (>7)")
    print("2. Ver atracciones de larga duracion (>2 min)")
    print("3. Ver solo atracciones activas actualmente")
    print("4. Volver al menu principal")
    
    try:
        opcion = int(input("Seleccione una consulta (1-4): "))
    except ValueError:
        return

    match opcion:
        case 1:
            print("\n--- Buscando Atracciones Intensas ---")
            resultados = atracciones_repo.obtener_atracciones_intensidad_alta()
            if resultados:
                for a in resultados:
                    # Usamos .get() porque 'detalles' es un diccionario JSON
                    print(f"- {a.nombre}: Intensidad {a.detalles.get('intensidad')}")
            else:
                print("No hay atracciones que cumplan el criterio.")
        
        case 2:
            print("\n--- Buscando Atracciones Largas ---")
            resultados = atracciones_repo.obtener_atracciones_larga_duracion()
            if resultados:
                for a in resultados:
                    print(f"- {a.nombre}: Duracion {a.detalles.get('duracion_segundos')} seg.")
            else:
                print("No hay atracciones de larga duracion.")

        case 3:
            print("\n--- Atracciones Disponibles (Activas) ---")
            resultados = atracciones_repo.obtener_atracciones_disponibles()
            for a in resultados:
                print(f"- {a.nombre} (Tipo: {a.tipo})")

        case 4:
            return

def main():

    print("Base de datos inicializada.")
    init_db = database.inicializar_base([visitantes_model.VisitantesModel, tickets_model.TicketsModel, atracciones_model.AtraccionesModel], reiniciar=True)
    ingesta.ingesta_completa(tickets_por_visitante=4)



    while True:
        menu()


if __name__ == "__main__":
    main()