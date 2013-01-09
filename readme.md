# Django New Project Template

Django project template for starting a new project.

## Table of Contents

### Introduction

* [Stop](#stop)
* [This Template](#this-template)
* [Vagrant](#vagrant)
* [Assumptions](#assumptions)

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
    * [TemplateTags](#templatetags-installed)
    * [Fabfile](#fabfile)

### Cheat Sheets

* [Vagrant Command Tips](#vagrant-command-tips)
* [VirtualenvWrapper Command Tips](#virtualenvwrapper-command-tips)
* [PIP Command Tips](#pip-command-tips)
* [Fabric Command Tips](#fabric-command-tips)
* [Django Extensions](#django-extensions)
* [Bash Aliases](#bash-aliases)

# Introduction

## Stop

This project assumes at least a passing familiarity with Django and the Terminal window. If you haven't done so, it is highly recommended that those unfamiliar with the Terminal window begin with [The Designer's Guide to the OSX Command Prompt](http://wiseheartdesign.com/articles/2010/11/12/the-designers-guide-to-the-osx-command-prompt/) and those unfamiliar with Django [read through the tutorial](https://docs.djangoproject.com/en/1.4/intro/tutorial01/) to understand some of the concepts discussed below.

## This Template

To start a new project with this template, execute:

    django-admin.py startproject --template=https://github.com/jbergantine/django-newproj-template/zipball/master --extension=py,rst <project_name>

However, this template is intended to be used in conjunction with Vagrant as part of a broader project as documented in the [Usage](#initial-setup-of-vagrant-base) directions below.

## Vagrant

Vagrant offers the ability to create unique virtual machines on a per-project basis. Using Vagrant you can install system-level libraries without conflicting with other projects and share virtual machines with others on your team so you're all using the same thing.

These instructions go through the configuration of a new Ubuntu 64-bit operating system on a Vagrant Box hosted on an Apple Macintosh computer with Git and Curl as a minimum. These same set of instructions should work on a Linux box with a similar configuration.

Using the Vagrant box requires you to interact with _manage.py_ from within the virtual environment but then allows you to use the text editor or IDE of your choice for editing on your host system via a shared folder and allows access to a compiled site through the web browser of your choice by taking advantage of port forwarding between the virtual environment and the host.

This configuration uses a [post-merge Git hook](#post-merge) to sync/migrate the database and compile SASS, as such managing Git must be done within the virtual environment as well rather than through the Tower or GitHub apps for example on the host. For simplicity sake it is recommended that SASS stylesheets be compiled within the virtual environment and a [shortcut is added to the bash profile to help facilitate this](#compass) as well rather than using an app like Scout on the host.

The [Vagrantfile](https://gist.github.com/3875868) configures a virtual environment to include:

* Python 2.7.3
* PIP
* Virtualenv
* VirtualenvWrapper
* Postgres 9.1
* Git
* libfreetype
* libjpeg
* zlib
* Xapian

Additionally, the Vagrantfile installs the recipes from a Chef Cookbook [(Chef-Cookbook-DjangoNewProj)](https://github.com/jbergantine/chef-cookbook-djangonewproj) intended to be used with this project which sets up a new Django project called _myproject_ in a virtual environment named _djangoproj_ and connects that to a PostgreSQL database called _django_db_.

## Assumptions

This template sets up a number of defaults for `django-admin.py startproject` by making a number of assumptions about your preferences, application choices, encouraging a particular dev environment configuration and by loading in an initial set of templates, and if used as intended, CSS files and JavaScript libraries.

### You will be using Git for Version Control.

This should be obvious by now. 

### You will be using VirtualEnv and PIP.

These are defacto standards for Python development. Virtualenv allows you to have multiple versions of packages installed on one machine which it collects into sets called "virtual environments". PIP is a package manager for installing, updating and removing packages.

### You will be using separate settings files for development and production.

This template sets up separate development and production settings files that inherit from a common base settings file.

Chef-Cookbook-DjangoNewProj configures postactivate and postdeactivate virtualenv hooks for specifying the proper settings file when working in the virtual environment within Vagrant for development so the `--settings=` flag doesn't need to be explicitly used. Something similar will need to be done in production.

### You will be using PostgreSQL as your database and South for database migrations.

This settings files in this template are explicitly configured to connect to a PostgreSQL server.

Chef-Cookbook-DjangoNewProj configures your Django project for use with a PostgreSQL database, _django\_db_, which it installs along with a user, _django\_login_, for said database and installs South for database migrations.

### Your site will be optimized for search engines.

This template includes a sitemaps module, _sitemaps.py_, which is initially configured to create a sitemaps XML file referencing "static" pages of a site but which can be expanded to most any application. The sitemap module is imported into _urls.py_ which sets up routing. 

This template also installs [Django-Robots](https://github.com/jbergantine/django-robots), a small app for creating a _robots.txt_ file.

### You will be developing for use on multiple devices.

The settings file in this template reference [django_mobile](https://github.com/gregmuellegger/django-mobile) middleware and templatetags to do device detection for making server or template-level modifications on a platform or device level.

Chef-Cookbook-DjangoNewProj installs [django-floppyforms](https://github.com/brutasse/django-floppyforms) to take advantage of HTML5 form fields to greatly enhance the mobile user experience.

### You will be using Fabric for deployment.

This template includes a fabfile with a number of pre-configured methods for deployment and server management.

### You will be using an HTML5 Doctype and writing your stylesheets with SASS

By default the [_base.html_](#basehtml) template has an HTML5 doctype. For backwards compatibility Chef-Cookbook-DjangoNewProj installs [modernizr.js](http://modernizr.com) with an HTML5 shiv for older versions of Internet Explorer to keep them from puking. Finally, Chef-Cookbook-DjangoNewProj installs [and configures](#stylesheets-created) Compass to instantiate the Compass [`+global-reset` mixin](http://compass-style.org/reference/compass/reset/utilities/#mixin-global-reset) which resets HTML5 element's display-roles for older browsers.

### Optionally, you will be using Xapian for plain text search.

Chef-Cookbook-DjangoNewProj installs Xapian with Python bindings. You will have to additionally install the _django-haystack_ and _xapian-haystack_ Python packages and configure the project to use this.

### Optionally, you will be using PIL and possibly SORL-Thumbnail.

Chef-Cookbook-DjangoNewProj installs the necessary libraries (libjpeg, libfreetype, zlib) to use PIL (you will have to still install the _pil_ Python package, however). To use SORL-Thumbnail you will have to install the _pil_ and _sorl-thumbanil_ Python packages and configure the project as appropriate.

### Other applications

Review _requirements/base.txt_ for other default application choices.

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
    (host) $ git submodule add git://github.com/opscode-cookbooks/git.git cookbooks/git
    (host) $ git submodule add git://github.com/opscode-cookbooks/openssl.git cookbooks/openssl
    (host) $ git submodule add git://github.com/opscode-cookbooks/postgresql.git cookbooks/postgresql
    (host) $ git submodule add git://github.com/opscode-cookbooks/python.git cookbooks/python
    (host) $ git submodule add git://github.com/opscode-cookbooks/zlib.git cookbooks/zlib
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

### Setup SSH Keys

Using SSH keys makes pushing and pulling changes from Bitbucket or GitHub or the server a lot easier since you will only have one password to remember. 

#### Copy in Existing Keys

If you are already using SSH keys on your host machine you can copy those keys into the Vagrant virtual box. Alternately, [you can create them from scratch](#setup-new-keys).

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

#### Setup new Keys

If you aren't using SSH keys on your host machine, you can setup a new key on your virtual box. These same instructions can be used on your host machine to generate SSH keys. Just execute them on host instead of the virtual box, skipping the step where you SSH into the virtual box.

SSH into the box if you aren't already, from the project directory (the one you made in [using the new Vagrant Base Box](#using-the-new-vagrant-base-box)) on your host system run:

    (host) $ vagrant up
    (host) $ vagrant ssh
    
Move into the _~/.ssh_ directory:

    (vm) $ cd ~/.ssh

Create the key, replacing your_email@youremail.com with your email address:

    (vm) $ ssh-keygen -t rsa -C “your_email@youremail.com”
    
When prompted with "Enter file in which to save the key (/home/vagrant/.ssh/id_rsa):" hit the return key to accept the default value.

When prompted for a passphrase enter a strong passphrase and hit the return key or hit the return key to create a key without a passphrase. 

Print the public key to the terminal window. The following will spit out about 5 lines of text beginning with "ssh-rsa" and ending with your email address. Once you've ran the following command, select all of its output with your mouse and copy it (Command + C should do it to copy it).

    (vm) $ cat id_rsa.pub
    
Now login to GitHub or Bitbucket or whatever service you're using for Git and add a new key for your account, pasting in the public key from your clipboard. You should now be able to push, pull and clone without having to enter a passphrase for the account (if you set a passphrase for the key you will have to enter that). 

### Personalize Git

Label your commits with your name.

    (vm) $ git config --global user.name "Your Name Here"
    
Git saves your email address into the commits you make. GitHub uses the email address to associate your commits with your GitHub account.

    (vm) $ git config --global user.email "your_email@youremail.com"

### Update the newly created settings files

This project utilizes separate settings files for development and production that both inherit from a common base file.

* Set `ADMINS` and `MANAGERS` for both local and production.
* Set `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` values for both local and production.
* Set all `DATABASES` settings for production.
* Set `MEDIA_ROOT`, `MEDIA_URL`, and `STATIC_ROOT` for production.
* Set production `CACHES`.
* Change your `TIME_ZONE` if desired.
    
### Update the newly created fabfile.py

* Configure the environments and default call to Python as described in the Configuration notes within the file. Read the full configuration and usage notes to understand how the fabfile works with the production environment.

### Update the [500 Error template](#500html)

* Replace `[email address]` (2 occurrences) with an email address for the system administrator.

### Update the [base template](#basehtml)

* There are numerous things to update and customize here including the Google Analytics account number, default Facebook Graph API data, creating the favicon and Apple Touch icons and putting them in the locations referenced, TypeKit script files, the name of the site in the `<title>` tag and site meta data.

### From Here

If you've been configuring your SSH Keys, you may need to move back to _/vagrant/_ before continuing.

    (vm) $ cd /vagrant/

Additionally, make sure you're working on the _djangoproj_ virtual environment. You should be able to see this in the terminal prompt. It should look like:

    (djangoproj)vagrant@precise64:/vagrant/myproject$

The bit in parens at the beginning is the name of the virtual environment (_djangoproj_). It is followed by the current user (_vagrant_), the name of the host (_precise64_) and the current directory (_/vagrant/myrpoject_). If you're not working on the _djangoproj_ project, run the following virtualenvwrapper command to instantiate it:

    (vm) $ workon djangoproj

#### Syndb and migrate, first you'll have to move into _/vagrant/myproject/_.

    (vm) $ cd /vagrant/myproject/
    (vm) $ dj syncdb
    (vm) $ dj migrate

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

#### Share

Freeze the requirments

    (vm) $ pip freeze > requirements/development.txt

Add a Git remote per the instructions at BitBucket or GitHub or whatever remote hosting service for adding an existing repo. Add and push.

    (vm) $ git remote add origin <path to repo>
    (vm) $ git add -A
    (vm) $ git commit -am "<commit message>"
    (vm) $ git push origin master
    
Your teammates will now be able to pull down the repo and setup their own Vagrant virtual environment. [Point them to the instructions for using it](#using-a-vagrant-virtual-environment-that-has-been-shared-with-you).

## Using a Vagrant Virtual Environment That Has Been Shared With You

* [Before you do anything else, STOP](#stop).
* [Read about Vagrant](#vagrant).
* [Read the assumptions of use](#assumptions).
* [See the Legend for the following directions](#legend).

### Clone the project from GitHub or Bitbucket or wherever it is hosted onto your host machine and change directory into the new directory.

    (host) $ git clone <path_to_repo>
    (host) $ cd $_

### Install the cookbooks.

    (host) $ git submodule init
    (host) $ git submodule update

### Boot up the Vagrant vitual environment

    (host) $ vagrant up

### SSH into the Vagrant virtual environment

    (host) $ vagrant ssh

### Install the project-specific packages

    (vm) sudo pip install -r requirements/development.txt

### Sync the database and migrate any migrations.

    (vm) $ dj syncdb
    (vm) $ dj migrate

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

The other recipes are tied together via the recipe in [chef-cookbook-djangonewproj](https://github.com/jbergantine/chef-cookbook-djangonewproj).

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

This project utilizes the [Compass](http://compass-style.org) [SASS](http://sass-lang.com) framework and creates a stylesheet directory following the requirements of that application. CSS files will be created in the appropriate spots the first time you run either `$ compass watch static_media/stylesheets` or `$ compass compile static_media/stylesheets`. The [bash shortcut `cw`](#compass) is set up to reduce keyboard fatigue. 

#### _base.sass, screen.sass, print.sass

[Documentation for these files is contained in a seperate repo](https://github.com/jbergantine/compass-gesso#included-files).

#### ie.sass

A stylesheet specifically for dealing with modifications necessary for Internet Explorer. Meant to be used in a way that styles defined here override _screen.sass_.

### TemplateTags Installed

#### fetch_content, nav, widont

[Documentation for these files is contained in a seperate repo](https://github.com/jbergantine/django-templatetags/blob/master/README.rst#usage).

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
            <p>Instigates django-extension's (RunServerPlus)[http://packages.python.org/django-extensions/runserver_plus.html] command with proper port forwarding. In a host the site will now be available at http://127.0.0.1:8001.</p>
        </td>
    </tr>
    <tr>
        <th>sh</th>
        <td><pre>python manage.py shell</pre></td>
    </tr>
</table>

### Foreman

<table>
    <tr>
        <th>frs</th>
        <td><pre>foreman start -f Procfile.dev</pre></td>
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
