# FastAPI + RQ + Redis Task Manager

Este proyecto es un **gestor de tareas en cola** utilizando **FastAPI, RQ (Redis Queue) y Redis**. Permite encolar tareas, consultar su estado y eliminarlas cuando están completadas.

## 📦 Requisitos

- Docker y Docker Compose
- Python 3.8+
- FastAPI
- Redis
- RQ (Redis Queue)

## 🚀 Instalación y Ejecución

### 1️⃣ Iniciar Redis con Docker Compose

Ejecuta el siguiente comando para levantar Redis:

```bash
docker-compose up -d
```

### 2️⃣ Iniciar el Worker de RQ

El worker de RQ procesa las tareas encoladas. Para iniciarlo, ejecuta:

```bash
rq worker default --url redis://localhost:6379
```

### 3️⃣ Iniciar FastAPI

Ejecuta el servidor de FastAPI con:

```bash
uvicorn main:app --reload
```

## 📌 Endpoints Disponibles

### Crear una nueva tarea
**POST** `/ftd-queues/tasks/`
```json
{
  "duration": 5,
  "payload": {"key": "value"}
}
```

### Obtener el estado de una tarea
**GET** `/ftd-queues/tasks/{job_id}`

### Listar todas las tareas
**GET** `/ftd-queues/tasks/`

### Eliminar una tarea completada
**DELETE** `/ftd-queues/tasks/{job_id}`

⚠️ **Solo se pueden eliminar tareas con estado "completed".**

## 📜 Licencia
Este proyecto está bajo la licencia MIT.