from django.contrib import admin

from .models import Adjunto, Propiedad, Reserva

admin.site.register(Propiedad)
admin.site.register(Reserva)
admin.site.register(Adjunto)
