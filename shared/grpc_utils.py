from prometheus_client import start_http_server
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer, GrpcInstrumentorClient
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace, metrics
from opentelemetry.exporter.zipkin.proto.http import ZipkinExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider

def init_grpc_telemetry(service_name, zipkin_url = None, otel_endpoint = None, prometheus_port = None, is_client = False) -> None:
        
    resource = Resource(attributes={SERVICE_NAME: service_name})

    if zipkin_url:
        span_processor = BatchSpanProcessor(ZipkinExporter(endpoint=zipkin_url))
    elif otel_endpoint:
        span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otel_endpoint))   
        
    
    if span_processor:
        tracer_provider = TracerProvider(resource=resource)
        tracer_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(tracer_provider)
        
    if prometheus_port != None:
        start_http_server(prometheus_port)
        reader = PrometheusMetricReader()
        meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
        metrics.set_meter_provider(meter_provider)
        
    GrpcInstrumentorClient().instrument()
    GrpcInstrumentorServer().instrument()
    

