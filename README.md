# Sistema de Gestión de Productos
## Stack: FastAPI + MySQL + Docker (WSL)

Guia operativa para equipos de frontend/vistas:
- docs/OPERATIVA_API.md

levanta:
docker compose up -d
detiene:
docker stop 
ver
docker ps -q

--------------------------------------------------------------
(Apaga todo)
docker-compose down 

(Borra basura de intentos fallidos)
docker system prune -f 

(Construye todo desde cero).
docker-compose up --build -d 

(Mira el resultado).                                                            
docker logs -f gestion_api 
----------------------------------------------------------------




---

## Estructura del proyecto

```
proyecto/
├── docker-compose.yml
├── .gitignore
├── mysql/
│   └── init/
│       └── 01_init.sql         
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    ├── .env.example
    └── app/
        ├── main.py
        ├── config.py
        ├── database/connection.py
        ├── models/models.py
        ├── schemas/schemas.py
        └── routers/routes.py
```

---

## Requisitos en WSL

```bash
# Instalar Docker Engine en WSL (Ubuntu)
sudo apt update && sudo apt install -y docker.io docker-compose
sudo service docker start

# Verificar
docker --version
docker-compose --version
```

---

## Levantar el proyecto

```bash
# 1. Entrar a la carpeta del proyecto
cd proyecto/

# 2. Construir imágenes y levantar contenedores en segundo plano
docker-compose up --build

docker-compose up --build -d

# 3. Ver logs en tiempo real
docker-compose logs -f

# 4. Ver solo los logs de la API
docker-compose logs -f api

# 5. Ver solo los logs de MySQL
docker-compose logs -f db
```

---

## URLs disponibles
-----------------------------------------------------------------
| Recurso            | URL                                      |
|--------------------|------------------------------------------|
| API raíz / health  | http://localhost:8000/                   |
| Swagger UI (docs)  | http://localhost:8000/docs               |
| ReDoc              | http://localhost:8000/redoc              |
| MySQL              | localhost:3306 (usuario: gestion_user)   |
----------------------------------------------------------------
---

## Endpoints principales

### Productos
-------------------------------------------------------------
| Método | Ruta                        | Acción              |
|--------|-----------------------------|---------------------|
| GET    | /api/v1/productos           | Listar todos        |
| GET    | /api/v1/productos/{id}      | Obtener uno         |
| POST   | /api/v1/productos           | Crear               |
| PUT    | /api/v1/productos/{id}      | Actualizar          |
| DELETE | /api/v1/productos/{id}      | Eliminar            |
-------------------------------------------------------------
### Inventario
--------------------------------------------------------------------------------
| Método | Ruta                                      | Acción                   |
|--------|-------------------------------------------|--------------------------|
| GET    | /api/v1/inventario                        | Listar todos             |
| GET    | /api/v1/inventario/producto/{id_producto} | Filtrar por producto     |
| POST   | /api/v1/inventario                        | Registrar entrada        |
| DELETE | /api/v1/inventario/{id}                   | Eliminar registro        |
--------------------------------------------------------------------------------
### Ventas
-----------------------------------------------------------------------------
| Método | Ruta                  | Acción                                   |
|--------|-----------------------|------------------------------------------|
| GET    | /api/v1/ventas        | Listar todas                             |
| GET    | /api/v1/ventas/{id}   | Obtener una                              |
| POST   | /api/v1/ventas        | Registrar (descuenta stock automático)   |
| DELETE | /api/v1/ventas/{id}   | Eliminar                                 |
----------------------------------------------------------------------------
### Catálogos (roles, unidades, vías, vigencias, laboratorios)
-----------------------------------
| Método | Ruta                   |
|--------|------------------------|
| GET    | /api/v1/roles          |
| GET    | /api/v1/unidades       |
| GET    | /api/v1/vias           |
| GET    | /api/v1/vigencias      |
| GET    | /api/v1/laboratorios   |
| POST   | /api/v1/roles          |
| POST   | /api/v1/unidades       |
| POST   | /api/v1/vias           |
| POST   | /api/v1/vigencias      |
| POST   | /api/v1/laboratorios   |
-----------------------------------
---

## Comandos útiles

```bash
# Detener los contenedores (sin borrar datos)
docker-compose stop

# Detener Y eliminar contenedores (los datos en el volumen se conservan)
docker-compose down

# Detener Y eliminar TODO incluyendo la base de datos
docker-compose down -v

# Entrar a la consola MySQL
docker exec -it gestion_db mysql -u gestion_user -pgestion_pass gestion_productos

# Entrar al contenedor de la API
docker exec -it gestion_api bash

# Reconstruir solo la API (si HAY CAMBIOS EN  requirements.txt)
docker-compose up --build api

# Ver contenedores corriendo
docker ps
```

---