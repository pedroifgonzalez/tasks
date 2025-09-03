#!/usr/bin/env python

from gunicorn.app.base import BaseApplication

from src.core.config import settings
from src.core.logging import logger


class StandaloneApplication(BaseApplication):
    """Gunicorn application for running FastAPI with proper workers."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    import main

    # Log startup information
    logger.info(f"Starting server with {settings.WORKERS_COUNT} workers")

    # Configure Gunicorn options
    options = {
        "bind": "0.0.0.0:8000",
        "workers": settings.WORKERS_COUNT,
        "worker_class": settings.WORKER_CLASS,
        "timeout": 120,
        "keepalive": 5,
        "max_requests": 1000,
        "max_requests_jitter": 50,
        "accesslog": "-",
        "errorlog": "-",
        "loglevel": "info",
        "proc_name": "tasks_api",
    }

    # Run the application with Gunicorn
    StandaloneApplication(main.app, options).run()
