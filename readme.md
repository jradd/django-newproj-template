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

Vagrant offers the ability to create unique virtual machines on a per-project basis. Using Vagrant you can install system-level libraries without conflicting with other projects and share virtual machines with others on your team so you're all using the same thing. Because of the way Vagrant works you can continue to edit files in your editor of choice on your host machine (TextMate, Coda, Dreamweaver, Sublime, whatever) and view the site in a variety of browsers (Firefox, Chrome, the iPhone Emulator's Safari browser, etc.).

These instructions go through the configuration of a new Ubuntu 64-bit operating system on a Vagrant Box hosted on an Apple Macintosh computer with Git and Curl as a minimum. These same set of instructions should work on a Linux box with a similar configuration.

## This Project

### You will be using Django within a [Virtual Environemnt](https://pypi.python.org/pypi/virtualenv) managed by [PIP](https://pypi.python.org/pypi/pip), associated with a PostgreSQL database.

This template sets up a number of defaults for `django-admin.py startproject` by making a number of assumptions about your preferences, application choices, encouraging a particular development environment configuration and by loading in an initial set of templates, and if used as intended, CSS files and JavaScript libraries.

On the virtual machine, a new Django project called _myproject_ is created in a virtual environment named _djangoproj_.

Using the Vagrant box requires you to interact with Django's management command (`$ python manage.py`) [from within the virtual machine](#django).

