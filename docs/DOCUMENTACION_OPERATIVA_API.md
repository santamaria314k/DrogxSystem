# Documentacion Operativa API DrogxSystem




====================================
FLUJO DE PRUEBAS DE LA APP       
====================================

Abre Swagger en el navegador
http://localhost:8000/docs

Verifica que la API está viva
Ejecuta GET /
Resultado esperado: 200 con {"status":"ok","docs":"/docs"}

Prueba que sin token hay protección
Ejecuta GET /api/v1/productos sin autorizar
Resultado esperado: 401

Haz login (admin)
En POST /api/v1/auth/login:

username: admin
password: hash_admin_123
Ejecuta y copia access_token
Autoriza Swagger
Pulsa Authorize (arriba derecha) y pega:
Bearer TU_TOKEN
Luego Authorize y Close

Prueba lectura con token
Ejecuta:

GET /api/v1/productos
GET /api/v1/inventario
GET /api/v1/ventas
Resultado esperado: 200
Prueba acción de admin (debe permitir)
Ejecuta POST /api/v1/productos con un body válido
Resultado esperado: 200 (o 201 según cliente)

Prueba permisos por rol vendedor
Haz login con usuario vendedor (mgarcia / hash_mgarcia_789), vuelve a Authorize con ese token y prueba:

POST /api/v1/productos → esperado 403
POST /api/v1/ventas → esperado 200
Prueba permisos por rol farmacéutico (si tienes usuario)
Con token farmacéutico:
POST /api/v1/productos → esperado permitido
POST /api/v1/ventas → esperado 403
Valida catálogo y usuarios
Con admin prueba:
GET /api/v1/roles, POST /api/v1/roles
GET /api/v1/usuarios, POST /api/v1/usuarios
Con no-admin, esas rutas de usuarios deben devolver 403
Cierra prueba
Pulsa Authorize y Logout para limpiar token en Swagger.




## 1) Objetivo
Esta guia documenta como operar, consumir y validar la API para que otros equipos (frontend/vistas) trabajen sin bloquearse.

Cubre:
- Como levantar el proyecto en WSL con Docker Compose.
- Como autenticarse con JWT.
- Que permisos tiene cada rol.
- Como ejecutar pruebas rapidas y diagnosticar errores comunes.

## 2) Arquitectura Operativa
- Backend: FastAPI
- ORM: SQLAlchemy
- Base de datos: MySQL 8
- Orquestacion: Docker Compose
- Prefix de API: `/api/v1`
- Swagger: `http://localhost:8000/docs`

## 3) Arranque del sistema (WSL)
Desde la raiz del proyecto:

```bash
docker-compose up --build -d
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Validaciones minimas:

```bash
curl -sS http://localhost:8000/ && echo
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/docs
```

Esperado:
- `GET /` -> `{"status":"ok","docs":"/docs"}`
- `/docs` -> `200`

## 4) Datos y esquema de base de datos
- El esquema y datos semilla se inicializan desde: `mysql/init/01_init.sql`
- En el arranque, MySQL ejecuta automaticamente `/docker-entrypoint-initdb.d/01_init.sql`

Tablas principales:
- `USUARIO`, `ROL`
- `PRODUCTO`, `INVENTARIO`, `VENTA`
- `UNIDADMEDIDA`, `VIAADMINISTRACION`, `VIGENCIA`, `LABORATORIO`

## 5) Autenticacion JWT
### Endpoint de login
- `POST /api/v1/auth/login`
- Content-Type: `application/x-www-form-urlencoded`
- Body: `username=<usuario>&password=<clave>`

Respuesta:
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "user": {
    "idusuario": 1,
    "username": "admin",
    "rol": 1
  }
}
```

Uso en llamadas protegidas:
- Header: `Authorization: Bearer <access_token>`

## 6) Roles y permisos
IDs de rol:
- `1` = Admin
- `2` = Farmaceutico
- `3` = Vendedor

