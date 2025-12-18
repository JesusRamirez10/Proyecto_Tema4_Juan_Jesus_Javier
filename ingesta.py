import random
from datetime import datetime, timedelta
from repositories import atracciones_repo, visitantes_repo, tickets_repo

# Datos completos de visitantes
VISITANTES = [
    {'nombre': 'Juan Pérez', 'email': 'juan.perez@example.com', 'altura': 175,
     'preferencias': {'tipo_favorito': 'extrema', 'restricciones': [], 'historial_visitas': []}},
    
    {'nombre': 'María García', 'email': 'maria.garcia@example.com', 'altura': 162,
     'preferencias': {'tipo_favorito': 'familiar', 'restricciones': ['altura'], 'historial_visitas': []}},
    
    {'nombre': 'Carlos López', 'email': 'carlos.lopez@example.com', 'altura': 180,
     'preferencias': {'tipo_favorito': 'extrema', 'restricciones': [], 'historial_visitas': []}},
    
    {'nombre': 'Ana Martínez', 'email': 'ana.martinez@example.com', 'altura': 155,
     'preferencias': {'tipo_favorito': 'acuatica', 'restricciones': ['mareos'], 'historial_visitas': []}},
    
    {'nombre': 'Pedro Sánchez', 'email': 'pedro.sanchez@example.com', 'altura': 168,
     'preferencias': {'tipo_favorito': 'familiar', 'restricciones': [], 'historial_visitas': []}},
    
    {'nombre': 'Laura Fernández', 'email': 'laura.fernandez@example.com', 'altura': 158,
     'preferencias': {'tipo_favorito': 'acuatica', 'restricciones': ['claustrofobia'], 'historial_visitas': []}},
    
    {'nombre': 'Diego Rodríguez', 'email': 'diego.rodriguez@example.com', 'altura': 185,
     'preferencias': {'tipo_favorito': 'extrema', 'restricciones': [], 'historial_visitas': []}},
    
    {'nombre': 'Carmen Gómez', 'email': 'carmen.gomez@example.com', 'altura': 160,
     'preferencias': {'tipo_favorito': 'familiar', 'restricciones': ['agua'], 'historial_visitas': []}},
    
    {'nombre': 'Javier Torres', 'email': 'javier.torres@example.com', 'altura': 172,
     'preferencias': {'tipo_favorito': 'extrema', 'restricciones': [], 'historial_visitas': []}},
    
    {'nombre': 'Isabel Ruiz', 'email': 'isabel.ruiz@example.com', 'altura': 165,
     'preferencias': {'tipo_favorito': 'acuatica', 'restricciones': ['mareos'], 'historial_visitas': []}},
    
    {'nombre': 'Miguel Díaz', 'email': 'miguel.diaz@example.com', 'altura': 178,
     'preferencias': {'tipo_favorito': 'extrema', 'restricciones': [], 'historial_visitas': []}},
    
    {'nombre': 'Elena Moreno', 'email': 'elena.moreno@example.com', 'altura': 152,
     'preferencias': {'tipo_favorito': 'infantil', 'restricciones': ['altura', 'mareos'], 'historial_visitas': []}},
    
    {'nombre': 'Pablo Muñoz', 'email': 'pablo.munoz@example.com', 'altura': 182,
     'preferencias': {'tipo_favorito': 'extrema', 'restricciones': [], 'historial_visitas': []}},
    
    {'nombre': 'Sara Álvarez', 'email': 'sara.alvarez@example.com', 'altura': 167,
     'preferencias': {'tipo_favorito': 'familiar', 'restricciones': [], 'historial_visitas': []}},
    
    {'nombre': 'Antonio Romero', 'email': 'antonio.romero@example.com', 'altura': 176,
     'preferencias': {'tipo_favorito': 'acuatica', 'restricciones': [], 'historial_visitas': []}},
]

