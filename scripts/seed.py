"""
Carga datos de prueba parecidos en volumen a los de producción.

Uso:
    python manage.py shell < scripts/seed.py

O bien:
    python scripts/seed.py

Tarda varios minutos. Genera ~40 propiedades y 1.000.000 de reservas.
"""

import datetime
import os
import random
import sys
from decimal import Decimal

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from reservas.models import Propiedad, Reserva  # noqa: E402

TOTAL_RESERVAS = 1_000_000
LOTE = 5_000

CIUDADES = [
    "Lima", "Arequipa", "Cusco", "Trujillo", "Piura",
    "Bogotá", "Medellín", "Ciudad de México", "Santiago", "Madrid",
]
NOMBRES = [
    "Ana", "Luis", "María", "Carlos", "Rosa", "Jorge", "Elena",
    "Miguel", "Sofía", "Diego", "Lucía", "Andrés", "Valeria", "Pedro",
]
APELLIDOS = [
    "Quispe", "Ramos", "Torres", "Flores", "Vargas", "Chávez",
    "Mendoza", "Castillo", "Rojas", "Delgado", "Salazar", "Núñez",
]
ESTADOS = ["pendiente", "confirmada", "cancelada"]


def crear_propiedades():
    if Propiedad.objects.exists():
        print("Ya hay propiedades cargadas, se reutilizan.")
        return list(Propiedad.objects.all())

    propiedades = [
        Propiedad(
            nombre=f"Propiedad {i:03d}",
            ciudad=random.choice(CIUDADES),
            habitaciones=random.randint(1, 6),
            activa=random.random() > 0.1,
        )
        for i in range(1, 41)
    ]
    Propiedad.objects.bulk_create(propiedades)
    print(f"{len(propiedades)} propiedades creadas.")
    return list(Propiedad.objects.all())


def crear_reservas(propiedades):
    existentes = Reserva.objects.count()
    faltan = TOTAL_RESERVAS - existentes
    if faltan <= 0:
        print(f"Ya hay {existentes} reservas, no se carga nada.")
        return

    print(f"Generando {faltan} reservas en lotes de {LOTE}...")
    base = datetime.date(2023, 1, 1)
    creadas = 0

    while creadas < faltan:
        lote = []
        for _ in range(min(LOTE, faltan - creadas)):
            inicio = base + datetime.timedelta(days=random.randint(0, 1200))
            noches = random.randint(1, 14)
            lote.append(
                Reserva(
                    propiedad=random.choice(propiedades),
                    huesped=f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}",
                    email=f"huesped{random.randint(1, 999999)}@example.com",
                    fecha_inicio=inicio,
                    fecha_fin=inicio + datetime.timedelta(days=noches),
                    monto_total=Decimal(random.randint(80, 400) * noches),
                    estado=random.choice(ESTADOS),
                )
            )
        Reserva.objects.bulk_create(lote, batch_size=LOTE)
        creadas += len(lote)
        if creadas % 50_000 == 0:
            print(f"  {creadas:,} / {faltan:,}")

    print(f"Listo: {Reserva.objects.count():,} reservas en total.")


if __name__ == "__main__":
    propiedades = crear_propiedades()
    crear_reservas(propiedades)
