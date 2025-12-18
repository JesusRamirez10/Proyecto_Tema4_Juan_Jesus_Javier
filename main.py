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
            if pref_input.lower() == 's':
                preferencias = input("Ingrese las preferencias en formato JSON: ")
                preferencias_json = json.loads(preferencias) if preferencias else None
            elif pref_input.lower() == 'n':
                preferencias = None
            else:
                print("Opción inválida. No se ingresarán preferencias.")
                preferencias = None
                visitantes_repo.crear_visitante(nombre, email, altura, preferencias_json)
        case 2:

            visitante_id = int(input("Ingrese el ID del visitante a eliminar: "))
            exito = visitantes_repo.eliminar_visitante(visitante_id)

            visitante = visitantes_repo.crear_visitante(nombre, email, altura, preferencias_json)
            if visitante:
                print(f"Visitante creado con ID: {visitante.id}")
            else:
                print("Error al crear el visitante.")
                

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

    init_db = database.inicializar_base([visitantes_model.VisitantesModel, tickets_model.TicketsModel, atracciones_model.AtraccionesModel], reiniciar=True)
    ingesta.IngestaDatos.ingesta_completa(tickets_por_visitante=3)


    print("Base de datos inicializada.")
    while True:
        menu()


if __name__ == "__main__":
    main()