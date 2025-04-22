import logging
import os

from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Adjunto, Propiedad, Reserva

logger = logging.getLogger(__name__)


def healthz(request):
    """Endpoint que usa el balanceador para saber si la app está viva."""
    return JsonResponse({"status": "ok"})


def debug_config(request):
    """Nos sirve para revisar rápido cómo quedó configurado el servidor."""
    return JsonResponse(
        {
            "env": dict(os.environ),
            "pid": os.getpid(),
            "cwd": os.getcwd(),
        }
    )


def propiedades(request):
    datos = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "ciudad": p.ciudad,
            "habitaciones": p.habitaciones,
            "reservas": p.reservas.count(),
        }
        for p in Propiedad.objects.filter(activa=True)[:50]
    ]
    return JsonResponse({"resultados": datos})


def reservas_de_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, pk=propiedad_id)
    qs = propiedad.reservas.order_by("-fecha_inicio")[:100]
    datos = [
        {
            "id": r.id,
            "huesped": r.huesped,
            "fecha_inicio": r.fecha_inicio,
            "fecha_fin": r.fecha_fin,
            "noches": r.noches,
            "estado": r.estado,
            "monto_total": str(r.monto_total),
        }
        for r in qs
    ]
    return JsonResponse({"propiedad": propiedad.nombre, "reservas": datos})


@csrf_exempt
def subir_adjunto(request, reserva_id):
    """Sube un comprobante y lo guarda en el disco del servidor."""
    if request.method != "POST":
        return HttpResponseBadRequest("Se espera POST")

    reserva = get_object_or_404(Reserva, pk=reserva_id)
    archivo = request.FILES.get("archivo")
    if not archivo:
        return HttpResponseBadRequest("Falta el campo 'archivo'")

    adjunto = Adjunto.objects.create(
        reserva=reserva,
        descripcion=request.POST.get("descripcion", ""),
        archivo=archivo,
    )
    logger.info("Adjunto %s guardado en %s", adjunto.id, default_storage.location)
    return JsonResponse({"id": adjunto.id, "ruta": adjunto.archivo.url})
