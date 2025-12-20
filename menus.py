from repositories import atracciones_repo, visitantes_repo, tickets_repo
from models import atracciones_model, visitantes_model, tickets_model
from peewee import *
from datetime import datetime

def menu():
    print(f"\n{'='*50}")
    print("1. Seccion de Visitantes")
    print("2. Seccion de Atracciones")
    print("3. Seccion de Tickets")
    print("4. Funcionalidades varias")
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
            print("Saliendo del sistema. ¡Hasta luego!")
            exit(0)
            print("Opcion invalida. Por favor, intente de nuevo.")

def menu_visitantes():
    print(f"\n{'='*50}")
    print("Sección de Visitantes")
    print("1. Crear Visitante")
    print("2. Eliminar Visitante")
    print("3. Listar todos los Visitantes")
    print("4. Eliminar restricción de un visitante")
    print("5. Agregar visita al historial de un visitante")
    print("6. Volver al Menú Principal")
    input_opcion = int(input("Seleccione una opción (1-5): "))
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
        case 4:
            print("\n--- Eliminar Restricción de Visitante ---")
            visitantes = visitantes_repo.obtener_todos()
            if not visitantes:
                print("No hay visitantes registrados.")
                return
            
            print("\nVisitantes con restricciones:")
            for v in visitantes:
                if v.preferencias and v.preferencias.get('restricciones'):
                    restricciones = v.preferencias.get('restricciones', [])
                    print(f"ID: {v.id} | Nombre: {v.nombre} | Restricciones: {restricciones}")
            
            visitante_id = int(input("\nIngrese el ID del visitante: "))
            restriccion = input("Ingrese la restricción a eliminar: ")
            
            visitantes_repo.eliminar_restriccion_visitante(visitante_id, restriccion)
        case 5:
            print("\n--- Agregar Visita al Historial ---")
            visitantes = visitantes_repo.obtener_todos()
            if not visitantes:
                print("No hay visitantes registrados.")
                return
            
            print("\nVisitantes disponibles:")
            for v in visitantes[:10]:  # Mostrar solo los primeros 10
                historial = v.preferencias.get('historial_visitas', []) if v.preferencias else []
                print(f"ID: {v.id} | Nombre: {v.nombre} | Visitas en historial: {len(historial)}")
            
            visitante_id = int(input("\nIngrese el ID del visitante: "))
            
            atracciones = atracciones_repo.obtener_todas()
            print("\nAtracciones disponibles:")
            for a in atracciones:
                print(f"  - {a.nombre}")
            
            nombre_atraccion = input("\nIngrese el nombre de la atracción visitada: ")
            
            visitantes_repo.agregar_visita_historial(visitante_id, nombre_atraccion)
        

def menu_atracciones():
    print(f"\n{'='*50}")    
    print("\n--- Sección de Atracciones ---")
    print("1. Crear Atracción")
    print("2. Cambiar Estado Activo (Activar/Desactivar)")
    print("3. Eliminar Atracción")
    print("4. Listar todas las Atracciones")
    print("5. Ver Atracciones de Alta Intensidad (>7)")
    print("6. Ver Atracciones de Larga Duración (>2min)")
    print("7. Agregar una caracteristica a una atraccion")
    print("8. Volver al Menú Principal")
    
    input_opcion = int(input("Seleccione una opción (1-7): "))
    
    match input_opcion:
        case 1:
            print("\n--- Nueva Atracción ---")
            nombre = input("Nombre de la atracción: ")
            tipo = input("Tipo (extrema, familiar, infantil, acuatica): ")
            altura_minima = int(input("Altura minima (cm): "))
            pref_detalles = input("¿Desea agregar detalles tecnicos (intensidad, duración, etc.)? (s/n): ").lower()
            detalles_json = None
            
            if pref_detalles == 's':
                intensidad = int(input("Nivel de intensidad (1-10): "))
                if intensidad < 1 or intensidad > 10:
                    print("Intensidad inválida, se establecerá en 5 por defecto.")
                    intensidad = 5
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
            nuevo_est_input = input("¿Desea activarla? (a) o desactivarla? (d): ").lower()
            if nuevo_est_input == 'a':
                nuevo_estado = True
            elif nuevo_est_input == 'd':
                nuevo_estado = False
            else:
                print(" Opción inválida. Operación cancelada.")
                return
            
            # Cambiar estado
            atracciones_repo.cambiar_estado_activo_atraccion(id_mod, nuevo_estado)
            
            if nuevo_estado==True:
                print(" La atracción ha sido activada.")
                q= input("Desea eliminar los horarios de mantenimiento programados? (s/n): ").lower()
                if q == 's':
                    atracciones_repo.eliminar_ultimo_mantenimiento(id_mod)
            # Si se desactiva, preguntar si es por mantenimiento
            if nuevo_estado == False:
                motivo = input(f"\n¿La atracción con ID {id_mod} está siendo desactivada por mantenimiento? (s/n): ").lower()
                
                if motivo == 's':
                    tiempo_mant = input("Ingrese el tramo horario estimado de mantenimiento (ej. 10:00-19:00): ")
                    
                    # Agregar horario de mantenimiento usando la nueva función
                    atracciones_repo.agregar_horario_mantenimiento(id_mod, tiempo_mant)
                    print(" La atracción ha sido desactivada y el horario de mantenimiento ha sido registrado.")
                else:
                    print(" La atracción ha sido desactivada.")

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
            print("\n--- Agregar Característica a Atracción ---")
            atracciones = atracciones_repo.obtener_todas()
            if not atracciones:
                print("No hay atracciones registradas.")
                return
            
            print("\nAtracciones disponibles:")
            for a in atracciones:
                caracteristicas = a.detalles.get('caracteristicas', []) if a.detalles else []
                print(f"ID: {a.id} | Nombre: {a.nombre} | Características actuales: {len(caracteristicas)}")
            
            atraccion_id = int(input("\nIngrese el ID de la atracción: "))
            nueva_caracteristica = input("Ingrese la nueva característica: ")
            
            atracciones_repo.agregar_caracteristica_atraccion(atraccion_id, nueva_caracteristica)
        
        case 8:
            return # Regresa al menú principal
            
        case _:
            print("Opción no válida.")