ATRACCIONES = [
    {'nombre': 'Montaña Rusa Infernal', 'tipo': 'extrema', 'altura_minima': 140, 
     'detalles': {'duracion_segundos': 180, 'capacidad_por_turno': 24, 'intensidad': 9}},
    
    {'nombre': 'Caída Libre', 'tipo': 'extrema', 'altura_minima': 130,
     'detalles': {'duracion_segundos': 60, 'capacidad_por_turno': 16, 'intensidad': 10}},
    
    {'nombre': 'Río Salvaje', 'tipo': 'acuatica', 'altura_minima': 120,
     'detalles': {'duracion_segundos': 300, 'capacidad_por_turno': 20, 'intensidad': 5}},
    
    {'nombre': 'Splash Mountain', 'tipo': 'acuatica', 'altura_minima': 110,
     'detalles': {'duracion_segundos': 420, 'capacidad_por_turno': 30, 'intensidad': 6}},
    
    {'nombre': 'Carrusel Mágico', 'tipo': 'infantil', 'altura_minima': 0,
     'detalles': {'duracion_segundos': 240, 'capacidad_por_turno': 40, 'intensidad': 1}},
    
    {'nombre': 'Tazas Giratorias', 'tipo': 'infantil', 'altura_minima': 90,
     'detalles': {'duracion_segundos': 180, 'capacidad_por_turno': 32, 'intensidad': 2}},
    
    {'nombre': 'Tren Fantasma', 'tipo': 'familiar', 'altura_minima': 100,
     'detalles': {'duracion_segundos': 360, 'capacidad_por_turno': 16, 'intensidad': 3}},
    
    {'nombre': 'Noria Gigante', 'tipo': 'familiar', 'altura_minima': 0,
     'detalles': {'duracion_segundos': 480, 'capacidad_por_turno': 48, 'intensidad': 2}},
    
    {'nombre': 'Péndulo del Terror', 'tipo': 'extrema', 'altura_minima': 135,
     'detalles': {'duracion_segundos': 150, 'capacidad_por_turno': 20, 'intensidad': 8}},
    
    {'nombre': 'Coches de Choque', 'tipo': 'familiar', 'altura_minima': 110,
     'detalles': {'duracion_segundos': 300, 'capacidad_por_turno': 24, 'intensidad': 4}},
    
    {'nombre': 'Casa Encantada', 'tipo': 'familiar', 'altura_minima': 100,
     'detalles': {'duracion_segundos': 420, 'capacidad_por_turno': 12, 'intensidad': 3}},
    
    {'nombre': 'Tobogán Acuático', 'tipo': 'acuatica', 'altura_minima': 125,
     'detalles': {'duracion_segundos': 90, 'capacidad_por_turno': 8, 'intensidad': 7}}
]

# Configuraciones de tickets por tipo
TICKETS_CONFIG = {
    'general': {
        'precio': 45.00,
        'descuentos': [],
        'extras': ['fast_pass', 'foto']
    },
    'colegio': {
        'precio': 25.00,
        'descuentos': ['descuento_grupo'],
        'extras': ['almuerzo']
    },
    'empleado': {
        'precio': 15.00,
        'descuentos': ['descuento_empleado'],
        'extras': []
    }
}


def crear_visitantes():
    """Crea todos los visitantes predefinidos"""
    print(f"\n{'='*50}")
    print(f"Creando {len(VISITANTES)} visitantes...")
    print(f"{'='*50}")
    
    visitantes = []
    
    for i, v_data in enumerate(VISITANTES):
        visitante = visitantes_repo.crear_visitante(
            v_data['nombre'],
            v_data['email'],
            v_data['altura'],
            v_data['preferencias']
        )
        
        if visitante:
            visitantes.append(visitante)
            print(f"✅ Visitante {i+1}: {v_data['nombre']} (altura: {v_data['altura']}cm)")
        else:
            print(f"❌ Error creando visitante: {v_data['nombre']}")
    
    print(f"\n✅ Total visitantes creados: {len(visitantes)}")
    return visitantes


