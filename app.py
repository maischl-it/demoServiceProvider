import requests
import time
import redis

from flask import Flask, request

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
RedisInstrumentor().instrument()

tracer=None

@app.route("/", methods=['POST', 'GET'])
def home():
    carrier = {'traceparent': request.headers["TRACEPARENT"]}
    ctx = TraceContextTextMapPropagator().extract(carrier=carrier)

    with tracer.start_as_current_span('spanProvider', context=ctx) as span:
        span.set_attribute("application","provider")
    requests.get("https://web.de")

    time.sleep(2)

    redis.set('testkey', 'Hello Meetup')
    
    entry = redis.get('testkey')
    print(entry)

    return entry

# @app.route("/redis")
# def redisDemo():
#     redis.set('testkey', 'Hello Meetup')
    
#     entry = redis.get('testkey')
#     print(entry)

#     return entry

if __name__ == '__main__':
    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({SERVICE_NAME: "DemoProvider"}))

    )

    jaeger_exporter=JaegerExporter(
        # agent_host_name="172.17.0.2",
        agent_host_name="simplest-agent.default.svc.cluster.local",
        agent_port=6831
    )

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
    
    tracer=trace.get_tracer(__name__)

    pool = redis.ConnectionPool(host='redis-master.demo.svc.cluster.local', port=6379, db=0, password="lEoa6dGvGP")
    redis = redis.Redis(connection_pool=pool)

    app.run(host='0.0.0.0', port=3000)
