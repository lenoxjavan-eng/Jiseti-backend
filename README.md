# Jiseti Backend

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
