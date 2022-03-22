from opentelemetry.instrumentation.celery import CeleryInstrumentor
# from opentelemetry.instrumentation.redis import RedisInstrumentor

import logging
bootstrap_logger = logging.getLogger('opentelemetry')
bootstrap_logger.setLevel(logging.DEBUG)
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


def instrument(*args, **kwargs):
    provider = TracerProvider()
    # simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
    simple_processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(simple_processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    CeleryInstrumentor().instrument()
    # RedisInstrumentor().instrument(tracer_provider=provider)