This project configures your Django project for use with a PostgreSQL database, _django\_db_, which it installs along with a user, _django\_login_, for said database and installs [South](https://pypi.python.org/pypi/South) for database migrations.

### You will be using Git for Version Control.

This configuration uses a [post-merge Git hook](#post-merge) to sync/migrate the database and compile SASS when pulling changes in from others, as such, it is strongly recommended that you execute Git commands within the virtual environment using the command line rather than using applications installed on the host machine such as Tower or GitHub App. 

### You will be using separate settings files for development and production.

This template sets up separate development (the Django project running only on your local computer) and production (the Django project running on the world wide web) settings files that inherit from a common base settings file.

This project configures [postactivate](https://github.com/jbergantine/chef-cookbook-djangonewproj/blob/master/recipes/default.rb#L119) and [postdeactivate](https://github.com/jbergantine/chef-cookbook-djangonewproj/blob/master/recipes/default.rb#L120) virtualenv hooks for specifying the proper settings file when working in the virtual environment within Vagrant for development so the `--settings=` flag doesn't need to be explicitly used. Something similar will need to be done in production to [specify the settings file to use](https://docs.djangoproject.com/en/dev/topics/settings/#designating-the-settings).

### You will be developing for use on multiple devices.

This project configures the project for use with [django-mobile](https://pypi.python.org/pypi/django-mobile/) and [django-responsive](https://github.com/mlavin/django-responsive) for doing server-level device and width detection.

This project installs [django-floppyforms](https://pypi.python.org/pypi/django-floppyforms) to take advantage of HTML5 form fields to greatly enhance the mobile user experience.

By default the [_base.html_](#basehtml) template has an HTML5 doctype. For backwards compatibility this project installs [modernizr.js](http://modernizr.com) with an HTML5 shiv for older versions of Internet Explorer to keep them from puking. 

This project installs [SASS along with Compass and Susy responsive grids](#stylesheets-created) and begins sketching in styles with [Gesso](https://github.com/jbergantine/compass-gesso). 

### Your site will be optimized for search engines.

This template includes a sitemaps module, _sitemaps.py_, which is initially configured to create a sitemaps XML file referencing "static" pages of a site but which can be expanded to most any application. The sitemap module is imported into _urls.py_ which sets up routing. 

This template also installs [Django-Robots](https://github.com/jbergantine/django-robots), a small app for creating a _robots.txt_ file.

### You will be using Fabric for deployment.

This project installs [Fabric](https://pypi.python.org/pypi/Fabric/) and includes a [fabfile](#fabfile) with a number of pre-configured methods for deployment and server management.

### Optionally, you will be using Xapian for plain text search.

This project installs Xapian with Python bindings. You will have to additionally install the [_django-haystack_](https://pypi.python.org/pypi/django-haystack/) and [_xapian-haystack_](https://pypi.python.org/pypi/xapian-haystack) Python packages and [configure the project as appropriate](http://django-haystack.readthedocs.org/en/latest/tutorial.html#configuration).

### Optionally, you will be using memcached for caching.

This project installs memcached and Python bindings and configures the development environment (in _myproject/settings/development.py_) to use memcached. The production environment settings file includes the necessary config for memcached but commented out since the production environment will need to have memcached installed onto the server with Python bindings in order for that to work.

### Optionally, you will be using PIL and possibly SORL-Thumbnail.

This project installs the necessary libraries (libjpeg, libfreetype, zlib) to use PIL (you will have to still install the [_pil_](https://pypi.python.org/pypi/PIL) Python package, however). To use SORL-Thumbnail you will have to install the [_pil_](https://pypi.python.org/pypi/PIL) and [_sorl-thumbnail_](https://pypi.python.org/pypi/sorl-thumbnail/) Python packages and [configure the project as appropriate](http://sorl-thumbnail.readthedocs.org/en/latest/installation.html#setup).

### Other applications

Review _requirements/base.txt_ for other default Python application choices and [Additional Optional Installs](#additional-optional-installs) for how to install other Linux packages such as Redis, Erlang and RabbitMQ.

# Directions

## Legend

`(host)` is for commands to run on the host machine, and `(vm)` is
for commands to run inside the Vagrant virtual machine.

## Initial setup of Vagrant Base

This step only ever needs to be done once. Once the precise64 box is installed on a system the remaining steps refer to that same box regardless of the project.

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

When you're all done, this directory will contain a directory named _myproject_ that matches up with _/vagrant/myproject_ in the virtual envirionment. Virtualbox keeps the two directories in sync so changes to one will be made in the other. This directory contains Django's _manage.py_ file as well as the project's fabfile and PIP requirements doc. Within it is a second _myproject_ directory which contains the Django project. On your host launch the text editor of your choice (Panic Coda, TextMate, Sublime, whatever), make edits to any of these files and those edits will be reflected in the virtual environment immediately.

Create a place for the Chef cookbooks. From within the Vagrant project directory on the host run the following command.

So, extending our example, this would be run from within _~/website/_.

    (host) $ git init
    (host) $ mkdir cookbooks

Clone the Chef cookbooks repositories as needed (we will use the following cookbooks in this guide). 

    (host) $ git submodule add git://github.com/opscode-cookbooks/apt.git cookbooks/apt
    (host) $ git submodule add git://github.com/opscode-cookbooks/build-essential.git cookbooks/build-essential
    (host) $ git submodule add git://github.com/opscode-cookbooks/sudo.git cookbooks/sudo
    (host) $ git submodule add git://github.com/opscode-cookbooks/git.git cookbooks/git
    (host) $ git submodule add git://github.com/opscode-cookbooks/openssl.git cookbooks/openssl
    (host) $ git submodule add git://github.com/opscode-cookbooks/postgresql.git cookbooks/postgresql
    (host) $ git submodule add git://github.com/opscode-cookbooks/python.git cookbooks/python
    (host) $ git submodule add git://github.com/opscode-cookbooks/zlib.git cookbooks/zlib
    (host) $ git submodule add git://github.com/opscode-cookbooks/memcached.git cookbooks/memcached
    (host) $ git submodule add git://github.com/jbergantine/chef-cookbook-python-psycopg2.git cookbooks/chef-cookbook-python-psycopg2
    (host) $ git submodule add git://github.com/jbergantine/chef-cookbook-libjpeg.git cookbooks/chef-cookbook-libjpeg
    (host) $ git submodule add git://github.com/jbergantine/chef-cookbook-libfreetype.git cookbooks/chef-cookbook-libfreetype
    (host) $ git submodule add git://github.com/jbergantine/chef-cookbook-xapian.git cookbooks/chef-cookbook-xapian
    (host) $ git submodule add git://github.com/jbergantine/chef-cookbook-djangonewproj.git cookbooks/chef-cookbook-djangonewproj


Init and update the submodules.

    (host) $ git submodule init
    (host) $ git submodule update

Copy in the Vagrantfile.
    
    (host) $ curl https://raw.github.com/gist/3875868/gistfile1.rb > Vagrantfile
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

    (vm) $ cd ~/.ssh

Create the key, replacing your_email@youremail.com with your email address:

    (vm) $ ssh-keygen -t rsa -C “your_email@youremail.com”
    
When prompted with "Enter file in which to save the key (/home/vagrant/.ssh/id_rsa):" hit the return key to accept the default value.

When prompted for a passphrase enter a strong passphrase and hit the return key or hit the return key to create a key without a passphrase. 

Print the public key to the terminal window. The following will spit out about 5 lines of text beginning with "ssh-rsa" and ending with your email address. Once you've ran the following command, select all of its output with your mouse and copy it (Command + C should do it to copy it).

    (vm) $ cat id_rsa.pub
    
Now login to GitHub or Bitbucket or whatever service you're using for Git and add a new key for your account, pasting in the public key from your clipboard. You should now be able to push, pull and clone without having to enter a passphrase for the account (if you set a passphrase for the key you will have to enter that). 

#### Copying Your Keys Into the Virtual Environment

SSH into the virtual box. From the project directory (the one you made in [using the new Vagrant Base Box](#using-the-new-vagrant-base-box)) on your host system run:

    (host) $ vagrant up
    (host) $ vagrant ssh

Open the _id_rsa.pub_ file on the virtual box for editing.

    (vm) $ vi ~/.ssh/id_rsa.pub

Copy the public key in a new Terminal window:

    (host) $ cat ~/.ssh/id_rsa.pub|pbcopy

Return to vi on the Virtual Machine. Paste, save and quit vi. If you're unfamiliar with vi/vim commands type or press the following keys/combos one line at a time:

    i
    cmd + v
    esc
    :wq

Open the _id_rsa_ file on the virtual box for editing. In the Terminal window that is SSH'd into the virtual box run:

    (vm) $ vi ~/.ssh/id_rsa

Copy the private key. In the Terminal window on your host machine run:

    (host) $ cat ~/.ssh/id_rsa|pbcopy
    
Return to vi on the Virtual Machine. Paste, save and quit vi. If you're unfamiliar with vi/vim commands type or press the following keys/combos one line at a time:

    i
    cmd + v
    esc
    :wq

Change permissions of the _id_rsa_ file.

    (vm) $ chmod 600 ~/.ssh/id_rsa

### Personalize Git

Label your commits with your name.

    (vm) $ git config --global user.name "Your Name Here"
    
Git saves your email address into the commits you make. GitHub uses the email address to associate your commits with your GitHub account.

    (vm) $ git config --global user.email "your_email@youremail.com"

### From Here

#### Syndb and migrate, first you'll have to move into _/vagrant/myproject/_. Then `collectstatic` for Django Grappelli.

    (vm) $ cd /vagrant/myproject/
    (vm) $ dj syncdb
    (vm) $ dj migrate
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

# Documentation

## Dependencies

This is a developer reference only to make sure that changes made to this project are referenced in its support files that are not directly included with the project. Dependencies not listed below include cookbooks as referenced in the [Vagrant file](https://gist.github.com/3875868).

### Gists referenced in this project's readme

* [Vagrant File](https://gist.github.com/3875868)

### Cookbooks

Some of the recipes referred to in the [Vagrant file](https://gist.github.com/3875868) are tied together via the recipe in [chef-cookbook-djangonewproj](https://github.com/jbergantine/chef-cookbook-djangonewproj).

### Gists referenced in chef-cookbook-djangonewproj

* [Bash Profile with Coloring and Git Knowledge](https://gist.github.com/4004242/)
* [Custom Build of Modernizr.js](https://gist.github.com/3868451/)
* [Git Post-Merge Hook](https://gist.github.com/3870080/)

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

This project utilizes the [Compass](http://compass-style.org) [SASS](http://sass-lang.com) framework and [Susy respoonsive grid plugin](http://susy.oddbird.net/) and creates a stylesheet directory following the requirements of that application. CSS files will be created in the appropriate spots the first time you run either `$ compass watch static_media/stylesheets` or `$ compass compile static_media/stylesheets`. The [bash shortcut `cw`](#compass) is set up to reduce keyboard fatigue. 

#### _base.sass, screen.sass, print.sass

[Documentation for these files is contained in the Gesso project repo](https://github.com/jbergantine/compass-gesso#included-files).

#### ie.sass

A stylesheet specifically for dealing with modifications necessary for Internet Explorer. Meant to be used in a way that styles defined here override _screen.sass_.

### Template Tags Installed

#### fetch_content, nav, widont

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

### Once shutdown or suspended, a VM can be restarted:

    (host) $ vagrant up

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
        <th>cw</th>
        <td><pre>compass watch myproject/static_media/stylesheets</pre></td>
    </tr>
</table>

### Django

<table>
    <tr>
        <th>dj</th>
        <td>
            <pre>python manage.py</pre>
            <p>Example usage, interact with the Django shell:</p>
            <pre>dj shell</pre>
        </td>
    </tr>
</table>
<table>
    <tr>
        <th>rs</th>
        <td>
            <pre>python manage.py runserver [::]:8000</pre>
            <p>This is necessary to enable port forwarding from the virtual machine to the host. In a host the site will now be available at http://127.0.0.1:8001.</p>
        </td>
    </tr>
    <tr>
        <th>rsp</th>
        <td>
            <pre>python manage.py runserver_plus [::]:8000</pre>
            <p>Instigates django-extension's <a href="http://packages.python.org/django-extensions/runserver_plus.html">RunServerPlus</a> command with proper port forwarding. In a host the site will now be available at http://127.0.0.1:8001.</p>
        </td>
    </tr>
    <tr>
        <th>sh</th>
        <td><pre>python manage.py shell</pre></td>
    </tr>
    <tr>
        <th>frs</th>
        <td>
            <pre>foreman start -f Procfile.dev</pre>
            <p>Simutaniously starts <code>compass watch myproject/static_media/stylesheets</code> and <code>python manage.py runserver [::]:8000</code> so stylesheets can be compiled and the server run from the same SSH session without manually managing processes.</p>
        </td>
    </tr>
</table>

### Git

<table>
    <tr>
        <th>br</th>
        <td><pre>branch</pre></td>
    </tr>
    <tr>
        <th>ci</th>
        <td><pre>commit</pre></td>
    </tr>
    <tr>
        <th>co</th>
        <td><pre>checkout</pre></td>
    </tr>
    <tr>
        <th>st</th>
        <td><pre>status</pre></td>
    </tr>
</table>
<table>
    <tr>
        <th>ga</th>
        <td><pre>git add</pre></td>
    </tr>
    <tr>
        <th>gb</th>
        <td><pre>git branch</pre></td>
    </tr>
    <tr>
        <th>gco</th>
        <td><pre>git checkout</pre></td>
    </tr>
    <tr>
        <th>gl</th>
        <td><pre>git pull</pre></td>
    </tr>
    <tr>
        <th>gp</th>
        <td><pre>git push</pre></td>
    </tr>
    <tr>
        <th>gst</th>
        <td><pre>git status</pre></td>
    </tr>
    <tr>
        <th>gss</th>
        <td><pre>git status -s</pre></td>
    </tr>
</table>

### Python

<table>
    <tr>
        <th>py</th>
        <td>
            <pre>python</pre>
            <p>Launches a Python interactive shell.</p>
        </td>
    </tr>
    <tr>
        <th>pyclean</th>
        <td>
            <pre>find . -name "*.pyc" -delete</pre>
            <p>Removes all files ending in ".pyc".</p>
        </td>
    </tr>
</table>
