# Gunicorn Configuration for VeroctaAI Production
# This file configures the WSGI server for optimal production performance

import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 10000)}"
backlog = 2048

# Worker processes
workers = int(os.environ.get('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2))
worker_class = 'sync'
worker_connections = 1000
timeout = int(os.environ.get('TIMEOUT', 120))
keepalive = 2

# Restart workers
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'veroctai-backend'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance tuning
worker_tmp_dir = '/dev/shm'  # Use memory for worker temp files

# Graceful shutdown
graceful_timeout = 30

# Development vs Production
if os.environ.get('FLASK_ENV') == 'development':
    reload = True
    workers = 1
else:
    reload = False