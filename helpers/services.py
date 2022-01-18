import os
import re

SUDOERS_DIR = '/etc/sudoers.d/'

def popen(cmdline):
    p = os.popen(cmdline)
    output = p.read()
    p.close()
    return output

# check username
user = popen('whoami')
user = re.sub(f'\s', '', user)
if user != 'root':
    print('Sorry, installer must be run by root, you logged as', user)
    os.abort()


def install_redis_server():
    if not os.path.isfile('/etc/init.d/redis-server'):
        print('Redis server is not installed, this script will automatically install it')
        print(popen('apt install redis-server'))
    cmd = '%{username} ALL=NOPASSWD: /etc/init.d/redis-server *\n'
    usernames = ['joearton', 'www-data']
    for username in usernames:
        sudoers_file = os.path.join(SUDOERS_DIR, username)
        if not os.path.isfile(sudoers_file):
            with open(sudoers_file, 'w') as writer:
                writer.write(cmd.format(username=username))
                popen(f'chmod 0444 {sudoers_file}')
                print(f'[{username}] redis service installed', sudoers_file)


install_redis_server()
