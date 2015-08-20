from fabric.context_managers import cd
from fabric.operations import sudo
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
from fabric.network import ssh

import os

import random


REPO_URL = 'https://github.com/TzvetomirTodorov/Test-Driven-Development-with-Python'

HOME = os.getenv('HOME')

env.user = 'ubuntu'
env.hosts = ['ec2-54-148-178-63.us-west-2.compute.amazonaws.com','54.148.178.63',]
env.key_filename = ['%s/.ssh/TzvettyAWSEC2Ubuntu1404PV.pem' % HOME]

def deploy():
    _host = 'lists'
    site_folder = '/home/%s/srv/webapps/%s' % (env.user, _host)  
    source_folder = site_folder + '/Test-Driven-Development-with-Python'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, _host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'Test-Driven-Development-with-Python'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))  
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdef*ghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../bin/virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
    ))


def _update_static_files(source_folder):
    run('cd %s && ../bin/virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder,
    ))

def _update_database(source_folder):
    run('cd %s && ../bin/virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder,
    ))