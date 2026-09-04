# Jiseti Backend

## Deploying to Render

This repository includes a `render.yaml` Blueprint. In Render, select **New +**
then **Blueprint**, connect this GitHub repository, and apply the Blueprint.
It creates a web service and PostgreSQL database and sets the service's
`DATABASE_URL` and `SECRET_KEY` automatically.

Before deploying, set these optional service environment variables in Render:

- `CORS_ALLOWED_ORIGINS`: the exact URL of the deployed frontend, such as
  `https://your-frontend.netlify.app`.
- `CSRF_TRUSTED_ORIGINS`: any domain from which the Django admin will submit
  forms, such as `https://your-service.onrender.com`.

After the first deploy, open the service's **Shell** in Render and run
`python manage.py createsuperuser`. The health check is available at
`/health/`.

Use the superuser email and password at `/admin/login` in the frontend to open
the administrator dashboard and update report statuses.

> Media uploads require persistent external storage (such as Cloudinary or
> Amazon S3) for production. Render's normal web-service filesystem is erased
> when the service is rebuilt or restarted, so uploaded files must not be
> relied on until external storage is configured.

## Authentication

Use `POST /api/auth/register/`, `POST /api/auth/login/`, and
`GET /api/auth/profile/`. Authenticated requests use the JWT access token as
`Authorization: Bearer <token>`.

## Admin status management

Authenticated staff users can change a record status with:

```http
PATCH /api/admin/records/<id>/status/
Content-Type: application/json
Authorization: Bearer <access-token>
```

```json
{
	"status": "resolved"
}
```

Valid statuses are `pending`, `under-investigation`, `rejected`, and `resolved`.
Non-staff users receive `403 Forbidden`, unknown statuses receive `400 Bad Request`,
and an unknown record receives `404 Not Found`.
