import time
import celery


app = celery.Celery(
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    broker_connection_retry_on_startup = True
)

@app.task()
def cpu_bound(a, b):
    time.sleep(1)
    return a + b