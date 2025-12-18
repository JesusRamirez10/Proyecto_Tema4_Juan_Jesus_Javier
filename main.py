import database
import ingesta
from repositories import atracciones_repo, visitantes_repo, tickets_repo
from models import atracciones_model, visitantes_model, tickets_model
from peewee import *
from datetime import datetime
def menu():
    print("Bienvenido al sistema de gestión del parque de atracciones.")
    print("1. Seccion de Visitantes")
    print("2. Seccion de Atracciones")
    print("3. Seccion de Tickets")
    print("4. Salir")
    input_opcion = int(input("Seleccione una opción (1-4): "))
    match input_opcion:
        case 1:
            menu_visitantes()
        case 2:
            menu_atracciones()
        case 3:
            menu_tickets()
        case 4:
            print("Saliendo del sistema. ¡Hasta luego!")
            exit(0)
        case _:
            print("Opción inválida. Por favor, intente de nuevo.")

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
    print("Sección de Atracciones")
    print("1. Crear Atracción")
    print("2. Cambiar Estado Activo de Atracción")
    print("3. Volver al Menú Principal")
    input_opcion = input("Seleccione una opción (1-3): ")

def menu_tickets():
    print("Sección de Tickets")
    print("1. Crear Ticket")
    print("2. Volver al Menú Principal")
    input_opcion = input("Seleccione una opción (1-2): ")

def main():

    print("Base de datos inicializada.")
    init_db = database.inicializar_base([visitantes_model.VisitantesModel, tickets_model.TicketsModel, atracciones_model.AtraccionesModel], reiniciar=True)
    ingesta.ingesta_completa(tickets_por_visitante=3)



    while True:
        menu()


if __name__ == "__main__":
    main()