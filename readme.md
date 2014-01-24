# Django New Project Template

Django project template for starting a new project.

## Table of Contents

### Introduction

* [Why Vagrant](#why-vagrant)
* [This Project](#this-project)

### Directions

* [Legend](#legend)
* [Initial setup of Vagrant Base](#initial-setup-of-vagrant-base)
* [Starting a New Project](#starting-a-new-project)
* [Using a Vagrant Virtual Environment That Has Been Shared With You](#using-a-vagrant-virtual-environment-that-has-been-shared-with-you)
* [Deploying to a WebFaction Instance](#deploying-to-a-webfaction-instance)

### Documentation

* [Dependencies](#dependencies)
* [Installed Files](#installed-files)
    * [Git Hooks](#git-hooks-created)
    * [HTML Templates](#html-templates-created)
    * [JavaScript Files](#javascript-files-created)
    * [Stylesheets](#stylesheets-created)
    * [Template Tags](#template-tags-installed)
    * [Fabfile](#fabfile)

### Cheat Sheets

* [Vagrant Command Tips](#vagrant-command-tips)
* [VirtualenvWrapper Command Tips](#virtualenvwrapper-command-tips)
* [PIP Command Tips](#pip-command-tips)
* [Fabric Command Tips](#fabric-command-tips)
* [Django Extensions](#django-extensions)
* [Bash Aliases](#bash-aliases)

# Introduction

## Why Vagrant

* Local development while isolating system-level libraries and executing code in an Ubuntu 64-bit virtual machine on a per-project basis. Continue to edit files in the editor of choice (TextMate, Coda, Dreamweaver, Sublime) on your host machine and view the site in a variety of browsers (Firefox, Chrome, the iPhone Emulator's Safari browser).
* The environment is setup for you. Get team members, freelancers and designers up and running Django with a PostgreSQL database and SASS stylesheets in minutes without changing their host machine's configuration. 

## This Project

### Django,  [Virtualenv](https://pypi.python.org/pypi/virtualenv), [PIP](https://pypi.python.org/pypi/pip), PostgreSQL

This template sets up a number of defaults for `django-admin.py startproject` by encouraging a particular development environment and tool set. It loads an initial set of Django applications, Django templates, CSS files and JavaScript libraries.

On the virtual machine, a new Django project called _myproject_ is created in a virtual environment named _djangoproj_.

This project configures a Django project for use with a PostgreSQL database, _django\_db_, which it installs along with a user, _django\_login_, for said database and installs [South](https://pypi.python.org/pypi/South) for database migrations.

This project also configures the Django project to use the [Django Admin](https://docs.djangoproject.com/en/dev/ref/contrib/admin/) and [Django Sites Framework](https://docs.djangoproject.com/en/dev/ref/contrib/sites/).

#### Separate Settings Files for Development and Production

This template sets up separate development (the Django project running only on your local computer) and production (the Django project running on the world wide web) settings files that inherit from a common base settings file.

This project configures [postactivate](https://github.com/jbergantine/chef-cookbook-djangonewproj/blob/master/recipes/default.rb#L119) and [postdeactivate](https://github.com/jbergantine/chef-cookbook-djangonewproj/blob/master/recipes/default.rb#L120) virtualenv hooks for specifying the proper settings file when working in the virtual environment within Vagrant for development so the `--settings=` flag doesn't need to be explicitly used. Something similar will need to be done in production to [specify the settings file to use](https://docs.djangoproject.com/en/dev/topics/settings/#designating-the-settings).

### Fabric Deployment

This project installs [Fabric](https://pypi.python.org/pypi/Fabric/) and includes a [fabfile](#fabfile) with a number of pre-configured methods for deployment and server management.

### Version Control with Git

This configuration uses a [post-merge Git hook](#post-merge) to sync/migrate the database and compile SASS when pulling changes in from others, as such, it is strongly recommended that you execute Git commands within the virtual environment using the command line rather than using applications installed on the host machine such as Tower or GitHub App. 

### HTML5 Doctype

By default the [_base.html_](#basehtml) template has an HTML5 doctype. For backwards compatibility this project installs [modernizr.js](http://modernizr.com) with an HTML5 shiv for older versions of Internet Explorer to keep them from puking. 

### Mobile First Responsive Design with SASS Stylesheets, Susy Responsive Grids and Server-Level Device Detection

This project installs [SASS along with Compass and Susy responsive grids](#stylesheets-created) and begins sketching in styles with [Gesso](https://github.com/jbergantine/compass-gesso). This project keeps the CSS files out of Git to avoid conflicts and compiles the stylesheets at deployment via Fabric and in production by co-running `runserver` and `compass watch` with Foreman.

This project configures the project for use with [django-mobile](https://pypi.python.org/pypi/django-mobile/) and [django-responsive](https://github.com/mlavin/django-responsive) for doing server-level device and width detection.

### jQuery

This project downloads the latest version of [jQuery](http://jquery.com) and includes it in the base template.

### Minified JavaScript and CSS

This project installs [django_compressor](https://pypi.python.org/pypi/django_compressor) for minifying JavaScript and CSS files.

### SEO

This template includes a sitemaps module, _sitemaps.py_, which is initially configured to create a sitemaps XML file referencing "static" pages of a site but which can be expanded to most any application. The sitemap module is imported into _urls.py_ which sets up routing. 

This template also installs [Django-Robots](https://github.com/jbergantine/django-robots), a small app for creating a _robots.txt_ file.

### Xapian Plain Text Search Ready

This project installs Xapian with Python bindings. You will have to additionally install the [_django-haystack_](https://pypi.python.org/pypi/django-haystack/) and [_xapian-haystack_](https://pypi.python.org/pypi/xapian-haystack) Python packages and [configure the project as appropriate](http://django-haystack.readthedocs.org/en/latest/tutorial.html#configuration).

### memcached Ready

This project installs memcached and Python bindings and configures the development environment (in _myproject/settings/development.py_) to use memcached (although it is commented out as enabling it requries restarting the server to see template changes). The production environment settings file includes the necessary config for memcached but commented out since the production environment will need to have memcached installed onto the server with Python bindings in order for that to work.

### PIL and SORL-Thumbnail Ready

This project installs the necessary libraries (libjpeg, libfreetype, zlib) to use PIL (you will have to still install the [_pil_](https://pypi.python.org/pypi/PIL) or [_pillow_](https://pypi.python.org/pypi/Pillow/) Python package, however). To use SORL-Thumbnail you will have to install the [_pil_](https://pypi.python.org/pypi/PIL) or [_pillow_](https://pypi.python.org/pypi/Pillow/) and [_sorl-thumbnail_](https://pypi.python.org/pypi/sorl-thumbnail/) Python packages and [configure the project as appropriate](http://sorl-thumbnail.readthedocs.org/en/latest/installation.html#setup).

### Redis, Erlang, RabbitMQ and More

Review [Additional Optional Installs](#additional-optional-installs) for how to install other Linux packages such as Redis, Erlang and RabbitMQ.

Review _requirements/base.txt_ for other default Python application choices (and the use cases for them) that you might want to enable out of the box. 

# Directions

## Legend

`(host)` is for commands to run on the host machine, and `(vm)` is for commands to run inside the Vagrant virtual machine. To run commands in the virtual machine you must be SSH'd into it. Instructions for doing so the first time through are provided in context below or in the [Vagrant Command Tips](#vagrant-command-tips) section.

## Initial setup of Vagrant Base

This step only ever needs to be done once. Once the precise64 box is installed on a system the remaining steps refer to that same box regardless of the project.

Download and install [Xcode from the Apple App Store](https://itunes.apple.com/us/app/xcode/id497799835?ls=1&mt=12).

Download virtualbox from http://www.virtualbox.org/wiki/Downloads, install dmg.

Download vagrant from http://downloads.vagrantup.com/, install dmg.

Launch a terminal window, check that it installed:

    (host) $ which vagrant

Add a vagrant box (we'll be using Ubuntu Precise Pangolin (12.04 LTS) 64-bit):

    (host) $ vagrant box add precise64 http://files.vagrantup.com/precise64.box

## Starting a New Project

Make a directory for the project and change to it, replacing `<path_to>` with the path to the project and `<project_name>` with the name of the project.

    (host) $ mkdir <path_to>/<project_name> && cd $_
    
For example, to create a project called 'website' in your home directory:

    (host) $ mkdir ~/website && cd $_

When you're all done, this directory will contain a directory named _myproject_ that matches up with _/vagrant/myproject_ in the virtual envirionment. Virtualbox keeps the two directories in sync so changes to one will be made in the other. This directory contains Django's _manage.py_ file as well as the project's fabfile and PIP requirements doc. Within it is a second _myproject_ directory which contains the Django project. On your host you can launch the text editor of your choice (Panic Coda, TextMate, Sublime, whatever), make edits to any of these files, and those edits will be reflected in the virtual environment immediately.

Create a place for the Chef cookbooks. From within the Vagrant project directory on the host run the following command.

So, extending our example, this would be run from within _~/website/_.

    (host) $ git init
    (host) $ mkdir cookbooks

Clone the Chef cookbooks repositories as needed (we will use the following cookbooks in this guide). 

    (host) $ git submodule add git://github.com/opscode-cookbooks/apt.git cookbooks/apt && git submodule add git://github.com/opscode-cookbooks/build-essential.git cookbooks/build-essential && git submodule add git://github.com/opscode-cookbooks/sudo.git cookbooks/sudo && git submodule add git://github.com/opscode-cookbooks/git.git cookbooks/git && git submodule add git://github.com/opscode-cookbooks/openssl.git cookbooks/openssl && git submodule add git://github.com/opscode-cookbooks/postgresql.git cookbooks/postgresql && git submodule add git://github.com/poise/python.git cookbooks/python && git submodule add git://github.com/opscode-cookbooks/zlib.git cookbooks/zlib && git submodule add git://github.com/opscode-cookbooks/memcached.git cookbooks/memcached && git submodule add git://github.com/jbergantine/chef-cookbook-python-psycopg2.git cookbooks/chef-cookbook-python-psycopg2 && git submodule add git://github.com/jbergantine/chef-cookbook-libjpeg.git cookbooks/chef-cookbook-libjpeg && git submodule add git://github.com/jbergantine/chef-cookbook-libfreetype.git cookbooks/chef-cookbook-libfreetype && git submodule add git://github.com/jbergantine/chef-cookbook-xapian.git cookbooks/chef-cookbook-xapian && git submodule add git://github.com/jbergantine/chef-cookbook-djangonewproj.git cookbooks/chef-cookbook-djangonewproj

Init and update the submodules.

    (host) $ git submodule init
    (host) $ git submodule update

Copy in the Vagrantfile.
    
    (host) $ curl https://gist.github.com/jbergantine/3875868/raw/gistfile1.rb > Vagrantfile
Startup Vagrant and install cookbooks (first time through), use `$ vagrant provision` instead if you mess something up and have to go through it again:

    (host) $ vagrant up

SSH in to the virtualbox:

    (host) $ vagrant ssh 
    
### Additional Optional Installs

#### Erlang and RabbitMQ

    (host) $ git submodule add git://github.com/opscode-cookbooks/erlang.git cookbooks/erlang
    (host) $ git submodule add git://github.com/opscode-cookbooks/rabbitmq.git cookbooks/rabbitmq
    
Then edit the _Vagrantfile_ to include the following in the `cfg.vm.provision :chef_solo do |chef|` loop below the installation of _build-essential_:

    chef.add_recipe "erlang"
    chef.add_recipe "rabbitmq"
   
Reprovision the machine (if it is running) or run `$ vagrant up` if it is not running to reprovision.

    (host) $ vagrant provision

#### Redis

    (host) $ git submodule add git://github.com/miah/chef-redis.git cookbooks/redis

Then edit the _Vagrantfile_ to include the following in the `cfg.vm.provision :chef_solo do |chef|` loop below the installation of _build-essential_:

    chef.add_recipe "redis::server_package"

Reprovision the machine (if it is running) or run `$ vagrant up` if it is not running to reprovision.

    (host) $ vagrant provision

### Setup SSH Keys

Using SSH keys makes pushing and pulling changes from Bitbucket or GitHub or the server a lot easier since you will only have one password to remember. 

#### Creating Keys

If you don't already have SSH keys setup on your Host machine, follow these directions to create them. If you already have SSH keys setup, skip on to the next step, [Copying Your Keys Into the Virtual Environment](#copying-your-keys-into-the-virtual-environment).

Move into the _~/.ssh_ directory:

    (host) $ cd ~/.ssh

Create the key, replacing your_email@youremail.com with your email address:

    (host) $ ssh-keygen -t rsa -C “your_email@youremail.com”
    
When prompted with "Enter file in which to save the key (...):" hit the return key to accept the default value.

When prompted for a passphrase enter a strong passphrase and hit the return key or hit the return key to create a key without a passphrase. 

Print the public key to the terminal window. The following will spit out about 5 lines of text beginning with "ssh-rsa" and ending with your email address. Once you've ran the following command, select all of its output with your mouse and copy it (Command + C should do it to copy it).

    (host) $ cat id_rsa.pub
    
Login to GitHub or Bitbucket or whatever service you're using for Git and add a new key for your account, pasting in the public key from your clipboard. You should now be able to push, pull and clone without having to enter a passphrase for the account (if you set a passphrase for the key you will have to enter that). 

Now you're ready to copy those keys into the Virtual Environment.

#### Copying Your Keys Into the Virtual Environment

SSH into the virtual box if you aren't already there. From the project directory (the one you made in [using the new Vagrant Base Box](#using-the-new-vagrant-base-box)) on your host system run:

    (host) $ vagrant up
    (host) $ vagrant ssh

Open the `id_rsa.pub` file on the virtual box for editing.

    (vm) $ nano ~/.ssh/id_rsa.pub

Copy the public key in a new Terminal window:

    (host) $ cat ~/.ssh/id_rsa.pub|pbcopy

Return to nano on the Virtual Machine. Paste, exit and save changes.

Open the `id_rsa` file on the virtual box for editing. In the Terminal window that is SSH'd into the virtual box run:

    (vm) $ nano ~/.ssh/id_rsa

Copy the private key. In the Terminal window on your host machine run:

    (host) $ cat ~/.ssh/id_rsa|pbcopy

Return to nano on the Virtual Machine. Paste, exit and save changes.

Change permissions of the `id_rsa` file.

    (vm) $ chmod 600 ~/.ssh/id_rsa

### Personalize Git

Label your commits with your name.

    (vm) $ git config --global user.name "Your Name Here"
    
Git saves your email address into the commits you make. GitHub uses the email address to associate your commits with your GitHub account.

    (vm) $ git config --global user.email "your_email@youremail.com"

### From Here

#### Syndb and migrate, first you'll have to move into _/vagrant/myproject/_. 

    (vm) $ cd /vagrant/myproject/
    (vm) $ dj syncdb
    (vm) $ dj migrate
    
If you've installed Django Grappelli you will also have to ``collectstatic``.
    
    (vm) $ dj collectstatic

#### Run server

##### Port Forwarding

The Vagrantfile forwards port 8000 on the virtual environment to port 8001 on the host. In order to access the site in a browser on the host when you execute `$ runserver` on the virtual environment, you need to add a port configuration to the runserver command:

    python manage.py runserver [::]:8000

[Chef-Cookbook-DjangoNewProj](https://github.com/jbergantine/chef-cookbook-djangonewproj/) sets up a [bash alias](#django) to avoid keyboard fatigue when running this command:

    (vm) $ rs

#### Watch for changes to SASS Stylesheets

    (vm) $ cw

Note that you will likely want to have both runserver and compass watch running at the same time so you can review your changes in a web browser. To avoid having to open two SSH sessions into Vagrant you can run both with Foreman:

    (vm) $ foreman start -f Procfile.dev

That's a lot to remember so there's a shortcut for it:

    (vm) $ frs

### Update the newly created settings files

This project utilizes separate settings files for development and production that both inherit from a common base file. The following is a list of things that need to be configured. If you're not ready to deploy the site you can just edit the development settings in the _development.py_ file for the time being and come back to the production settings in the _production.py_ file later.

* Set `ADMINS` and `MANAGERS` for both local and production.
* Set `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` values for both local and production.
* Set all `DATABASES` settings for production.
* Set `MEDIA_ROOT`, `MEDIA_URL`, and `STATIC_ROOT` for production.
* Set production `CACHES`.
* Change your `TIME_ZONE` if desired.
    
### Update the newly created fabfile.py

**This can be put off until you are ready to deploy the site to your production environment.**

* Configure the environments and default call to Python as described in the Configuration notes within the file. Read the full configuration and usage notes to understand how the fabfile works with the production environment.

### Update the [500 Error template](#500html)

* Replace `[email address]` (2 occurrences) with an email address for the system administrator.

### Update the [base template](#basehtml)

* There are numerous things to update and customize here including the Google Analytics account number, default Facebook Graph API data, creating the favicon and Apple Touch icons and putting them in the locations referenced, TypeKit script files, the name of the site in the `<title>` tag and site meta data.

### Share

Freeze the requirments

    (vm) $ pip freeze > requirements/development.txt

Add a Git remote per the instructions at BitBucket or GitHub or whatever remote hosting service for adding an existing repo. Add and push.

    (vm) $ git remote add origin <path to repo>
    (vm) $ git add -A
    (vm) $ git commit -am "<commit message>"
    (vm) $ git push origin master
    
Your teammates will now be able to pull down the repo and setup their own Vagrant virtual environment. [Point them to the instructions for using it](#using-a-vagrant-virtual-environment-that-has-been-shared-with-you).

## Using a Vagrant Virtual Environment That Has Been Shared With You

### Clone the project from GitHub or Bitbucket or wherever it is hosted onto your host machine and change directory into the new directory.

    (host) $ git clone <path_to_repo>
    (host) $ cd <path_to_cloned_repo>

### Install the cookbooks.

    (host) $ git submodule init
    (host) $ git submodule update

### Boot up the Vagrant vitual environment

    (host) $ vagrant up

### SSH into the Vagrant virtual environment

    (host) $ vagrant ssh

### Install the project-specific packages

    (vm) sudo pip install -r requirements/development.txt
    
If this fails, the person sharing the environment with you probably forgot to [freeze the requirements](#share).

### Sync the database and migrate any migrations. Collectstatic.

    (vm) $ dj syncdb
    (vm) $ dj migrate
    (vm) $ dj collectstatic

### Setup or copy over SSH keys.

Follow the directions [here](#setup-ssh-keys).

### Personalize Git.

Follow the directions [here](#personalize-git).

### Begin editing, pushing, pulling, etc.

* [Run Server](#run-server)
* [Run Compass Watch](#watch-for-changes-to-sass-stylesheets)

# Deploying to a WebFaction Instance

[Signup for a WebFaction hosting account on the WebFaction website](http://www.webfaction.com?affiliate=kinsa). Once you're signed up login to the control panel with your username and password.

## Setup Databases

In the WebFaction control panel navigate to _Databases_. Create a PostgreSQL database for the project. Make a note of the _database name_, _user_ and _password_ for later.

## Setup the mod_wsgi Application

In the WebFaction control panel navigate to _Domains/Websites_ and then _Applications_. Create a *mod_wsgi* type app for the site using Python 2.7 along with whatever version of mod_wsgi is available for that version of Python.


## Setup Static Media Applications

In the WebFaction control panel navigate to _Domains/Websites_ and then _Applications_. Create a _Static_ type app for static media and a _Static type app for dynamic media. Name the static media app 'static' and the dynamic media app 'media'. Choose an _App type_ of _Static only (no .htaccess)_ and enter _expires max_ into _Extra info_ for both apps.

_If the app isn't named static, a symlink app can serve as a go-between to still use `/static` as the URL for the app. This is kind of weird. An example would be the where the static app is named `awesomesite_static` and has a path on the server of `/home/awesomesiteuser/webapps/awesomesite_static/` and the `awesomesite_static_symlink` app serves as a symlink to `/home/awesomesiteuser/webapps/awesomesite_static/static/` in which case the symlink app gets the url of `/static` when setting up the Website in the WebFaction control panel (as opposed to the actual static app which doesn't get it's own URL)._

## Create the 'Website'

In the WebFaction control panel navigate to _Domains/Websites_ and then _Websites_. Click _Add new website_, give it a name and a domain then from _Add an application_ choose _Reuse an existing application_. Pick your mod_wsgi application from the list and leave the URL empty, click Save. Follow that same method for choosing your static media application, entering a URL of `static` and your dynamic media application, entering a URL of `media`. Save the website.

## Add your SSH key to the WebFaction Server

This makes it so you don't have to continuously input our password when connecting over SSH.

### Copy the key to your WebFaction account

	(vm) $ scp ~/.ssh/id_rsa.pub <accountname>@<accountname>.webfactional.com:temp_id_rsa_key.pub 

When prompted, enter your password.

### Open an SSH session to your account

	(vm) $ ssh <accountname>@<accountname>.webfactional.com 

When prompted, enter your password.

### Create ~/.ssh

	(webfaction) $ mkdir -p $HOME/.ssh

### Add your key to the authorized_keys file

	(webfaction) $ cat ~/temp_id_rsa_key.pub >> ~/.ssh/authorized_keys 

### Remove the temporary key file 

	(webfaction) $ rm ~/temp_id_rsa_key.pub 

### Secure the SSH keys

	(webfaction) $ chmod 600 ~/.ssh/authorized_keys 

### Secure the SSH directory

	(webfaction) $ chmod 700 ~/.ssh 

### Close the SSH session

	(webfaction) $ exit


### Verify that your key works properly. Open an SSH session to your account, you shouldn't be prompted for your password this time

	(vm) $ ssh <accountname>@<accountname>.webfactional.com 

#### Close the SSH session

	(webfaction) $ exit

## Install necessary modules

**Note: use ``python2.7`` to run all commands instead of just `python` or `./`.**

### SSH into your account

	(vm) $ ssh <accountname>@<accountname>.webfactional.com 

Then run:

	(webfaction) $ mkdir -p ~/lib/python2.7
	(webfaction) $ easy_install-2.7 pip 


### Install VirtualEnv and VirtualEnvWrapper

Check whether `virtualenv` and `virtualenvwrapper` are installed, run the following and look for them in the output:

	(webfaction) $ pip freeze

If so, carry on, if not:

	(webfaction) $ pip install virtualenv

If you have to install Virtualenvwrapper, it has to be installed from source ([ref](http://community.webfaction.com/questions/10316/pip-install-virtualenvwrapper-not-working)). The latest version at the time of documentation is 4.1.1… check the list at [https://pypi.python.org/packages/source/v/virtualenvwrapper/]() to verify that before proceeding:

	(webfaction) $ mkdir -p ~/bin ~/lib/python2.7 ~/src
	(webfaction) $ cd ~/src
	(webfaction) $ ln -s $HOME/lib/python2.7 $HOME/lib/python
	(webfaction) $ wget http://pypi.python.org/packages/source/v/virtualenvwrapper/virtualenvwrapper-4.1.1.tar.gz --no-check-certificate
	(webfaction) $ tar zxf virtualenvwrapper-4.1.1.tar.gz
	(webfaction) $ cd virtualenvwrapper-4.1.1
	(webfaction) $ PYTHONPATH=$HOME/lib/python2.7 python2.7 setup.py install --home=$HOME
	(webfaction) $ rm $HOME/lib/python

### Edit the `~/.bashrc` file to reference the virtualenvs 

	(webfaction) $ nano ~/.bashrc

Append at the end:

	export WORKON_HOME=$HOME/.virtualenvs 
	export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7 
	source /home/<accountname>/bin/virtualenvwrapper.sh 
	
If you're on a CentOS 6 machine (your WebFaction server number is >Web300) also add the following ([ref](http://community.webfaction.com/questions/7714/installing-psycopg2-pg_config-missing)):

	export PATH=/usr/pgsql-9.1/bin:$PATH

Exit and save.
 
#### Source the `~/.bashrc` file to load it

	(webfaction) $ source ~/.bashrc


### Configure PIL 

PIP installation of PIL doesn't work so well on WebFaction. (From [http://community.webfaction.com/questions/7340/how-to-install-pil-with-truetype-support]().)

	(webfaction) $ mkdir -p ~/src ~/lib/python2.7
	(webfaction) $ cd ~/src
	(webfaction) $ wget http://effbot.org/media/downloads/PIL-1.1.7.tar.gz
	(webfaction) $ tar zxf PIL-1.1.7.tar.gz
	(webfaction) $ cd PIL-1.1.7

edit PIL's setup.py to set the library pointers as follows:

	# --------------------------------------------------------------------
	# Library pointers.
	#
	# Use None to look for the libraries in well-known library locations.
	# Use a string to specify a single directory, for both the library and
	# the include files.  Use a tuple to specify separate directories:
	# (libpath, includepath).  Examples:
	#
	# JPEG_ROOT = "/home/libraries/jpeg-6b"
	# TIFF_ROOT = "/opt/tiff/lib", "/opt/tiff/include"
	#
	# If you have "lib" and "include" directories under a common parent,
	# you can use the "libinclude" helper:
	#
	# TIFF_ROOT = libinclude("/opt/tiff")

	TCL_ROOT = None
	JPEG_ROOT = '/usr/lib64','/usr/include'
	ZLIB_ROOT = '/lib64','/usr/include'
	TIFF_ROOT = None
	FREETYPE_ROOT = '/usr/lib64','/usr/include/freetype2/freetype'
	LCMS_ROOT = None

build PIL with the following command:

	(webfaction) $ python2.7 setup.py build_ext -i
	
run the test to confirm that the build was successful:

	(webfaction) $ python2.7 selftest.py
	
should return:

	--------------------------------------------------------------------
	PIL 1.1.7 TEST SUMMARY 
	--------------------------------------------------------------------
	Python modules loaded from ./PIL
	Binary modules loaded from ./PIL
	--------------------------------------------------------------------
	--- PIL CORE support ok
	--- TKINTER support ok
	--- JPEG support ok
	--- ZLIB (PNG/ZIP) support ok
	--- FREETYPE2 support ok
	--- LITTLECMS support ok
	--------------------------------------------------------------------

install the library:

	(webfaction) $ python2.7 setup.py install

### Create the virtualenv

	(webfaction) $ mkdir -p ~/.virtualenvs/ 
	(webfaction) $ mkvirtualenv <envname>
	(webfaction) $ workon <envname> && cdvirtualenv
	(webfaction) $ add2virtualenv .

### Correct the permissions for the media app

	(webfaction) $ chmod 755 ~/webapps/<dynamic_media_application_name>

### Edit the .wsgi file

Create a wsgi file in the mod_wsgi application:

	$ nano ~/webapps/<wsgi_application_name>/<wsgi_application_name>.wsgi

Edit it to include:

	#!/usr/bin/python 
	import os
	import site
	import sys  

	# Tell wsgi to add the Python site-packages to it's path. 
	site.addsitedir('/home/<accountname>/.virtualenvs/<envname>/lib/python2.7/site-packages')  

	# Fix markdown.py (and potentially others) using stdout 
	sys.stdout = sys.stderr  

	# Append the Django project to the path. 
	sys.path.append('/home/<accountname>/.virtualenvs/<envname>/<django_project_name>')  

	# On Django 1.4 projects settings now lives in an application (generally named myproject) within the project (also named myproject) so this should be 'myproject.settings.production', on older Django installations (Django 1.3 say) this should just be 'settings'
	os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings.production' 
	from django.core.handlers.wsgi import WSGIHandler 
	application = WSGIHandler()  

### Edit the apache config file

	$ nano ~/webapps/<wsgi_application_name>/apache2/conf/httpd.conf

Comment out the `DirectoryIndex` and `DocumentRoot` lines.

At the bottom of the file, add the following where port number is the port number assigned for the mod_wsgi application (which can be found by selecting the mod\_wsgi application from the list of Applications in the WebFaction Control Panel under Domains/Websites):

	NameVirtualHost *:<port_number>
	<VirtualHost *:<port_number>>
	    ServerName <domain_name.com>
	    ServerAlias www.<domain_name.com> <alternate_domain_name.com>
	    WSGIScriptAlias / /home/<accountname>/webapps/<wsgi_application_name>/<wsgi_application_name>.wsgi
	</VirtualHost>

#### (Optional) Configure Domain Aliases

Make sure that the Apache rewrite_module is being loaded, there should be a line at the top that looks like:

	LoadModule rewrite_module modules/mod_rewrite.so

In the `VirtualHost`, before the closing tag (`</VirtualHost>`), add the following:

Turn on the RewriteEngine:

	RewriteEngine On

Send access attempts to 'www' to the domain without that subdomain (make sure that 'www.domainname.tld' is setup under the domains tab of the WebFaction Domains control panel and is pointed at the app). Replace `domainname.tld` with the real domain name and top level domain:

	RewriteCond %{HTTP_HOST} ^www.domainname.tld$ [NC]
	RewriteRule ^(.*)$ http://domainname.tld$1 [R=301,L]

Point an alternate domain at our domain (make sure that 'www.otherdomainname.tld' and 'otherdomainname.tld' are setup under the domains tab of the WebFaction Domains control panel and are pointed at the app). Replace `otherdomainname.tld` with the other domain name and top level domain and replace `domainname.tld` with the primary domain name and top level domain:

	RewriteCond %{HTTP_HOST} ^otherdomainname.tld$ [NC]
	RewriteRule ^(.*)$ http://domainname.tld$1 [R=301,L]

	RewriteCond %{HTTP_HOST} ^www.otherdomainname.tld$ [NC]
	RewriteRule ^(.*)$ http://domainname.tld$1 [R=301,L]

#### Reboot Apache

Verify that works by rebooting (site won't load yet, need to do a deploy, but restart should go without errors).

	(webfaction) $ ~/webapps/<wsgi_application_name>/apache2/bin/restart

### (Optional) .htpasswd protect site

From [http://httpd.apache.org/docs/2.0/howto/auth.html]() AND [http://community.webfaction.com/questions/256/apache-basic-authentication-for-mod_wsgi-inc-django-applications]():

Make a directory to store the .htapasswd files:

	(webfaction) $ mkdir -p /home/<username>/webapps/<webapp name>/apache2/passwd

Create the .htpasswd file (which in this case is a file called 'passwords' using the htpasswd command:

	(webfaction) $ htpasswd -c /home/<username>/webapps/<webapp name>/apache2/passwd/passwords <htpasswd user's username>

Edit the httpd.conf file to include the necessary lines:

	(webfaction) $ nano /home/<username>/webapps/<webapp name>/apache2/conf/httpd.conf

And append:

	LoadModule auth_basic_module modules/mod_auth_basic.so
	LoadModule authn_file_module modules/mod_authn_file.so
	LoadModule authz_user_module modules/mod_authz_user.so
	<Location />
		AuthType Basic
		AuthName "Authentication Required"
		AuthUserFile /home/<username>/webapps/<webapp name>/apache2/passwd/passwords
		Require valid-user
	</Location>

Restart the server:

	$ /home/<username>/webapps/<webapp name>/apache2/bin/restart

### Schedule a Regular Database Backup

From [http://docs.webfaction.com/user-guide/databases.html]().

	(webfaction) $ nano ~/.pgpass

Add a new line containing the following, where `database_name` is the name of the database as it appears on the control panel, `database_user` is the user you created for the database and `password` is the database password:

	*:*:database_name:database_user:password

Secure the ~/.pgpass file. 

	(webfaction) $ chmod 600 ~/.pgpass

Create a directory to store the database backups. 

	(webfaction) $ mkdir -p ~/db_backups

Edit your crontab:

	(webfaction) $ crontab -e

To include, replacing `databaseUser` with the user you created for the database and `databaseName` with the name of the database (occurs multiple times). Adjust the frequency as desired. This will backup the database once a day at 0800 UTC (or whatever the system clock is set to).:

	0 8 * * * /usr/local/pgsql/bin/pg_dump -Ft -b -U databaseUser databaseName | gzip -9 > $HOME/db_backups/databaseName-`date +\%Y\%m\%d`.sql.gz 2>> $HOME/db_backups/backups.log && echo "Database backup completed successfully on `date`" >> $HOME/db_backups/backups.log

**NOTE:** If the above line executes when run directly in the Bash shell but not when executed via crontab, the leading cause is the escaping of the timestamp. So, if it is not working, try unescaping the timestamp by removing the backslashes.

### Configure memcached

Based on: [http://docs.webfaction.com/software/memcached.html](), [http://docs.webfaction.com/software/django/config.html#django-memcached](), [http://forum.webfaction.com/viewtopic.php?pid=2311](), and [http://docs.webfaction.com/software/python.html#installing-packages-with-setup-py]().

_A supposedly much faster alternative to python-memcached is pylibmc. I have yet to figure out how to install it though._

Make sure not to be in a virtual environment:

	(webfaction) $ deactivate

Create `~/src` if it doesn't exist yet:

	(webfaction) $ mkdir -p ~/src

Install and configure:

	(webfaction) $ cd ~/src
	(webfaction) $ wget ftp://ftp.tummy.com//pub/python-memcached/python-memcached-1.48.tar.gz
	(webfaction) $ tar -xzvf python-memcached-1.48.tar.gz
	(webfaction) $ cd python-memcached-1.48
	(webfaction) $ python2.7 setup.py build
	(webfaction) $ python2.7 setup.py install --home=$HOME

Enable memcached as a daemon (defaults to using 64mb of memory; run `memcached -h` for optional configuration parameters including the amount of memory to use)

	(webfaction) $ memcached -d -s ~/memcached.sock

Establish that memcached is running (where `username` is your WebFaction account username):

	(webfaction) $ ps -u username -o pid,command | grep memcached

### Close the SSH session

	(webfaction) $ exit

## Edit the project's environmental settings file

In `settings/<environment name>.py`, update the following configuration variables, replacing <accountname> with your WebFaction account name and <url> with your website's URL (including any variants such as _accountname.webfaction.com_):

	MEDIA_ROOT = '/home/<accountname>/webapps/<dynamic_media_app_name>/'
	MEDIA_URL = '/media/'

	STATIC_ROOT = '/home/<accountname>/webapps/<static_media_app_name>/'
	STATIC_URL = '/static/'

	ADMIN_MEDIA_PREFIX = '/static/admin/'
	
	ALLOWED_HOSTS = [<url>]

	CACHES = {
    	'default': {
        	'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
	        'LOCATION': 'unix://unix:/home/<username>/memcached.sock',
    	}
	}

## Edit the project's fab file

In `fabfile.py`, in the environment you are configuring (probably `production` but possibly `staging` or something else) replace `<accountname>` with your WebFaction account name, `<envname>` with your virtualenv name, `<wsgi_application_name>` with the name of the WSGI application you created and adjust the name of the `env.remote_static_root` as necessary based on the name of the static app created. In the `production()` method update the following variables:

	env.apache_restart_command = '/home/<accountname>/webapps/<wsgi_application_name>/apache2/bin/restart'
	env.hosts = ['<accountname>@<accountname>.webfactional.com']
	env.password = '<password>'
	env.virtualenv_name = '<envname>'
	env.path = '/home/<accountname>/.virtualenvs/<virtualenv_name>'
	env.remote_media_root = '/home/<accountname>/webapps/media'
	env.remote_static_root = '/home/<accountname>/webapps'

## Setup the environment on the server and do an initial deployment

Replace `<environemnt name>` with the name of the environment as configured in `fabfile.py`, probably `production`.

	(vm) $ fab <environment name> remote_setup
	
### Freeze production requirements

	(vm) $ sudo pip freeze > requirements/<environment name>.txt
	(vm) $ git add requirements/<environment name>.txt
	(vm) $ git commit requirements/<environment name>.txt -m "adding <environment name> requirements"

### Deploy

	(vm) $ fab <environment name> deploy

_Watch the output the first time debugging. If PIL installs without libjpeg support, follow these directions: [http://community.webfaction.com/questions/7340/how-to-install-pil-with-truetype-support]()._

# Documentation

## Dependencies

Dependencies not listed below include cookbooks as referenced in the [Vagrant file](https://gist.github.com/3875868).

### Gists referenced in this project's readme

* [Vagrant File](https://gist.github.com/3875868)

### Cookbooks

Some of the recipes referred to in the [Vagrant file](https://gist.github.com/jbergantine/3875868) are tied together via the recipe in [chef-cookbook-djangonewproj](https://github.com/jbergantine/chef-cookbook-djangonewproj).

### Gists referenced in chef-cookbook-djangonewproj

* [Bash Profile with Coloring and Git Knowledge](https://gist.github.com/jbergantine/7363927)
* [Custom Build of Modernizr.js](https://gist.github.com/jbergantine/3868451/)
* [Git Post-Merge Hook](https://gist.github.com/jbergantine/3870080/)

## Installed Files

This template includes a number of HTML templates and template tags as well as other things.

### Git Hooks Created

#### post-merge

[View source.](https://gist.github.com/3870080)

A hook that runs every time a merge is made. A merge will happen every time `$ git pull` is executed (and there are changes to be brought in; it won't happen if there are no changes) in addition to the explicit `$ git merge` command. This hook will compile stylesheets, sync and migrate the database and install new requirements if _requirements/development.txt_ is updated. This hook lives in _.git/hooks/post-merge_ and can be disabled by either removing the _post-merge_ file or making it non-executable. If you want to use Scout to compile SASS or use Tower or a similar application to manage Git you will want to disable or remove this hook as it relies on the presence of SASS, Compass, Susy, Django and a database among other things.

### HTML Templates Created

#### 404.html

A default 404-type error page. Required for production deployment.

#### 500.html

A default 500-type error page. Required for production deployment.

#### __default.html

A default template to base other templates off of. Loads _base.html_ and includes all the customizable blocks from that template. Copy this when creating new pages. eg:

    $ cp __default.html home.html

#### _form_snippet.html

An include for forms that creates properly-semantically-structured forms. To use it, include it within the body of a form like so:

    <form action="" method="post">
        {% csrf_token %}
        {% include "_form_snippet.html" %}
        <div>
            <input type="submit" value="Submit" id="submit" />
        </div>
    </form>

#### _nav.html

Global site nav. Built as an include to be placed on the header or footer of the site depending on whether the site is being viewed on a mobile device or not.

#### base.html

The basis to inherit all other templates off of. A responsive-design (mobile) friendly HTML5 template. Sitewide stylesheets and script files are referenced in the appropriate places and wrapped in django-compressor to minimize page load times. This template also includes Google Analytics, default meta data and Facebook Graph API data for page sharing purposes as well as a link to a favicon and Apple Touch icons for Web application development purposes.

### JavaScript Files Created

When you run the script to create the project, the script downloads the latest version of jQuery (which is then referenced both locally and via Google's AJAX load in base.html) as well as a [customized basic version of modernizr.js](https://gist.github.com/3868451) which includes only the shims for the HTML5 doctype.

### Stylesheets Created

This project utilizes the [Compass](http://compass-style.org) [SASS](http://sass-lang.com) framework and [Susy responsive grid plugin](http://susy.oddbird.net/) and creates a stylesheet directory following the requirements of that application. CSS files will be created in the appropriate spots the first time you run either `$ compass watch static_media/stylesheets` or `$ compass compile static_media/stylesheets`. The [bash shortcut `cw`](#compass) is set up to reduce keyboard fatigue. 

#### _base.sass, screen.sass, print.sass

[Documentation for these files is contained in the Gesso project repo](https://github.com/jbergantine/compass-gesso#included-files).

#### ie.sass

A stylesheet specifically for dealing with modifications necessary for Internet Explorer. Meant to be used in a way that styles defined here override _screen.sass_.

### Template Tags Installed

#### fetch_content, nav, widont, dumbquotes, dumbpunct

[Documentation for these template tags is contained in a seperate repo](https://github.com/jbergantine/django-templatetags/blob/master/README.rst#usage).

### current_site_url

[Documentation for this template tag is contained in a seperate repo](https://github.com/jbergantine/django-robots/blob/master/README.rst#template-tags-installed).

### Fabfile

This project includes a default fabfile, the primary use of which is deploying changes to a remote server or servers. The file is broken into "public" and "private" methods which can be bundled into custom commands or expanded on. The public methods are [documented](#fabric-command-tips) below.

#### Configuration

Setup the necessary environments. The framework for the first, production() is sketched out in _fabfile.py_, just fill in the blanks. 

The Fabfile uses `python2.7` as the default call to Python on the server. If the server uses `python` or `python2.6` or `python3` or `py`, find and replace all the instances of `python2.7` with whatever your server uses.

The Fabfile assumes that the Python environment on the server is defined using VirtualEnv and VirtualEnvWrapper and that a virtual environment has already been created for the project on the server.

#### Usage Notes

##### Setup the necessary directories on the server (1-time only)

This file assumes that the directories referenced in _fabfile.py_ for the environment as `env.path`, `env.remote_media_root` and `env.remote_static_root` have already been created (that is to say, you've configured a virtual environment on the remote server and setup static media hosting).

    $ fab <environment> remote_setup

If there are no other environment's defined, the default is _production_. As in:

    $ fab production remote_setup

##### Deploy

**Before deploying make sure that any extra software such as a database (PostgreSQL presumably), memcached, Xapian, etc. are installed and setup.**

Upload the first set of files, install python packages, sync and migrate databases:

    $ fab <environment> deploy

``$ fab <environment> deploy`` runs the following tasks:

1. Compiles SASS for production
1. Collects Python packages to _requirements/production.txt_
1. Collects static files into the _static_ files directory on the remote server
1. Uploads the latest version of the project from the local Git repository to the remote server
1. Installs packages from _requirements/production.txt_ on the remote server
1. Migrates and syncs the database(s) on the remote server
1. Restarts apache on the remote server
1. Removes legacy production deployments to keep only the latest (5) versions on the remote server

``$ fab production deploy`` will be the command you will most frequently run going forward.

For documentation on the other commands bundeled into the fabfile see the [Fabric Cheat Sheet](#fabric-command-tips).

# Cheat Sheets

## Vagrant command tips

### To exit the VM and return to your host machine:

    (vm) $ exit

### To shutdown the VM:

    (host) $ vagrant halt

### To suspend the VM (i.e. freeze the VM's state):

    (host) $ vagrant suspend

### Once shutdown or suspended, a VM can be restarted. To boot a VM:

    (host) $ vagrant up

### SSH into a VM (VM must [first be booted](#once-shutdown-or-suspended-a-vm-can-be-restarted)):

    (host) $ vagrant ssh
    
### To destroy the VM:

    (host) $ vagrant destroy

### To check if the VM is currently running:

    (host) $ vagrant status

### To re-run the provisioning after the VM has been started (if you have built the VM from scratch):

    (host) $ vagrant provision

More information is available in the [Vagrant documentation](http://vagrantup.com/v1/docs/index.html).

## VirtualenvWrapper Command Tips

Replacing `<virtualenv_name>` with the name of the virtual environement (IE: `djangoproj`).

### To make a virtual environment:

    (vm) $ mkvirtualenv <virtualenv_name>

### To activate a virtual environment:

    (vm) $ workon <virtualenv_name>
   
### To deactivate a virtual environment:

    (vm) $ deactivate
    
### To remove a virtual environment (warning this will delete the environment and any files therein):

    (vm) rmvirtualenv <virtualenv_name>
    
## PIP Command Tips

### List intalled packages

    (vm) $ pip freeze
    
The output of this command can be routed to a file as in:

    (vm) $ pip freeze > <path_to_file>
    
As in:

    (vm) $ pip freeze > requirements.txt
    
### Install a new package:
 
    (vm) $ pip install <package_name>
    
### Upgrade a package that is alrady installed:

    (vm) $ pip install <package_name> --upgrade
    
### Install a specific version of a package (where x.x.x is the version number):

    (vm) $ pip install <package_name>==x.x.x
    
### Install all the packages listed in a file:

    (vm) pip install -r <path_to_file>
    
As in:

    (vm) $ pip install -r requirements.txt
    
### Uninstall a package:

    (vm) $ pip uninstall <package_name>

## Fabric command tips

The following commands reference `<environment>` which is the name of the environment defined in _fabfile.py_. If no adjustments are made this will be `production`. You may define alternate environments (for example `staging`) by duplicating the `production()` method.

### Setup the server:

The following command make the _packages_ and _releases_ directories on the remote server and set permissions on the _media_ directory to allow Django to write to it. This must be the first fabric command you run and won't be run again.

    (vm) $ fab <environment> remote_setup

### Deploy:

First make sure that you have committed all your changes to the repository. **Uncommitted changes will not be collected for deployment.**

    (vm) $ fab <environment> deploy

### To restart Apache on the server:

    (vm) $ fab <environment> restart_server

### To load a fixture:

Before running the following, commit the fixture to the repo and run a `deploy` to upload the fixture to the remote server. Once the fixture is in place on the remote run the following. You will be prompted to name the fixture you want to load.

    (vm) $ fab <environment> load_data

### To simutaniously deploy and load_data:

    (vm) $ fab <environment> deploy_and_loaddata

### To export the remote database and copy it locally (to be then manually loaded):

    (vm) $ fab <environment> grab_data

## Django Extensions

### TimeStampledModel

Django Extensions includes a [TimeStampledModel](https://github.com/django-extensions/django-extensions/blob/master/django_extensions/db/models.py) class which classes can be inherited from.

The TimeStampledModel class adds `created` and `modified` date time fields and sets the ordering to `('-modified', '-created')`.

#### Usage:

    from django_extensions.db.models import TimeStampedModel

    class foo(TimeStampedModel):
        ...

### runserver_plus

`runserver_plus` is a shell command for interactive debugging. [More info](http://packages.python.org/django-extensions/runserver_plus.html).

### shell_plus

`shell_plus` is a shell command that expands on `$ ./manage.py shell` by dynamically reloading models.

### reset_db

`reset_db` is a shell command to reset the database.

### More Commands and Other Features

See the [documentation](http://packages.python.org/django-extensions/command_extensions.html) or read the [source code](https://github.com/django-extensions/django-extensions).
    
## Bash Aliases

The following bash aliases are added to the shell. 

### Compass

<table>
    <tr>
        <th>$ cw</th>
        <td><pre>compass watch myproject/static_media/stylesheets</pre></td>
    </tr>
</table>

### Django

<table>
    <tr>
        <th>$ dj</th>
        <td>
            <pre>python manage.py</pre>
            <p>Example usage, interact with the Django shell:</p>
            <pre>dj shell</pre>
        </td>
    </tr>
</table>
<table>
    <tr>
        <th>$ rs</th>
        <td>
            <pre>python manage.py runserver [::]:8000</pre>
            <p>This is necessary to enable port forwarding from the virtual machine to the host. In a host the site will now be available at http://127.0.0.1:8001.</p>
        </td>
    </tr>
    <tr>
        <th>$ rsp</th>
        <td>
            <pre>python manage.py runserver_plus [::]:8000</pre>
            <p>Instigates django-extension's <a href="http://packages.python.org/django-extensions/runserver_plus.html">RunServerPlus</a> command with proper port forwarding. In a host the site will now be available at http://127.0.0.1:8001.</p>
        </td>
    </tr>
    <tr>
        <th>$ sh</th>
        <td><pre>python manage.py shell</pre></td>
    </tr>
    <tr>
        <th>$ frs</th>
        <td>
            <pre>foreman start -f Procfile.dev</pre>
            <p>Simutaniously starts <code>compass watch myproject/static_media/stylesheets</code> and <code>python manage.py runserver [::]:8000</code> so stylesheets can be compiled and the server run from the same SSH session without manually managing processes.</p>
        </td>
    </tr>
</table>

### Git

<table>
    <tr>
        <th>$ git br</th>
        <td><pre>git branch</pre></td>
    </tr>
    <tr>
        <th>$ git ci</th>
        <td><pre>git commit</pre></td>
    </tr>
    <tr>
        <th>$ git co</th>
        <td><pre>git checkout</pre></td>
    </tr>
    <tr>
        <th>$ git last</th>
        <td><pre>git log -1 HEAD</pre></td>
    </tr>
    <tr>
        <th>$ git st</th>
        <td><pre>git status</pre></td>
    </tr>
    <tr>
        <th>$ git unstage</th>
        <td><pre>git reset HEAD --</pre></td>
    </tr>
</table>
<table>
    <tr>
        <th>$ ga</th>
        <td><pre>git add</pre></td>
    </tr>
    <tr>
        <th>$ gb</th>
        <td><pre>git branch</pre></td>
    </tr>
    <tr>
        <th>$ gco</th>
        <td><pre>git checkout</pre></td>
    </tr>
    <tr>
        <th>$ gl</th>
        <td><pre>git pull</pre></td>
    </tr>
    <tr>
        <th>$ gp</th>
        <td><pre>git push</pre></td>
    </tr>
    <tr>
        <th>$ gst</th>
        <td><pre>git status</pre></td>
    </tr>
    <tr>
        <th>$ gss</th>
        <td><pre>git status -s</pre></td>
    </tr>
</table>

### Python

<table>
    <tr>
        <th>$ py</th>
        <td>
            <pre>python</pre>
            <p>Launches a Python interactive shell.</p>
        </td>
    </tr>
    <tr>
        <th>$ pyclean</th>
        <td>
            <pre>find . -name "*.pyc" -delete</pre>
            <p>Removes all files ending in ".pyc".</p>
        </td>
    </tr>
</table>
