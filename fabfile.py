import os
import time

from fabric.api import env, local, prompt, put, require, run
from fabric.contrib.project import rsync_project


"""
THIS FILE MUST BE CONFIGURED BEFORE USE
"""

# !Global Settings
# Django Project Name
env.project_name = 'myproject'

env.local_static_root = os.path.join(os.path.dirname(__file__),
    '%(project)s/static' % {'project': env.project_name})


# !Environments
def production():
    # Command to use to restart Apache, this will vary between hosts
    # On WebFaction it is:
    #   /home/<username>/webapps/<application name>/apache2/bin/restart,
    # In a Ubuntu server it is: apache2ctl graceful
    env.apache_restart_command = ''
    # One or multiple username@server/IP address combos
    env.hosts = ['']
    # Connection and sudo password (this can be left as an empty string
    #   and Fabric will prompt as necessary)
    env.password = ''
    # Name of the virtual environment
    env.virtualenv_name = ''
    # Absolute path to where the application will be deployed
    #   (directory immediately above project in virtual environemt).
    # Don't end with a trailing slash.
    # On Webfaction this will be:
    #   '/home/<accountname>/.virtualenvs/<virtualenv_name>'
    env.path = ''
    # Absolute path to where media files will be served from.
    # This is the same as settings.MEDIA_ROOT.
    # Don't end with a trailing slash.
    env.remote_media_root = ''
    # Absolute path to the directory above where static files.
    #   will be served from. This is the same as settings.STATIC_ROOT.
    # Don't end with a trailing slash.
    env.remote_static_root = ''
    
    # The following settings are environment specific and generally 
    #   should be named after the name of this environment.
    
    # Default branch of Git repository to be used to deploy to 
    #   this environment. 
    env.default_branch = 'master'
    # Requirements file to be used for this environment.
    # Should match the name of this environment followed by '.txt'
    # Dynamically created by the script at: 
    #   <project_name>/requirements/<requirements_filename>
    env.requirements_filename = 'production.txt'
    # Settings module to be used for this environment.
    # Should extend <project_name>/settings/base.py.
    # Lives at:
    #   <project_name>/settings/<settings_module>.py
    # Filename should match the name of this environment followed by '.py'
    env.settings_module = 'production'

    # The following settings are for the grab_data method ONLY
    #   and are otherwise OPTIONAL.

    # Name of remote database (must be a PostgreSQL-type database).
    # This is the same as settings.DATABASES['default']['NAME'].
    env.database_name = ''
    # User of remote database.
    # This is the same as settings.DATABASES['default']['USER'].
    env.database_user = ''
    # Path to tmp or other remote directory for temporary storage.
    # Don't end with a trailing slash
    env.temp_path = ''


# !Host Tasks
def deploy():
    "Deploy the latest version of the site to the server(s)."
    prompt('Git branch:', 'git_branch', default='%(branch)s' % {
        'branch': env.default_branch})
    _deploy()


def deploy_and_loaddata():
    "Deploy and then load specified fixtures."
    prompt('Git branch:', 'git_branch', default='%(branch)s' % {
        'branch': env.default_branch})
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


def load_data():
    "Load specified fixtures. Runs locally on the server so deploy first."
    _load_fixtures()


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
    _freeze_packages()
    _deploy_static()
    _upload_archive_from_git()
    _symlink_current_release()
    _load_packages()
    _migrate_databases()
    _reload_apache()
    _cleanup()


def _deploy_static():
    local('./manage.py collectstatic --noinput')
    rsync_project(
        remote_dir=env.remote_static_root,
        local_dir=env.local_static_root,
        delete=True)


def _freeze_packages():
    local('pip freeze > %(current_dir)s/requirements/%(requirements_filename)s' % {
            'current_dir': os.path.dirname(__file__),
            'requirements_filename': env.requirements_filename,
        })
    try:
        local('git commit -am "freezing requirements for server environment"',
            capture=False)
    except:
        # This will be thrown if the requirments doc hasn't changed during the
        # freeze. A 'Nothing to commit.' message will still be shown.
        _output_message("Commit failed for reason above. "\
            "Continuing on with deployment.")


def _load_fixtures():
    "Load fixtures"
    prompt('Which fixtures to load? (Space separate names):', 'fixtures')
    run('cd %(path)s/%(project)s; workon %(virtualenv)s; '\
        'python2.7 manage.py loaddata %(fixtures)s '\
        '--settings=myproject.settings.%(settings_module)s' % {'path': env.path,
        'project': env.project_name, 'virtualenv': env.virtualenv_name,
        'fixtures': env.fixtures, 'settings_module': env.settings_module})


def _load_packages():
    run('workon %(virtualenv)s; pip install -r '\
        '%(path)s/%(project)s/requirements/%(requirements_filename)s' % {
        'virtualenv': env.virtualenv_name, 'path': env.path,
        'project': env.project_name,
        'requirements_filename': env.requirements_filename})


def _migrate_databases():
    "Migrate databases"
    run('cd %(path)s/%(project)s; workon %(virtualenv)s; '\
        'python2.7 manage.py migrate --settings=myproject.settings.%(settings_module)s; '\
        'python2.7 manage.py syncdb --settings=myproject.settings.%(settings_module)s' % {
        'path': env.path, 'project': env.project_name,
        'virtualenv': env.virtualenv_name, 'settings_module': env.settings_module})


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
    "Create an archive from the current Git branch and upload it"
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
