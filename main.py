import database
from repositories import atracciones_repo, visitantes_repo, tickets_repo
from models import atracciones_model, visitantes_model, tickets_model
from peewee import *
from datetime import datetime



def main():

    init_db = database.inicializar_base([visitantes_model.VisitantesModel, tickets_model.TicketsModel, atracciones_model.AtraccionesModel], reiniciar=True)
    visitante = visitantes_repo.crear_visitante('Juan Perez', 'juan.perez@example.com', 180) #nombre, email, altura, preferencias_json=None
    atraccion = atracciones_repo.crear_atraccion('Montaña Rusa', 'extrema', 140)  #nombre, tipo, altura_minima, detalles_json=None
    ticket = tickets_repo.crear_ticket(visitante.id, datetime.now().date(), 'general', {}, atraccion.id)  #visitante_id, fecha_visita, tipo_ticket, detalles_compra_json, atraccion_id


    print("Base de datos inicializada.")

if __name__ == "__main__":
    main()