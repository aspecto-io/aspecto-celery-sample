from tracing import instrument
from celery import Celery
from celery.signals import worker_process_init

app = Celery('calculator', broker_url='redis://localhost:6379/0')

@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    instrument()

@app.task
def add(x, y):
    # raise Exception('error in add')
    return x + y
