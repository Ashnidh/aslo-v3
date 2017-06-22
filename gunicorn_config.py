import os
import multiprocessing

bind = '0.0.0.0:%s' % os.environ.get('PORT', '5000')
workers = int(
    os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count())
)
timeout = int(os.environ.get('G_TIMEOUT', 30))

accesslog = '-'
access_log_format = '%(m)s %(U)s status=%(s)s time=%(T)ss size=%(B)sb'
