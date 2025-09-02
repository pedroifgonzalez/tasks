## Task at hand

Crea una **API REST** usando **FastAPI** y **PostgreSQL** para administrar una lista de tareas (**TODOs**).

### Requerimientos funcionales
1. Cada tarea debe tener los siguientes campos:  
   - `id` (UUID o entero autoincremental)  
   - `título` (string)  
   - `descripción` (string, opcional)  
   - `estado` (pendiente/completada)  
   - `fecha_creación` (timestamp)  
   - `id_usuario` (para distinguir tareas entre diferentes usuarios)  

2. La API debe exponer los siguientes endpoints:  
   - `POST /tasks` → Crear una nueva tarea.  
   - `GET /tasks` → Listar todas las tareas del usuario autenticado.  
   - `GET /tasks/{id}` → Obtener el detalle de una tarea por su ID.  
   - `PUT /tasks/{id}` → Actualizar una tarea (estado, título o descripción).  
   - `DELETE /tasks/{id}` → Eliminar una tarea.  

3. **Autenticación básica**:  
   - Implementar un sistema sencillo de autenticación (ejemplo: JWT o token en headers).  
   - Cada usuario solo puede acceder a sus propias tareas.  

4. **Persistencia en base de datos**:  
   - Usa **PostgreSQL** (no SQLite).  
   - Define correctamente los modelos usando **SQLAlchemy o SQLModel**.  

---

## ⚡️ Problemáticas adicionales a considerar

La API se usará en un **entorno real**. Considera lo siguiente al diseñar tu solución:

1. **Alta concurrencia**  
   - La aplicación será utilizada por muchos usuarios al mismo tiempo.  

2. **Grandes volúmenes de datos**  
   - Algunos usuarios pueden tener cientos o miles de tareas.  

3. **Escenarios de error**  
   - Es posible que un usuario intente acceder a una tarea que no existe o envíe datos inválidos.  

4. **Seguridad**  
   - Cada usuario debe tener acceso solo a sus propias tareas.  

👉 Cómo resuelvas estos puntos dependerá de tu criterio y experiencia.  

---

## 🌟 Plus (no obligatorio, pero valorado)

- Tests automatizados.  
- Docker Compose para levantar la API y PostgreSQL fácilmente.  
- Logging básico para errores y auditoría.  
- Migraciones con **Alembic**.  

---