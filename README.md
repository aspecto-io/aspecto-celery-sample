Installs:
```commandline
pip install opentelemetry-exporter-otlp
pip install opentelemetry-api
pip install opentelemetry-sdk
pip install opentelemetry-instrumentation-celery
```

# Sample task file
This is the task.py that defines the celery task and adds a task to the queue in redis. 
It uses the instrument function that resides in tracing.py file that you can copy to your own repo.
```python
from celery import Celery
from tracing import instrument

instrument()
app = Celery('tasks', broker_url='redis://localhost:6379/0')

@app.task
def add(x, y):
    return x + y

add.delay(2, 3)
```
# Running your celery task:
Take the aspecto token from the settings in aspecto.io and put it here as env var.
Also, replace OTEL_SERVICE_NAME with the relevant service name
Also, replace the word task after celery -A with the file name that contains your celery task. same as 
```commandline
OTEL_SERVICE_NAME=service-name OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=https://otelcol.aspecto.io:4317 OTEL_EXPORTER_OTLP_HEADERS=Authorization=aspecto-token celery -A task worker -l INFO --concurrency=1
```

