import datetime
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Propiedad, Reserva


class PropiedadTests(TestCase):
    def setUp(self):
        self.propiedad = Propiedad.objects.create(
            nombre="Casa Barranco", ciudad="Lima", habitaciones=3
        )

    def test_listado_incluye_propiedades_activas(self):
        respuesta = self.client.get(reverse("propiedades"))
        self.assertEqual(respuesta.status_code, 200)
        nombres = [p["nombre"] for p in respuesta.json()["resultados"]]
        self.assertIn("Casa Barranco", nombres)

    def test_propiedad_inactiva_no_aparece(self):
        Propiedad.objects.create(nombre="Depa Miraflores", ciudad="Lima", activa=False)
        respuesta = self.client.get(reverse("propiedades"))
        nombres = [p["nombre"] for p in respuesta.json()["resultados"]]
        self.assertNotIn("Depa Miraflores", nombres)


class ReservaTests(TestCase):
    def setUp(self):
        self.propiedad = Propiedad.objects.create(
            nombre="Casa Barranco", ciudad="Lima", habitaciones=3
        )

    def _crear_reserva(self, **kwargs):
        datos = {
            "propiedad": self.propiedad,
            "huesped": "Ana Quispe",
            "email": "ana@example.com",
            "fecha_inicio": datetime.date(2026, 3, 1),
            "fecha_fin": datetime.date(2026, 3, 4),
            "monto_total": Decimal("450.00"),
        }
        datos.update(kwargs)
        return Reserva.objects.create(**datos)

    def test_calculo_de_noches(self):
        reserva = self._crear_reserva()
        self.assertEqual(reserva.noches, 3)

    def test_estado_por_defecto_es_pendiente(self):
        reserva = self._crear_reserva()
        self.assertEqual(reserva.estado, "pendiente")

    def test_listado_por_propiedad(self):
        self._crear_reserva()
        url = reverse("reservas-propiedad", args=[self.propiedad.id])
        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()["reservas"]), 1)


class ReporteDiarioTests(TestCase):
    """
    El reporte de cierre de día lista las reservas cargadas en la jornada.
    Lo corre un cron en el servidor, por eso comparamos contra la hora del servidor.
    """

    def setUp(self):
        self.propiedad = Propiedad.objects.create(
            nombre="Casa Barranco", ciudad="Lima", habitaciones=3
        )

    def test_reserva_creada_hoy_aparece_en_el_reporte(self):
        reserva = Reserva.objects.create(
            propiedad=self.propiedad,
            huesped="Luis Ramos",
            email="luis@example.com",
            fecha_inicio=datetime.date(2026, 5, 10),
            fecha_fin=datetime.date(2026, 5, 12),
            monto_total=Decimal("300.00"),
        )

        hoy = datetime.datetime.utcnow().date()
        del_dia = Reserva.objects.filter(creada_en__date=hoy)

        self.assertIn(reserva, del_dia)


class HealthTests(TestCase):
    def test_healthz_responde_ok(self):
        respuesta = self.client.get(reverse("healthz"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["status"], "ok")
