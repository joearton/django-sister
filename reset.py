import os
import json
import shutil
import pymysql
import sys
import subprocess


current_dir = os.getcwd()

def get_project():
    project_list = []
    for dirname in os.listdir(current_dir):
        if os.path.isfile(os.path.join(dirname, 'settings.py')) :
            project_list.append(dirname)
        if os.path.isfile(os.path.join(dirname, 'settings', 'default.py')):
            project_list.append(dirname)
    print('Choose Project: ')
    counter = 1
    for project in project_list:
        print('[{0}] {1}'.format(counter, project))
    choose = input('\nProject Name (enter number): ')
    if choose == None or choose.isdigit() == False:
        print('Cancel resetting...')
        os.abort()
    if not choose.isdigit():
        return get_project()
    if int(choose) > len(project_list):
        return get_project()
    project = project_list[int(choose)-1]
    return project


def rename(old, new):
    path, name = os.path.split(old)
    os.rename(old, os.path.join(path, new))


def backup_app(backup_dir, apps):
    print('Start backing up {}'.format(apps))
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    filename = os.path.join(backup_dir, f'{apps}.json')
    if os.path.isfile(filename):
        filename = os.path.join(backup_dir, '{0}-{1}.json'.format(apps, len(os.listdir(backup_dir))))
    loaddata = os.popen('python manage.py dumpdata {0} --output {1}'.format(apps, filename))
    output = loaddata.read()
    if output:
        print(output)
    loaddata.close()
    if os.path.isfile(filename):
        try:
            data = json.load(open(filename, 'r'))
            name, ext = os.path.splitext(os.path.basename(filename))
            rename(filename, f"{name}-{len(data)}{ext}")
        except:
            pass


project = get_project()
print('Connecting to your {0} application...'.format(project))

confirm = input('Enter 12345 to confirm: ')
if confirm != '12345':
    print('Cancel resetting...')
    os.abort()


#------------ start execution ----------#

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{0}.settings'.format(project))
print('Calling Django core modules...')
from django.conf import settings
APPS_DIR = os.path.join(settings.BASE_DIR, settings.APPS_DIRNAME)


print('Start backing up your aurora apps data...')
for apps in os.listdir(APPS_DIR):
    app_dir = os.path.join(APPS_DIR, apps)
    if os.path.isdir(app_dir):
        backup_dir = os.path.join(app_dir, '.backup')
        if not apps.startswith('__'):
            backup_app(backup_dir, apps)


print('Start backing up your non aurora apps data...')
backup_dir = os.path.join(settings.CACHE_DIR, '.backup')
for apps in ['auth', 'sites']:
    backup_app(backup_dir, apps)


print('Please wait, removing old files')
db_settings = settings.DATABASES['default']
if 'USER' in db_settings:
    cursor_type  = pymysql.cursors.DictCursor
    db_connector = pymysql.connect(
       user=db_settings['USER'],
       password=db_settings['PASSWORD'],
       host=db_settings['HOST'],
       port=int(db_settings['PORT']),
       cursorclass=cursor_type
    )
    db_cursor = db_connector.cursor()
    db_cursor.execute("SHOW DATABASES")
    databases = list(map(lambda x: x['Database'], db_cursor.fetchall()))
    if db_settings['NAME'] in databases:
        print('Reseting your database ({0})...'.format(db_settings['NAME']))
        db_cursor.execute("DROP DATABASE {0}".format(db_settings['NAME']))
        db_cursor.execute("CREATE DATABASE {0}".format(db_settings['NAME']))
    db_connector.close()


print('Start removing migrations files and cache')
for apps in os.listdir(APPS_DIR):
    app_dir = os.path.join(APPS_DIR, apps)
    if os.path.isdir(app_dir):
        migrations_dir = os.path.join(app_dir, 'migrations')
        if os.path.exists(migrations_dir):
            for migration in os.listdir(migrations_dir):
                if not migration == "__init__.py":
                    migration_file = os.path.join(migrations_dir, migration)
                    try:
                        print('Removing {0}'.format(migration_file))
                        if os.path.isdir(migration_file):
                            shutil.rmtree(migration_file)
                        else:
                            os.remove(migration_file)
                    except:
                        print('Failed {0}'.format(migration_file))



remove_media = input('Remove media [Yes, Y, No]? ')
if remove_media.lower() in ['yes', 'y']:
    media_directory = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT)
    if os.path.exists(media_directory):
        print('Start reseting media...')
        shutil.rmtree(media_directory)


remove_static = input('Remove staticfiles [Yes, Y, No]?')
if remove_static.lower() in ['yes', 'y']:
    static_directory = os.path.join(settings.BASE_DIR, settings.STATIC_ROOT)
    if os.path.exists(static_directory):
        print('Start reseting static...')
        shutil.rmtree(static_directory)


db_sqlite = os.path.join(settings.BASE_DIR, 'db.sqlite3')
if os.path.isfile(db_sqlite):
    print('Start reseting sqlite3...')
    os.remove(db_sqlite)


print('Start database makemigrations')
makemigrations = subprocess.Popen(['python', 'manage.py', 'makemigrations'])
makemigrations.communicate()
makemigrations.wait()

print('Start migrating database')
migrate = subprocess.Popen(['python', 'manage.py', 'migrate'])
migrate.communicate()
migrate.wait()


print('Start loading fixtures data...')
for apps in os.listdir(APPS_DIR):
    app_dir = os.path.join(APPS_DIR, apps)
    if os.path.isdir(app_dir):
        fixture_dir = os.path.join(app_dir, 'fixtures')
        if os.path.exists(fixture_dir):
            try:
                if len(os.listdir(fixture_dir)) > 0:
                    print('Start loading fixtures on {}'.format(fixture_dir))
                    loaddata = os.popen('python manage.py loaddata {0}/*'.format(fixture_dir))
                    output = loaddata.read()
                    if output:
                        print(output)
                    loaddata.close()
            except:
                print('Failed to loaddata {0}'.format(fixture_dir))


print("\nFinish, don't forget create superuser...")
