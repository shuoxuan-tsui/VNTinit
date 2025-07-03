"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 设置Django的默认环境变量，指定settings模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# get_wsgi_application()是Django提供的WSGI应用入口函数
# 它返回一个符合WSGI规范的Django应用对象，用于与WSGI服务器(如Gunicorn/uWSGI)通信
# 这个应用对象会处理HTTP请求并返回响应
application = get_wsgi_application()
