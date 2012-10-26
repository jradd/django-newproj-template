import os
import time

from fabric.api import env, local, prompt, put, require, run
from fabric.contrib.project import rsync_project


"""
THIS FILE MUST BE CONFIGURED BEFORE USE

Configuration

# Setup the necessary environments. The framework for the first, production()
# is sketched out below. At a minimum define teh production environment.

# This uses python2.7 as the default call to Python. If the server uses
# `python` or `python2.6` or `python3` or `py`, find and replace all the
# instances of python2.7 with whatever your server uses.

# This assumes that the Python environment on the server is defined using
# VirtualEnv and VirtualEnvWrapper and that a virtual environment has already
# been created for the project there.


Usage Notes

# Setup the necessary directories on the server (1-time only)

# This file assumes that the directories referenced in the path, media_root
# and static_root are already created at this point.

$ fab <environment> remote_setup

# Upload the first set of files but don't do anything with it
$ fab <environment> upload_latest

# With that in place use the stable-req.txt file from within to install
# site packages
$ fab <environment> load_packages

# And then deploy the project:
$ fab <environment> deploy - deploys your application


"$ fab production deploy" runs the following tasks:

# Compiles SASS for production
# Collects static files into the static files directory
# Uploads the latest version of the project from local Git repository
# Migrates and syncs the database(s)
# Restarts apache
# Removes legacy production deployments to keep only the latest (5) versions
"""

# !Global Settings
# Django Project Name
env.project_name = 'myproject'

env.local_static_root = os.path.join(os.path.dirname(__file__),
    '%(project)s/static' % {'project': env.project_name})


# !Environments
def production():
    # Command to use to restart Apache, this will vary between hosts
    # On WebFaction it is: /home/<username>/webapps/<application name>,
    # usually 'django'>/apache2/bin/restart
    # In a Ubuntu server it is: apache2ctl graceful
    env.apache_restart_command = ''
    # One or multiple username@server/IP address combos
    env.hosts = ['']
    # Connection and sudo password (this can be left as an empty string
    # and Fabric will prompt as necessary)
    env.password = ''
    # Name of the virtual environment
    env.virtualenv_name = ''
    # Absolute path to where the application will be deployed
    # (directory immediately above project in virtual environemt).
    # Don't end with a trailing slash.
    # On Webfaction this will be:
    # '/home/<accountname>/.virtualenvs/<virtualenv_name>'
    env.path = ''
    # Absolute path to where media files will be served from
    # This is the same as settings.MEDIA_ROOT
    # Don't end with a trailing slash
    env.remote_media_root = ''
    # Absolute path to the directory above where static files
    # will be served from. This is the same as settings.STATIC_ROOT.
    # Don't end with a trailing slash.
    env.remote_static_root = ''

    # The following settings are for the grab_data method.
    # Name of remote database (must be PostgreSQL).
    # This is the same as settings.DATABASES['default']['NAME']
    env.database_name = ''
    # User of remote database.
    # This is the same as settings.DATABASES['default']['USER']
    env.database_user = ''
    # Path to tmp or other remote directory for temporary storage.
    # Don't end with a trailing slash
    env.temp_path = ''


# !Host Tasks
def deploy():
    "Deploy the latest version of the site to the server(s)."
    prompt('Git branch:', 'git_branch', default='master')
    _deploy()


def deploy_and_loaddata():
    "Deploy and then load specified fixtures."
    prompt('Git branch:', 'git_branch', default='master')
    _deploy()
    _load_fixtures()


def grab_data():
    "Copies remote database locally."
    now = time.strftime('%Y%m%d%H%M%S')
    dbname = '%(dbname)s.%(now)s' % {'dbname': env.database_name, 'now': now}
    run('pg_dump -U %(dbuser)s -W %(dbname)s > '\
        '%(temp_path)s/%(new_dbname)s.sql' % {
            'dbname': env.database_name,
            'dbuser': env.database_user,
            'new_dbname': dbname,
            'temp_path': env.temp_path})
    local('scp -rpv %(user_at_host)s:%(temp_path)s/%(dbname)s.sql '\
        '%(current_dir)s/%(dbname)s.sql' % {
            'current_dir': os.path.dirname(__file__),
            'dbname': dbname,
            'temp_path': env.temp_path,
            'user_at_host': env.hosts[0]})
    run('rm %(temp_path)s/%(dbname)s.sql' % {
        'dbname': dbname,
        'temp_path': env.temp_path})


def remote_setup():
    "Create directories on the server for the project. Assumes Static and "\
    "Media have already been created otherwise it will err."
    run('cd %(path)s; mkdir %(project)s; mkdir packages; mkdir releases' % {
        'path': env.path, 'project': env.project_name})
    run('chmod 766 %(media)s' % {'media': env.remote_media_root})


