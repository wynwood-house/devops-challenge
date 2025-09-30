from django.db import models


class Propiedad(models.Model):
    nombre = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default="Perú")
    habitaciones = models.PositiveSmallIntegerField(default=1)
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "propiedades"

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"


class Reserva(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
    ]

    propiedad = models.ForeignKey(
        Propiedad, on_delete=models.CASCADE, related_name="reservas"
    )
    huesped = models.CharField(max_length=200)
    email = models.EmailField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["propiedad", "fecha_inicio"],
                name="idx_reserva_prop_inicio",
            ),
            models.Index(fields=["estado"], name="idx_reserva_estado"),
        ]

    def __str__(self):
        return f"{self.huesped} — {self.propiedad_id} ({self.fecha_inicio})"

    @property
    def noches(self):
        return (self.fecha_fin - self.fecha_inicio).days


class Adjunto(models.Model):
    """Comprobantes y documentos que suben los administradores de propiedad."""

    reserva = models.ForeignKey(
        Reserva, on_delete=models.CASCADE, related_name="adjuntos"
    )
    descripcion = models.CharField(max_length=200, blank=True)
    archivo = models.FileField(upload_to="adjuntos/")
    subido_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.archivo.name
