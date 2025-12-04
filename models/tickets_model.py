from datetime import datetime
from peewee import *
from playhouse import postgres_ext
from models.basemodel import BaseModel
from models.atracciones_model import AtraccionesModel
from models.visitantes_model import VisitantesModel

#tipos permitidos de tickets
tipos_ticket = (('general', 'General'),('colegio', 'Colegio'),('empleado', 'Empleado'),)

class TicketsModel(BaseModel):
    # id (Primary Key, autoincrement)
    id = AutoField(primary_key=True)
    
    # foreign_key_field a la tabla Visitantes. CASCADE asegura que si el visitante se elimina, el ticket también.
    visitante = ForeignKeyField(VisitantesModel, backref='tickets', on_delete='CASCADE')
    
    # ForeignKeyField a Atracciones. null=True permite tickets que valen para cualquier atracción.
    atraccion = ForeignKeyField(AtraccionesModel, backref='tickets_vendidos', null=True, on_delete='SET NULL')
    
    # Por defecto, se usa el momento de la creación del registro.
    fecha_compra = DateTimeField(default=datetime.now)
    
    # fecha_visita (date)
    fecha_visita = DateField(null=False)
    
    # tipo_ticket (string): puede ser “general”, “colegio”, “empleado”
    tipo_ticket = CharField(eleccion=tipos_ticket, null=False)
    
    # detalles_compra (jsonb)
    detalles_compra = postgres_ext.BinaryJSONField(null=False, default={
        "precio": 0.00,
        "descuentos_aplicados": [],
        "servicios_extra": [],
        "metodo_pago": "" 
    })
    
    # usado (boolean, default = False)
    usado = BooleanField(default=False)
    
    # fecha_uso (datetime, NULL)
    fecha_uso = DateTimeField(null=True)