### Matriz operativa de permisos
| Recurso | Metodo | Ruta | Admin | Farmaceutico | Vendedor |
|---|---|---|---|---|---|
| Auth | POST | `/api/v1/auth/login` | Si | Si | Si |
| Productos | GET | `/api/v1/productos` | Si | Si | Si |
| Productos | GET | `/api/v1/productos/{id}` | Si | Si | Si |
| Productos | POST | `/api/v1/productos` | Si | Si | No |
| Productos | PUT | `/api/v1/productos/{id}` | Si | Si | No |
| Productos | DELETE | `/api/v1/productos/{id}` | Si | Si | No |
| Inventario | GET | `/api/v1/inventario` | Si | Si | Si |
| Inventario | GET | `/api/v1/inventario/producto/{id_producto}` | Si | Si | Si |
| Inventario | POST | `/api/v1/inventario` | Si | Si | No |
| Inventario | DELETE | `/api/v1/inventario/{id}` | Si | Si | No |
| Ventas | GET | `/api/v1/ventas` | Si | Si | Si |
| Ventas | GET | `/api/v1/ventas/{id}` | Si | Si | Si |
| Ventas | POST | `/api/v1/ventas` | Si | No | Si |
| Ventas | DELETE | `/api/v1/ventas/{id}` | Si | No | Si |
| Roles | GET | `/api/v1/roles` | Si | Si | Si |
| Roles | POST | `/api/v1/roles` | Si | No | No |
| Roles | DELETE | `/api/v1/roles/{idrol}` | Si | No | No |
| Usuarios | GET | `/api/v1/usuarios` | Si | No | No |
| Usuarios | GET | `/api/v1/usuarios/{id}` | Si | No | No |
| Usuarios | POST | `/api/v1/usuarios` | Si | No | No |
| Usuarios | DELETE | `/api/v1/usuarios/{id}` | Si | No | No |
| Catalogos | GET | `/api/v1/unidades|vias|vigencias|laboratorios` | Si | Si | Si |
| Catalogos | POST | `/api/v1/unidades|vias|vigencias|laboratorios` | Si | No | No |
| Catalogos | DELETE | `/api/v1/laboratorios/{id}` | Si | No | No |

Notas:
- Toda ruta de negocio requiere token.
- Sin token: `401`.
- Token valido con rol no permitido: `403`.

## 7) Flujo recomendado para frontend
1. Login en `/api/v1/auth/login`.
2. Guardar `access_token` en almacenamiento seguro del cliente.
3. Enviar `Authorization: Bearer <token>` en cada request.
4. Si respuesta `401`, forzar re-login.
5. Si respuesta `403`, ocultar/inhabilitar accion segun rol.

## 8) Coleccion minima de pruebas (manual)
### 8.1 Sin token
```bash
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/api/v1/productos
```
Esperado: `401`

### 8.2 Login admin
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin&password=hash_admin_123'
```

### 8.3 Admin consulta productos
```bash
curl -X GET http://localhost:8000/api/v1/productos \
  -H 'Authorization: Bearer <TOKEN_ADMIN>'
```
Esperado: `200`

### 8.4 Vendedor intenta crear producto
Esperado: `403`

### 8.5 Vendedor crea venta
Esperado: `200` (o `201` segun cliente)

## 9) Operacion diaria
Comandos utiles:
```bash
# Ver logs API
docker logs -f gestion_api

# Ver logs DB
docker logs -f gestion_db

# Reinicio limpio total
docker-compose down -v
docker-compose up --build -d
```

## 10) Errores frecuentes y solucion
### Error: `401 Unauthorized`
- Falta token o token invalido.
- Verificar header `Authorization`.

### Error: `403 Forbidden`
- El usuario autenticado no tiene rol permitido para ese endpoint.
- Revisar matriz de permisos.

### Error en arranque por DB no lista
- La API tiene reintentos de conexion al iniciar.
- Si persiste, revisar `docker logs -f gestion_db`.

### Error en entorno local de VS Code: imports no resueltos
- Suele ser interprete Python local no configurado.
- No implica fallo dentro del contenedor Docker.

## 11) Criterio de aceptacion operativa
Se considera operativa cuando:
- `gestion_db` esta `healthy`.
- `gestion_api` esta `Up`.
- `GET /` responde `status: ok`.
- Login JWT funciona.
- Las reglas de rol cumplen (401/403/200 segun matriz).

