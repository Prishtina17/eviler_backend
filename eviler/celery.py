from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите переменную окружения для настройки имени приложения.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eviler.settings')

app = Celery('eviler')

# Используйте строку настроек Django для настройки Celery.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузите модули задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks()