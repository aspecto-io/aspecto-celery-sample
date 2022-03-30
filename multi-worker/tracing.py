from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from models.calculation import engine
# from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.trace import (
   format_span_id,
   format_trace_id,
   get_current_span,
)

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
    SQLAlchemyInstrumentor().instrument(
        engine=engine,
    )
    # RedisInstrumentor().instrument(tracer_provider=provider)


def print_otel_data():
    span_context = get_current_span().context
    trace_id = format_trace_id(span_context.trace_id)
    span_id = format_span_id(span_context.span_id)
    print(f'OTEL_DATA ||| Trace id {trace_id}, Span id: {span_id}')