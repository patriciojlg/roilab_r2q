from rq.job import Job
from redis import Redis
from rq import Queue
redis_conn = Redis()
q = Queue("default", connection=redis_conn)
for job in q.jobs:
    job.delete()
q.empty()

redis_conn = Redis()  # Ajusta host/puerto/db si es necesario
redis_conn.flushall()  # ⚠️ Elimina TODO: todas las keys de todos los DBs