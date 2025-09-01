# logging.py

# Purpose: Structured JSON logs + trace correlation.
# Put inside: uvicorn/root logger config, request ID/trace ID filter, log level by env.
# Tip: Use Google’s log fields (severity, logging.googleapis.com/trace).