from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    ConsoleSpanExporter,
)


def configure_tracing():
    resource = Resource.create(
        {
            "service.name": "automobile-ai-agent",
            "service.version": "1.0.0",
            "deployment.environment": "dev",
        }
    )

    provider = TracerProvider(
        resource=resource
    )

    processor = SimpleSpanProcessor(
        ConsoleSpanExporter()
    )

    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