def restart_server():
    _reload_apache()


# Rarely Used Host Tasks, Generally for Setup of a New Environment
def deploy_static():
    "Compile SASS for production and replace static files on server."
    _compile_sass()
    _deploy_static()


def load_data():
    "Load specified fixtures. Runs locally on the server so deploy or upload "\
    "latest first."
    _load_fixtures()


def load_packages():
    "Load packages from requirements file. Runs locally on the server so "\
    "deploy or upload latest before running. Requires PIP to be installed on "\
    "the server."
    _load_packages()


def upload_latest():
    "Use sparingly during setup because files will be changed but database "\
    "will not be migrated nor will the server be restarted. For example "\
    "before running load_data or load_packages."
    env.release = time.strftime('%Y%m%d%H%M%S')
    prompt('Git branch:', 'git_branch', default='master')
    _upload_archive_from_git()
    _symlink_current_release()
    _cleanup()


# !Helper Tasks
def _output_message(msg):
    print ""
    print "%s" % '-' * 80
    print ""
    print "%s" % msg
    print ""
    print "%s" % '-' * 80
    print ""


def _cleanup(keep=5):
    """Remove all previous version except latest n"""
    # `grep -v ^p` ignores any files beginning with 'p' (ie the 'previous'
    # symlink (for old use cases where there was a previous symlink)
    dirs = ['releases', 'packages']
    for d in dirs:
        run("cd %(path)s/%(dir)s/ && ls ./  | grep -v ^p | sort | "\
            "head --lines=-%(keep)i | xargs rm -rf" % {'path': env.path,
            'dir': d, 'keep': keep})


def _compile_sass():
    "Compile SASS stylesheets and update repo"
    _output_message("Compiling SASS stylesheets and updating repo.")
    local('compass compile -e production --force '\
        '%(project)s/static_media/stylesheets' % {'project': env.project_name})
    try:
        local('git commit -am "compiling sass for production"',
            capture=False)
    except:
        # This will be thrown if the stylesheets haven't changed during the
        # compile. A 'Nothing to commit.' message will still be shown.
        _output_message("Commit failed for reason above. "\
            "Continuing on with deployment.")


def _deploy():
    env.release = time.strftime('%Y%m%d%H%M%S')

    _compile_sass()
    _deploy_static()
    _upload_archive_from_git()
    _symlink_current_release()
    _migrate_databases()
    _reload_apache()
    _cleanup()


def _deploy_static():
    local('./manage.py collectstatic --noinput')
    rsync_project(
        remote_dir=env.remote_static_root,
        local_dir=env.local_static_root,
        delete=True)


def _load_fixtures():
    "Load fixtures"
    prompt('Which fixtures to load? (Space separate names):', 'fixtures')
    run('cd %(path)s/%(project)s; workon %(virtualenv)s; '\
        'python2.7 manage.py loaddata %(fixtures)s' % {'path': env.path,
        'project': env.project_name, 'virtualenv': env.virtualenv_name,
        'fixtures': env.fixtures})


def _load_packages():
    run('workon %(virtualenv)s; pip install -r '\
        '%(path)s/%(project)s/stable-req.txt' % {
        'virtualenv': env.virtualenv_name, 'path': env.path,
        'project': env.project_name})


def _migrate_databases():
    "Migrate databases"
    run('cd %(path)s/%(project)s; workon %(virtualenv)s; '\
        'python2.7 manage.py migrate; python2.7 manage.py syncdb' % {
        'path': env.path, 'project': env.project_name,
        'virtualenv': env.virtualenv_name})


def _reload_apache():
    "Reload the apache server"
    run('%(command)s' % {'command': env.apache_restart_command})


def _symlink_current_release():
    "Symlink our current release"
    require('release', provided_by=[deploy])
    run('cd %(path)s; rm -rf %(project)s;'\
        'ln -s releases/%(release)s %(project)s' % {'path': env.path,
        'release': env.release, 'project': env.project_name})


def _upload_archive_from_git():
    "Create an archive from the current Git master branch and upload it"
    require('release', provided_by=[deploy])

    local('git archive --format=zip %(branch)s > %(release)s.zip' % {
        'branch': env.git_branch, 'release': env.release})
    run('mkdir %(path)s/releases/%(release)s' % {'path': env.path,
        'release': env.release})
    put('%(release)s.zip' % {'release': env.release}, '%(path)s/packages/' % {
        'path': env.path})
    run('cd %(path)s/releases/%(release)s && '\
        'unzip ../../packages/%(release)s.zip' % {'path': env.path,
        'release': env.release})
    local('rm %(release)s.zip' % {'release': env.release})
