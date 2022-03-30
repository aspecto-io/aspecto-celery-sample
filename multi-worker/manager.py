from tracing import instrument, print_otel_data
from celery import Celery, group, chord
from celery.signals import worker_process_init
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.calculation import Calculation, engine
from calculator import add


app = Celery('manager', broker_url='redis://localhost:6379/0')

@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    instrument()
    with Session(engine) as session:
        calc1 = Calculation(x=1, y=1)
        calc2 = Calculation(x=2, y=2)
        calc3 = Calculation(x=3, y=3)
        # calc4 = Calculation(x=1, y=1)
        print(calc1)
        session.add_all([calc1, calc2, calc3])
        session.commit()
        # raise Exception('error in add')
        # lazy_group = group([add.s(2, 3), add.s(4, 3), add.s(5, 3), add.s(7, 3)])
        # result = lazy_group.apply_async(queue='calculator')
        # print(result)


def some_func():
    return 1


@app.task
def add_calculation_request():
    print_otel_data()
    # raise Exception('error in add')
    lazy_group = group([add.s(2, 3), add.s(4, 3), add.s(5, 3), add.s(7, 3)])
    result = lazy_group.apply_async(queue='calculator')
    # result = chord(lazy_group, some_func)
    # result = promise.get()
    print(result)

# engine = create_engine("sqlite://", echo=True, future=True)


@app.task
def add_calculation_requests():
    print_otel_data()
    with Session(engine) as session:
        statement = select(Calculation)
        signatures_to_add = []

        # lazy_group = group([add.s(2, 3), add.s(4, 3), add.s(5, 3), add.s(7, 3)])
        # result = lazy_group.apply_async(queue='calculator')
        for calculation in session.scalars(statement):
            signatures_to_add.append(add.s(calculation.x, calculation.y))
            # print(f'Would add task for {calculation}')
        print(f'tasks to add {signatures_to_add}')
        lazy_group = group(signatures_to_add)
        lazy_group(queue='calculator')


