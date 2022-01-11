from celery import Celery
from tracing import instrument

instrument()
app = Celery('tasks', broker_url='redis://localhost:6379/0')

@app.task
def add(x, y):
    return x + y

add.delay(2, 3)