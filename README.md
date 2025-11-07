# Django_REST_Framework
Implementar funcionalidades avanzadas en Django REST Framework para mejorar la API.
# weather_api — API RESTful para temperaturas de ciudades

Este repositorio contiene una API construida con **Django + Django REST Framework** para gestionar temperaturas por ciudad. La API implementa operaciones CRUD y usa **autenticación por token** para las operaciones de escritura (POST, PUT, DELETE). Las operaciones de lectura (GET) son públicas.

---

## 1. Preparación del entorno

1. Abrir CMD y situarte en la carpeta del proyecto (la que contiene `manage.py`):

```cmd
cd "C:\ruta\a\weather_api"
```

2. Crear y activar un entorno virtual (Windows - CMD):

```cmd
python -m venv .venv
.venv\Scripts\activate
```

En PowerShell usa: `.\.venv\Scripts\Activate.ps1`.

## 3. Instalar dependencias

Instala Django y Django REST Framework:

```cmd
pip install Django djangorestframework djangorestframework-authtoken
```

## 4. Configuración mínima en `weather_api/settings.py`

Asegúrate de tener en `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... apps de Django ...
    'rest_framework',
    'rest_framework.authtoken',
    'temperatures',
]
```

Y añade (opcional, si quieres valores por defecto globales):

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}
```

## 5. Migraciones y crear la base de datos

Ejecuta:

```cmd
python manage.py makemigrations
python manage.py migrate
```

## 6. Crear usuario (jean) y token

### 6.1 Crear usuario

**Opción interactiva (superuser)**:

```cmd
python manage.py createsuperuser --username jean --email jean@gmail.com
```

Sigue el prompt para definir la contraseña.

**Opción one-liner (no interactivo)**:

```cmd
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.create_user('jean','jean@gmail.com','1234')"
```

### 6.2 Crear token para el usuario

**Opción 1 — comando (si está disponible):**

```cmd
python manage.py drf_create_token jean
```

**Opción 2 — desde shell (funciona siempre):**

```cmd
python manage.py shell -c "from django.contrib.auth import get_user_model; from rest_framework.authtoken.models import Token; User=get_user_model(); u=User.objects.get(username='jean'); t,created=Token.objects.get_or_create(user=u); print(t.key)"
```

La salida será la cadena del token, por ejemplo:

```
9f1e2a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9
```

Guarda ese valor para usarlo en las peticiones autenticadas.

## 7. Ejecutar el servidor de desarrollo

En la carpeta del proyecto (donde está `manage.py`):

```cmd
python manage.py runserver
```

Verás un mensaje similar a:

```
Starting development server at http://127.0.0.1:8000/
```

## 8. Endpoints disponibles

Suponiendo que registraste el router como `/api/` en `temperatures/urls.py`:

* `GET  /api/temperatures/` — listar todas las temperaturas (público)
* `POST /api/temperatures/` — crear (requiere autenticación)
* `GET  /api/temperatures/{id}/` — detalle (público)
* `PUT  /api/temperatures/{id}/` — actualizar (requiere autenticación)
* `PATCH /api/temperatures/{id}/` — actualización parcial (requiere autenticación)
* `DELETE /api/temperatures/{id}/` — eliminar (requiere autenticación)

## 9. Comandos `curl` — ejemplos listos y salida esperada

### 9.1 GET — Listar (público)

Comando:

```bash
curl -i -X GET http://127.0.0.1:8000/api/temperatures/
```

**Salida esperada (vacío inicialmente)**:

```
HTTP/1.1 200 OK
Content-Type: application/json

[]
```

Si ya hay datos, la respuesta será un arreglo de objetos JSON:

```json
[
  {
    "id": 1,
    "city": "Maracay",
    "temperature": "27.50",
    "last_updated": "2025-11-06T20:15:30Z"
  }
]
```

### 9.2 POST — Intento sin token (debe fallar)

Comando (sin auth header):

```bash
curl -i -X POST http://127.0.0.1:8000/api/temperatures/ \
  -H "Content-Type: application/json" \
  -d '{"city":"Maracay","temperature":"27.50"}'
```

**Salida esperada**: error de autenticación (HTTP 401 Unauthorized)

```
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{"detail":"Authentication credentials were not provided."}
```

> Si recibes `403 Forbidden`, revisa la configuración de permisos; por defecto `IsAuthenticatedOrReadOnly` devuelve 401 cuando no hay credenciales.

### 9.3 POST — Con token (éxito)

Comando:

```bash
curl -i -X POST http://127.0.0.1:8000/api/temperatures/ \
  -H "Authorization: Token coloca_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{"city":"Maracay","temperature":"27.50"}'
```

**Salida esperada**:

```
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "city": "Maracay",
  "temperature": "27.50",
  "last_updated": "2025-11-06T20:20:00Z"
}
```

### 9.4 GET detalle

Comando:

```bash
curl -i -X GET http://127.0.0.1:8000/api/temperatures/1/
```

**Salida esperada**:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "city": "Maracay",
  "temperature": "27.50",
  "last_updated": "2025-11-06T20:20:00Z"
}
```

### 9.5 PUT — Actualizar (con token)

Comando:

```bash
curl -i -X PUT http://127.0.0.1:8000/api/temperatures/1/ \
  -H "Authorization: Token coloca_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{"city":"Maracay","temperature":"28.00"}'
```

**Salida esperada**:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "city": "Maracay",
  "temperature": "28.00",
  "last_updated": "2025-11-06T20:25:00Z"
}
```

### 9.6 DELETE — Eliminar (con token)

Comando:

```bash
curl -i -X DELETE http://127.0.0.1:8000/api/temperatures/1/ \
  -H "Authorization: Token coloca_token_aqui"
```

**Salida esperada**:

```
HTTP/1.1 204 No Content
```

(El recurso fue eliminado.)
Si quieres, puedo también generar un archivo `requirements.txt` con las dependencias necesarias (basado en lo instalado por mí aquí) o exportar un `curl_examples.sh` con todos los comandos listos. ¿Quieres que cree alguno de esos archivos en el canvas?
