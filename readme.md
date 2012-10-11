# Django New Project Template

Django project template for starting a new project.

## This Template

To start a new project with this template, execute:

    django-admin.py startproject --template=https://github.com/jbergantine/django-newproj-template/zipball/master --extension=py,rst <project_name>

However, this template is intended to be used in conjunction with Vagrant.

## Assumptions

This template sets up a number of defaults for ``django-admin.py startproject`` by making a number of assumptions about your preferences, application choices, encouraging a particular dev environment configuration and by loading in an initial set of templates, and if used as intended, CSS files and JavaScript libraries.

### You will be using seperate settings files for development and production.

This template sets up seperate development and production settings files that inherit from a common base settings file.

[Chef-Cookbook-DjangoNewProj](https://github.com/jbergantine/chef-cookbook-djangonewproj) configures postactivate and postdeactivate virtualenv hooks for specifying the proper settings file when working in the virtual environment within Vagrant for development so the ``--settings=`` flag doesn't need to be explicitly used. Something similar will need to be done in production.

### You will be using PostgreSQL as your database.

This settings files in this template are explicitly configured to connect to a PostgreSQL server.

[Chef-Cookbook-DjangoNewProj](https://github.com/jbergantine/chef-cookbook-djangonewproj) configures your Django project for use with a PostgreSQL database and installs South for database migrations.

### You will be using SASS with the Compass and Susy frameworks.

[Chef-Cookbook-DjangoNewProj](https://github.com/jbergantine/chef-cookbook-djangonewproj) installs the Compass and Susy frameworks and [lays down a primer coat to build off of](https://github.com/jbergantine/compass-gesso).

### Your site will be optimized for search engines.

This template includes a sitemaps module (``sitemaps.py``) which is initially configured to create a sitemaps XML file referencing "static" pages of a site but which can be expanded to most any application. The sitemap module is imported into ``urls.py`` which sets up routing. 

This template also installs [Django-Robots](https://github.com/jbergantine/django-robots), a small app for creating a robots.txt file.

### You will be developing for use on multiple devices.

The settings file in this template reference [django_mobile](https://github.com/gregmuellegger/django-mobile) middleware and templatetags to do device detection for making server or template-level modifications on a platform or device level.

[Chef-Cookbook-DjangoNewProj](https://github.com/jbergantine/chef-cookbook-djangonewproj) installs [django-floppyforms](https://github.com/brutasse/django-floppyforms) to take advantage of HTML5 form fields to greatly enhance the mobile user experience.

### You will be using Fabric for deployment.

This template includes a fabfile with a number of pre-configured methods for deployment and server management.

### Other applications

Review ``stable-req.txt`` for other default applicaiton choices.

## Vagrant

Vagrant offers the ability to create unique virtual machines on a per-project basis. Using Vagrant you can install system-level libraries without conflicting with other projects and share virtual machines with others on your team so you're all using the same thing.

These instructions go through the configuration of a new Ubuntu 64-bit operating system on a Vagrant Box hosted on an Apple Macintosh computer.

Using the Vagrant box requires you to interact with _manage.py_ from within the virtual environment although you can use a text editor or IDE of your choice for editing on your host system via a shared folder and you can access the site through a web browser of your choice by taking advantage of port forwarding between the virtual environment and the host.

This configuration uses a [post-merge Git hook](https://github.com/jbergantine/chef-cookbook-djangonewproj#post-merge) to sync/migrate the database and compile SASS, as such managing Git must be done within the virtual environment as well. For simplicity sake it is recommended that SASS stylesheets be compiled within the virtual environment and a [shortcut is added to the bash profile to help facilitate this](https://github.com/jbergantine/chef-cookbook-djangonewproj#compass).

The Vagrantfile configures a virtual environment to include:

* Python 2.7.3
* PIP
* Virtualenv
* VirtualenvWrapper
* Postgres 9.1
* Git
* Vim
* libjpeg
* zlib
* freetype
* Xapian

Additionally, the Vagrantfile calls on a [Cookbook](https://github.com/jbergantine/chef-cookbook-djangonewproj) intended to be used with this project which sets up a new Django project called _myproject_ in a virtual environment named _djangoproj_ and connects that to a PostgreSQL database called _django_db_.

## Legend

`(host)` is for commands to run on the host machine, and `(vm)` is
for commands to run inside the VM.

## Initial setup of Vagrant Base

This step only ever needs to be done once. Once the precise64 box is installed on a system the remaining steps refer to that same box regardless of the project.

Download virtualbox from http://www.virtualbox.org/wiki/Downloads, install dmg.

Download vagrant from http://downloads.vagrantup.com/, install dmg.

Launch a terminal window, check that it installed:

    (host) $ which vagrant

Add a vagrant box (we'll be using Ubuntu Precise Pangolin (12.04 LTS) 64-bit):

    (host) $ vagrant box add precise64 http://files.vagrantup.com/precise64.box
    
## Usage

Make a directory for the project and change to it, replacing <path_to> with the path to the project and <project_name> with the name of the project.

    (host) $ mkdir <path_to>/<project_name> && cd $_
    
For example, to create a project called 'website' in your home directory:

    (host) $ mkdir ~/website && cd $_

When you're all done, this directory will contain a directory named _djangoproj_ that matches up with `/vagrant/.virutalenvs/djangoproj` in the virtual envirionment. Virtualbox keeps the two directories in sync so changes to one will be made in the other.

Init the Vagrant instance, install the [vagrant-vbguest](https://github.com/dotless-de/vagrant-vbguest) plugin and start up the Vagrant instance.

    (host) $ vagrant init precise64
    (host) $ vagrant gem install vagrant-vbguest
    
Create a place for the Chef cookbooks. From within the base directory run:
    
    (host) $ mkdir cookbooks && cd $_

Clone the Chef cookbooks repositories as needed (we will use the following cookbooks in this guide)

    (host) $ git clone git://github.com/opscode-cookbooks/apt.git
    (host) $ git clone git://github.com/opscode-cookbooks/build-essential.git
    (host) $ git clone git://github.com/opscode-cookbooks/git.git
    (host) $ git clone git://github.com/opscode-cookbooks/openssl.git
    (host) $ git clone git://github.com/opscode-cookbooks/vim.git
    (host) $ git clone git://github.com/opscode-cookbooks/postgresql.git
    (host) $ git clone git://github.com/opscode-cookbooks/python.git
    (host) $ git clone git://github.com/opscode-cookbooks/zlib.git
    (host) $ git clone git://github.com/jbergantine/chef-cookbook-libjpeg.git
    (host) $ git clone git://github.com/jbergantine/chef-cookbook-libfreetype.git
    (host) $ git clone git://github.com/jbergantine/chef-cookbook-xapian.git
    (host) $ git clone git://github.com/jbergantine/chef-cookbook-djangonewproj.git

Startup Vagrant:

    (host) $ vagrant up

Provision Vagrant (install all those cookbooks):

    (host) $ vagrant provision
    
SSH in to the virtualbox:

    (host) $ vagrant ssh 
    
Verify installation of Python 2.7.3:

    (vm) $ python -V
    Python 2.7.3

Verify that PostgreSQL was installed correctly by logging into the psql shell and then exiting (if it was installed and configured correctly the following should happen without errors):

    (vm) $ psql -h localhost -U postgres --password
    (vm) $ thisisapassword
    (vm) postgres=# \q
    
Verify the installation of Xapian with Python bindings by attempting an import (if it installed successfully it should return without errors):

    (vm) $ python -c "import xapian"
    
Verify the installation of Compass and Susy by verifying their existance in the gem list (if they installed correctly their name and a version number should be returned):

    (vm) $ gem list | grep compass
    (vm) $ gem list | grep susy

### Setup SSH Keys

Creating keys makes pushing and pulling changes from Bitbucket or GitHub or the server a lot easier since you will only have one password to remember. 

SSH into the box, from the project directory (the one you made in [using the new Vagrant Base Box](#using-the-new-vagrant-base-box)) on your host system run:

    (host) $ vagrant up
    (host) $ vagrant ssh
    
Move into the ``~/.ssh`` directory:

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

This project utilizes seperate settings files for development and production that both inherit from a common base file.

* Set ``ADMINS`` and ``MANAGERS`` for both local and production.
* Set ``EMAIL_HOST``, ``EMAIL_HOST_USER``, ``EMAIL_HOST_PASSWORD``, ``DEFAULT_FROM_EMAIL`` values for both local and production.
* Set all ``DATABASES`` settings for production.
* Set ``MEDIA_ROOT``, ``MEDIA_URL``, and ``STATIC_ROOT`` for production.
* Set production ``CACHES``. (Unless edited out, the default-requirments file installs the necessary Python modules to utilize Memcached on the server but the exact location etc. of that needs to be set here.)
* Change your ``TIME_ZONE`` if desired.
    
### Update the newly created fabfile.py

* Configure the environments and default call to Python as described in the Configuration notes within the file. Read the full configuration and usage notes to understand how the fabfile works with the production environment.

### Update the [500 Error template](#500html)

* Replace ``[email address]`` (2 occurrences) with an email address for the system administrator.

### Update the [base template](#basehtml)

* There are numerous things to update and customize here including the Google Analytics account number, default Facebook Graph API data, creating the favicon and Apple Touch icons and putting them in the locations referenced, TypeKit script files, the name of the site in the ``<title>`` tag and site meta data.

### Stylesheets, JavaScript files, Bash aliases and Git Hooks

If used as intended with Vagrant see the various files and shortcuts created by the [Chef-Cookbook-DjangoNewProj](https://github.com/jbergantine/chef-cookbook-djangonewproj/blob/master/README.md)

## Port Forwarding

The Vagrantfile forwards port 8000 on the virtual environment to port 8001 on the host. In order to access the site in a browser on the host from ``runserver`` on the virtual environment you need to add a port configuration to the command:

    python manage.py runserver [::]:8000

[Chef-Cookbook-DjangoNewProj](https://github.com/jbergantine/chef-cookbook-djangonewproj/) sets up a [bash alias](https://github.com/jbergantine/chef-cookbook-djangonewproj/blob/master/README.md#django) to avoid keyboard fatigue when running this command.

## Installed Files

This template includes a number of HTML templates and template tags.

### Templates Created

#### 404.html

A default 404-type error page. Required for production deployment.

#### 500.html

A default 500-type error page. Required for production deployment.

#### __default.html

A default template to base other templates off of. Loads ``base.html`` and includes all the customizable blocks from that template. Copy this when creating new pages. eg:

    $ cp __default.html home.html

#### _form_snippet.html

An include for forms that creates properly-semantically-structured forms.

#### _nav.html

Global site nav. Built as an include to be placed on the header or footer of the site depending on whether the site is being viewed on a mobile device or not.

#### base.html

The basis to inherit all other templates off of. A responsive-design (mobile) friendly HTML5 template. Sitewide stylesheets and script files are referenced in the appropriate places and wrapped in django-compressor to minimize page load times. This template also includes Google Analytics, default meta data and Facebook Graph API data for page sharing purposes as well as a link to a favicon and Apple Touch icons for Web application development purposes.

### TemplateTags Installed

#### fetch_content

Returns a specific number of entries for a particular model. (If the model is sorted by date published they will be sorted that way hence the name get_latest_content.)

Example usage:

    {% load fetch_content %}
    {% get_latest_content application_name.model_name 5 as foo %}
    {% for bar in foo %}
        {{ bar.attribute }}
    {% endfor %}

Can also be used to return all entries for a particular model.

Example usage:
	
	{% load fetch_content %}
	{% get_all_content application_name.model_name as foo %}
	{% for bar in foo %}
		{{ bar.attribute }}
	{% endfor %}

#### nav

Handles navigation item selection.

Example usage:

    {# Set up the variable for use across context-stacking tags #}
    {% nav %} or {% nav for mynav %}
    
    {# Set the context so {{ nav.home }} (or {{ mynav.home }}) is True #}
    {% nav "home" %} or {% nav "home" for mynav %}

The most basic (and common) use of the tag is to call ``{% nav [item] %}``,
where ``[item]`` is the item you want to check is selected.

By default, this tag creates a ``nav`` context variable. To use an
alternate context variable name, call ``{% nav [item] for [var_name] %}``.

To use this tag across ``{% block %}`` tags (or other context-stacking
template tags such as ``{% for %}``), call the tag without specifying an
item.

Your HTML navigation template should look something like:

    {% block nav %}
    <ul class="nav">
        <li{% if nav.home %} class="selected"{% endif %}><a href="/">Home</a></li>
        <li{% if nav.about %} class="selected"{% endif %}><a href="/about/">About</a></li>
    </ul>
    {% endblock %}

To override this in a child template, you'd do:

    {% include "base.html" %}
    {% load nav %}

    {% block nav %}
    {% nav "about" %}
    {{ block.super }}
    {% endblock %}

This works for multiple levels of template inheritance, due to the fact
that the tag only does anything if the ``nav`` context variable does not
exist. So only the first ``{% nav %}`` call found will ever be processed.

To create a sub-menu you can check against, dot-separate the item:

    {% nav "about_menu.info" %}

This will be pass for both ``{% if nav.about_menu %}`` and
``{% if nav.about_menu.info %}``.

#### widont Filter

_From: http://djangosnippets.org/snippets/17/_

"Widows" are single words that end up on their own line, thanks to automatic line-breaks. This is an no-no in graphic design, and is especially unsightly in headers and other short bursts of text. This filter automatically replaces the space before the last word of the passed value with a non-breaking space, ensuring there is always at least two words on any given line. Usage is like so:

    {{ blog.entry.headline|widont }}

## Vagrant command tips

### To exit the VM and return to your host machine:

    (vm) $ exit

### To shutdown the VM, type:

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