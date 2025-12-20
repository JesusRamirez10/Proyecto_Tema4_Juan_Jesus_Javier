import database
import ingesta
from models import atracciones_model, visitantes_model, tickets_model
from menus import menu


def main():

    print("Base de datos inicializada.")
    init_db = database.inicializar_base([visitantes_model.VisitantesModel, tickets_model.TicketsModel, atracciones_model.AtraccionesModel], reiniciar=True)
    ingesta.ingesta_completa(tickets_por_visitante=4)


    print("Bienvenido al sistema de gestión del parque de atracciones.")
    while True:
        menu()


if __name__ == "__main__":
    main()