def menu_tickets():
    print(f"\n{'='*50}")
    print("Sección de Tickets")
    print("1. Crear Ticket")    
    print("2. Eliminar Ticket")
    print("3. Obtener todos")
    print("4. Obtener ticket por ID")
    print("5. Cambiar precio de un ticket")
    print("6. Volver al Menú Principal")
    input_opcion = int(input("Seleccione una opción (1-6): "))
    match input_opcion:
        case 3:
            print("\n--- Listado Completo de Tickets ---")
            tickets = tickets_repo.obtener_todos()
            for t in tickets:
                print(f"ID: {t.id}, Tipo: {t.tipo_ticket}, Detalles: {t.detalles_compra}")
        case 4:
            ticket_id = int(input("Ingrese el ID del ticket a buscar: "))
            ticket = tickets_repo.obtener_un_ticket(ticket_id)
            if ticket:
                print(f"Ticket: ID: {ticket.id}, Tipo: {ticket.tipo_ticket}, Detalles: {ticket.detalles_compra}")
            else:
                print(f"No se encontró ningún ticket con ID {ticket_id}.")
        case 5:
            print("\n--- Cambiar Precio de Ticket ---")
            tickets = tickets_repo.obtener_todos()
            if not tickets:
                print("No hay tickets registrados.")
                return
            for t in tickets:
                precio = t.detalles_compra.get('precio', 'No especificado')
                print(f"ID: {t.id}, Tipo: {t.tipo_ticket}, Precio Actual: {precio}")
            ticket_id = int(input("Ingrese el ID del ticket a modificar: "))
            ticket_seleccionado = tickets_repo.obtener_un_ticket(ticket_id)
            print(f"Ticket seleccionado: ID {ticket_seleccionado.id}, Tipo: {ticket_seleccionado.tipo_ticket}, Precio Actual: {ticket_seleccionado.detalles_compra.get('precio', 'No especificado')}")
            nuevo_precio = float(input("Ingrese el nuevo precio: "))
            tickets_repo.cambiar_precio_ticket(ticket_id, nuevo_precio)


