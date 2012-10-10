# Vagrant

Vagrant offers the ability to create unique virtual machines on a per-project basis. Using Vagrant you can install system-level libraries without conflicting with other projects and share virtual machines with others on your team so you're all using the same thing.

These instructions go through the configuration of a new Ubuntu 64-bit operating system on a Vagrant Box hosted on an Apple Macintosh computer.

Using the Vagrant box requires you to compile SASS, push and pull from Git, and interact with manage.py from within the virtual environment although you can use a text editor or IDE of your choice for editing on your host system via a shared folder and you can access the site through a web browser of your choice by taking advantage of port forwarding between the virtual environment and the host. Additional details on shared folders and port forwarding are provided in the setup instructions.

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

It sets up a new project called myproject in a virtual environment named djangoproj and connects that to a PostgreSQL database called django_db.

## Legend

`(host)` is for commands to run on the host machine, and `(vm)` is
for commands to run inside the VM.

## Initial setup of Vagrant Base

Download virtualbox from http://www.virtualbox.org/wiki/Downloads, install dmg.

Download vagrant from http://downloads.vagrantup.com/, install dmg.

Launch a terminal window, check that it installed:

    (host) $ which vagrant

Add a vagrant box (we'll be using Ubuntu Precise Pangolin (12.04 LTS) 64-bit):

    (host) $ vagrant box add precise64 http://files.vagrantup.com/precise64.box
    
## Using Vagrant for projects

Make a directory for the project and change to it, replacing <path_to> with the path to the project and <project_name> with the name of the project.

    (host) $ mkdir <path_to>/<project_name> && cd $_
    
For example, to create a project called 'website' in your home directory:

    (host) $ mkdir ~/website && cd $_

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

## This Template

To start a new project with this template, execute:

    django-admin.py startproject --template=https://github.com/jbergantine/django-newproj-template/zipball/master --extension=py,rst <project_name>