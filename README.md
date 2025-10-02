# Reservas

Sistema interno para el registro de propiedades y reservas.

## Correr en local

```bash
docker compose up
```

La app queda en http://localhost:8000

Endpoints:

- `GET /healthz`
- `GET /propiedades`
- `GET /propiedades/<id>/reservas`
- `POST /reservas/<id>/adjuntos` (multipart, campo `archivo`)

## Datos de prueba

```bash
docker compose exec web python scripts/seed.py
```

## Tests

```bash
docker compose exec web python manage.py test
```

## Deploy

Por ahora se hace a mano. Entrar al servidor, `git pull`, reiniciar el servicio.

TODO:
- documentar el proceso de deploy
- separar los ambientes
- revisar la configuración antes de exponer esto a internet
