import platform
import psutil
import os
import re
from datetime import date, datetime
from time import sleep
from django.conf import settings
from django.utils.translation import gettext as _


arg_celery_conf = 'worker1'
arg_celery_log  = f'--loglevel=INFO --logfile={settings.CELERY_LOG}/worker-%n.log'
arg_celery_pid  = f'--pidfile={settings.CELERY_PID}/worker-%n.pid'
celery_start    = f'celery -A {settings.CELERY_PROJECT} multi start {arg_celery_conf} {arg_celery_log} {arg_celery_pid}'
celery_restart  = f'celery -A {settings.CELERY_PROJECT} multi restart {arg_celery_conf} {arg_celery_log} {arg_celery_pid}'
celery_stop     = f'celery multi stopwait {arg_celery_conf} {arg_celery_pid}'


def popen(cmdline):
    p = os.popen(cmdline)
    output = p.read()
    p.close()
    return output


def start_service(res, service_name, cmd):
    service = is_running(service_name, True, True)
    if service: # ensure that service is running
        res['status'] = True
        res['data'] = f"PID: {service.pid} | User: {service.username()}"
        return res
    output = popen(cmd)
    sleep(2) # wait for finishing execution
    service = is_running(service_name, True, True)
    if service: # ensure that celery worker is running
        res['status'] = True
        res['data'] = f"PID: {service.pid} | User: {service.username()}"
    else:
        res['messages'] = output
    return res


def stop_service(res, service_name, cmd):
    service = is_running(service_name, True, True)
    if not service: # ensure that service is not running
        res['status'] = True
        res['data'] = _('Deactivated')
        return res
    output = popen(cmd)
    sleep(2) # wait for finishing execution
    service = is_running(service_name, True, True)
    if not service: # ensure that celery worker is running
        res['status'] = True
        res['data'] = _('Deactivated')
    else:
        res['messages'] = output
    return res


def toggle_celery_worker(res, command):
    service_name = 'celery'
    if command == 'start':
        res = start_service(res, service_name, celery_start)
    if command == 'stop':
        res = stop_service(res, service_name, celery_stop)
    return res


def toggle_redis_server(res, command):
    '''
        Before use this service
        ensure that you have modified /etc/sudoers.d/user
        ex: %user_name ALL=NOPASSWD: /etc/init.d/redis-server
    '''
    service_name = 'redis-server'
    if command == 'start':
        res = start_service(res, service_name, 'sudo /etc/init.d/redis-server start')
    if command == 'stop':
        res = stop_service(res, service_name, 'sudo /etc/init.d/redis-server stop')
    return res


def get_sys_info():
    virtual_memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    return {
        'platform': platform.platform(),
        'os': f'{platform.system()} ({platform.version()})',
        'architecture': platform.architecture(),
        'processor': platform.processor(),
        'cpu_usage': psutil.cpu_percent(),
        'virtual_memory': {
            'used': virtual_memory.used,
            'free': virtual_memory.free,
            'available': virtual_memory.available,
        },
        'disk_usage': {
            'used': disk_usage.used,
            'free': disk_usage.free,
        },
    }

def find_process(process_name, by_user=False, by_cmdline=False):
    '''
        Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string
            process_name = process_name.lower()
            if process_name in proc.name().lower():
                return proc
            if by_cmdline and process_name in proc.cmdline():
                return proc
            if by_user and process_name in proc.username().lower():
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def is_running(process_name, by_user=False, by_cmdline=False):
    return find_process(process_name, by_user, by_cmdline)


