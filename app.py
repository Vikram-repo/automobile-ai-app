import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import Response
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from graph.graph import graph
from memory.database import init_db

from observability.logging_config import (
    configure_logging,
    get_logger,
)

from observability.tracing import configure_tracing

from observability.metrics import (
    REQUEST_COUNT,
    REQUEST_ERRORS,
    REQUEST_LATENCY,
    ACTIVE_REQUESTS,
)


# --------------------------------------------------
# Observability Initialization
# --------------------------------------------------

configure_logging()
configure_tracing()

log = get_logger()


# --------------------------------------------------
# Database Initialization
# --------------------------------------------------

init_db()


# --------------------------------------------------
# Request ID + Metrics Middleware
# --------------------------------------------------

class RequestIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # Clear context from previous request
        clear_contextvars()

        # Read existing request ID or generate a new one
        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid.uuid4())
        )

        # Bind request ID to structlog context
        bind_contextvars(
            request_id=request_id
        )

        method = request.method
        path = request.url.path

        # Track active requests
        ACTIVE_REQUESTS.inc()

        # Start latency timer
        start_time = time.perf_counter()

        log.info(
            "request_started",
            method=method,
            path=path,
        )

        try:

            response = await call_next(request)

            status_code = response.status_code

            # Request counter
            REQUEST_COUNT.labels(
                method=method,
                path=path,
                status=str(status_code),
            ).inc()

            log.info(
                "request_completed",
                status_code=status_code,
            )

            # Return request ID to client
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as exc:

            # Error counter
            REQUEST_ERRORS.labels(
                method=method,
                path=path,
            ).inc()

            log.error(
                "request_failed",
                error=str(exc),
                error_type=type(exc).__name__,
            )

            raise

        finally:

            # Record latency
            latency = time.perf_counter() - start_time

            REQUEST_LATENCY.labels(
                method=method,
                path=path,
            ).observe(latency)

            # Request completed
            ACTIVE_REQUESTS.dec()

            # Clear request context
            clear_contextvars()


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="Production Ready AI Agent",
    version="1.0.0",
)

# Request ID + Metrics middleware
app.add_middleware(RequestIDMiddleware)

# OpenTelemetry FastAPI instrumentation
FastAPIInstrumentor.instrument_app(app)


# --------------------------------------------------
# Request Schema
# --------------------------------------------------

class ChatRequest(BaseModel):

    thread_id: str
    message: str


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
def home():

    log.info(
        "health_check",
        endpoint="/",
    )

    return {
        "status": "running",
        "framework": "LangGraph",
        "version": "1.0.0",
    }


# --------------------------------------------------
# Prometheus Metrics Endpoint
# --------------------------------------------------

@app.get("/metrics")
def metrics():

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    log.info(
        "chat_request",
        thread_id=request.thread_id,
    )

    config = RunnableConfig(
        configurable={
            "thread_id": request.thread_id,
        }
    )

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=request.message
                )
            ],

            # Future use
            # Memory / User Context
            "user_id": request.thread_id,
        },
        config=config,
    )

    log.info(
        "chat_response",
        thread_id=request.thread_id,
    )

    return {
        "thread_id": request.thread_id,
        "response": result["messages"][-1].content,
    }
