import os

workers = int(os.environ.get('WEB_CONCURRENCY', 2))
threads = int(os.environ.get('PYTHON_MAX_THREADS', 1))
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")
loglevel = os.environ.get('GUNICORN_LOGLEVEL', 'info')
accesslog = '-'
errorlog = '-'