def menu_consultas():
    print(f"\n{'='*50}")
    print("\n--- FUNCIONALIDADES VARIAS / CONSULTAS ---")
    print("1. Ver atracciones de alta intensidad (>7)")
    print("2. Ver atracciones de larga duracion (>2 min)")
    print("3. Ver solo atracciones activas actualmente")
    print("4. Ver visitantes con problemas cardiacos")
    print("5. Ver atracciones con looping y caida libre")
    print("6. Ver tickets con descuento estudiante")
    print("7. Ver atracciones con mantenimiento programado")
    print("8. Ver visitantes con preferencia extrema")
    print("9. Ver tickets de colegio economicos (<30€)")
    print("10. Ver visitantes ordenados por tickets")
    print("11. Ver visitantes con gasto mayor a X€")
    print("12. Ver top atracciones mas vendidas")
    print("13. Ver atracciones compatibles para visitante")
    print("14. Volver al menu principal")
    
    try:
        opcion = int(input("Seleccione una consulta (1-14): "))
    except ValueError:
        return

    match opcion:
        case 1:
            print("\n--- Buscando Atracciones Intensas ---")
            resultados = atracciones_repo.obtener_atracciones_intensidad_alta()
            if resultados:
                for a in resultados:
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
            print("\n--- Visitantes con Problemas Cardiacos ---")
            resultados = visitantes_repo.obtener_visitantes_problemas_cardiacos()
            if resultados:
                for v in resultados:
                    restricciones = v.preferencias.get('restricciones', []) if v.preferencias else []
                    print(f"- {v.nombre}: Restricciones {restricciones}")
            else:
                print("No hay visitantes con problemas cardiacos.")

        case 5:
            print("\n--- Atracciones con Looping y Caida Libre ---")
            resultados = atracciones_repo.obtener_atracciones_looping_caida_libre()
            if resultados:
                for a in resultados:
                    caracteristicas = a.detalles.get('caracteristicas', []) if a.detalles else []
                    print(f"- {a.nombre}: Caracteristicas {caracteristicas}")
            else:
                print("No hay atracciones con looping y caida libre.")

        case 6:
            print("\n--- Tickets con Descuento Estudiante ---")
            resultados = tickets_repo.obtener_tickets_descuento_estudiante()
            if resultados:
                print(f"Total de tickets encontrados: {len(resultados)}")
                for t in resultados[:10]:  # Mostrar solo los primeros 10
                    descuentos = t.detalles_compra.get('descuentos', []) if t.detalles_compra else []
                    precio = t.detalles_compra.get('precio', 0) if t.detalles_compra else 0
                    print(f"- Ticket ID {t.id}: {t.visitante.nombre} | Precio: ${precio} | Descuentos: {descuentos}")
                if len(resultados) > 10:
                    print(f"... y {len(resultados) - 10} tickets mas")
            else:
                print("No hay tickets con descuento estudiante.")

        case 7:
            print("\n--- Atracciones con Mantenimiento Programado ---")
            resultados = atracciones_repo.obtener_atracciones_mantenimiento_programado()
            if resultados:
                for a in resultados:
                    if a.detalles and 'horarios' in a.detalles:
                        mantenimientos = a.detalles['horarios'].get('mantenimiento', [])
                        print(f"- {a.nombre}: {len(mantenimientos)} horarios")
                        for horario in mantenimientos:
                            print(f"    * {horario}")
            else:
                print("No hay atracciones con mantenimiento programado.")

        case 8:
            print("\n--- Visitantes con Preferencia Extrema ---")
            resultados = visitantes_repo.obtener_visitantes_preferencia_extrema()
            if resultados:
                for v in resultados:
                    tipo_fav = v.preferencias.get('tipo_favorito', 'N/A') if v.preferencias else 'N/A'
                    print(f"- {v.nombre}: Tipo favorito {tipo_fav}")
            else:
                print("No hay visitantes con preferencia extrema.")

        case 9:
            print("\n--- Tickets de Colegio Economicos (<30€) ---")
            resultados = tickets_repo.obtener_tickets_colegio_economicos()
            if resultados:
                print(f"Total de tickets encontrados: {len(resultados)}")
                for t in resultados[:10]:
                    precio = t.detalles_compra.get('precio', 0) if t.detalles_compra else 0
                    print(f"- Ticket ID {t.id}: {t.visitante.nombre} | Precio: ${precio} | Tipo: {t.tipo_ticket}")
                if len(resultados) > 10:
                    print(f"... y {len(resultados) - 10} tickets mas")
            else:
                print("No hay tickets de colegio economicos.")

        case 10:
            print("\n--- Visitantes Ordenados por Cantidad de Tickets ---")
            visitantes_repo.obtener_visitantes_ordenados_por_tickets()

        case 11:
            print("\n--- Visitantes con Gasto Mayor a X€ ---")
            try:
                cantidad = float(input("Ingrese cantidad minima gastada (default 100): ") or 100)
            except ValueError:
                cantidad = 100
            visitantes_repo.obtener_visitantes_gasto_mayor_a(cantidad)

        case 12:
            print("\n--- Top Atracciones Mas Vendidas ---")
            try:
                limite = int(input("Ingrese cantidad de atracciones (default 5): ") or 5)
            except ValueError:
                limite = 5
            atracciones_repo.obtener_top_atracciones_mas_vendidas(limite)

        case 13:
            print("\n--- Atracciones Compatibles para Visitante ---")
            try:
                visitante_id = int(input("Ingrese ID del visitante: "))
                atracciones_repo.obtener_atracciones_compatibles_visitante(visitante_id)
            except ValueError:
                print("ID invalido")
            except Exception as e:
                print(f"Error: {e}")

        case 14:
            return