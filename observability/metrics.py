from prometheus_client import Counter, Gauge, Histogram


REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"],
)

REQUEST_ERRORS = Counter(
    "app_request_errors_total",
    "Total number of failed HTTP requests",
    ["method", "path"],
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

ACTIVE_REQUESTS = Gauge(
    "app_active_requests",
    "Number of currently active HTTP requests",
)
