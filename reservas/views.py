from django.http import JsonResponse


def healthz(request):
    """Endpoint que usa el balanceador para saber si la app está viva."""
    return JsonResponse({"status": "ok"})
