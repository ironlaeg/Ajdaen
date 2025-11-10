# Gunicorn configuration file
import multiprocessing
import os

# Server socket
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')

# Worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = '-'
errorlog = '-'
loglevel = os.environ.get('LOG_LEVEL', 'info')

# Process naming
proc_name = 'aidaen_gunicorn'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Performance tuning
max_requests = 1000
max_requests_jitter = 50