def crear_atracciones():
    """Crea todas las atracciones predefinidas"""
    print(f"\n{'='*50}")
    print(f"Creando {len(ATRACCIONES)} atracciones...")
    print(f"{'='*50}")
    
    atracciones = []
    
    for i, a_data in enumerate(ATRACCIONES):
        atraccion = atracciones_repo.crear_atraccion(
            a_data['nombre'],
            a_data['tipo'],
            a_data['altura_minima'],
            a_data.get('detalles')
        )
        
        if atraccion:
            atracciones.append(atraccion)
            print(f"✅ Atracción {i+1}: {a_data['nombre']} ({a_data['tipo']})")
        else:
            print(f"❌ Error creando atracción: {a_data['nombre']}")
    
    print(f"\n✅ Total atracciones creadas: {len(atracciones)}")
    return atracciones


def crear_tickets(visitantes, atracciones, tickets_por_visitante=2):
    """Crea tickets para los visitantes"""
    print(f"\n{'='*50}")
    print(f"Creando tickets (aprox. {tickets_por_visitante} por visitante)...")
    print(f"{'='*50}")
    
    tickets = []
    ticket_count = 0
    tipos_ticket = list(TICKETS_CONFIG.keys())
    
    for visitante in visitantes:
        num_tickets = random.randint(1, tickets_por_visitante)
        
        for _ in range(num_tickets):
            atraccion = random.choice(atracciones)
            
            # Verificar altura mínima
            if visitante.altura < atraccion.altura_minima:
                continue
            
            # Seleccionar tipo de ticket y sus datos
            tipo_ticket = random.choice(tipos_ticket)
            config = TICKETS_CONFIG[tipo_ticket]
            
            # Generar fecha de visita (próximos 30 días)
            dias_adelante = random.randint(0, 30)
            fecha_visita = (datetime.now() + timedelta(days=dias_adelante)).date()
            
            # Construir detalles de compra
            detalles_compra = {
                'precio': config['precio'],
                'descuentos_aplicados': config['descuentos'],
                'servicios_extra': config['extras'],
                'metodo_pago': random.choice(['efectivo', 'tarjeta', 'app'])
            }
            
            ticket = tickets_repo.crear_ticket(
                visitante.id,
                fecha_visita,
                tipo_ticket,
                detalles_compra,
                atraccion.id
            )
            
            if ticket:
                tickets.append(ticket)
                ticket_count += 1
                print(f"✅ Ticket {ticket_count}: {visitante.nombre} → {atraccion.nombre} ({fecha_visita})")
            else:
                print(f"❌ Error creando ticket para {visitante.nombre}")
    
    print(f"\n✅ Total tickets creados: {len(tickets)}")
    return tickets


def ingesta_completa(tickets_por_visitante=2):
    """Ejecuta la ingesta completa de datos"""
    print("\n" + "="*50)
    print("🎢 INICIANDO INGESTA DE DATOS DEL PARQUE DE ATRACCIONES 🎢")
    print("="*50)
    
    # Crear visitantes
    visitantes = crear_visitantes()
    
    # Crear atracciones
    atracciones = crear_atracciones()
    
    # Crear tickets
    tickets = crear_tickets(visitantes, atracciones, tickets_por_visitante)
    
    # Resumen final
    print(f"\n{'='*50}")
    print("📊 RESUMEN DE LA INGESTA")
    print(f"{'='*50}")
    print(f"👥 Visitantes creados: {len(visitantes)}")
    print(f"🎢 Atracciones creadas: {len(atracciones)}")
    print(f"🎟️  Tickets creados: {len(tickets)}")
    print(f"{'='*50}\n")
    
    return {
        'visitantes': visitantes,
        'atracciones': atracciones,
        'tickets': tickets
    }


if __name__ == "__main__":
    resultados = ingesta_completa(tickets_por_visitante=3)