from django.urls import path

from . import views

urlpatterns = [
    path("healthz", views.healthz, name="healthz"),
    path("propiedades", views.propiedades, name="propiedades"),
    path(
        "propiedades/<int:propiedad_id>/reservas",
        views.reservas_de_propiedad,
        name="reservas-propiedad",
    ),
    path(
        "reservas/<int:reserva_id>/adjuntos",
        views.subir_adjunto,
        name="subir-adjunto",
    ),
]
