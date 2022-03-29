from tracing import instrument
from celery import Celery, group, chord
from celery.signals import worker_process_init

from calculator import add

app = Celery('manager', broker_url='redis://localhost:6379/0')

@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    instrument()


def some_func():
    return 1


@app.task
def add_calculation_request():
    # raise Exception('error in add')
    lazy_group = group([add.s(2, 3), add.s(4, 3), add.s(5, 3), add.s(7, 3)])
    result = lazy_group.apply_async(queue='calculator')
    # result = chord(lazy_group, some_func)
    # result = promise.get()
    print(result)



