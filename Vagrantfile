# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.define :djangovm do |cfg|
    # Every Vagrant virtual environment requires a box to build off of.
    cfg.vm.box = "precise64"

    # The url from where the 'config.vm.box' box will be fetched if it
    # doesn't already exist on the user's system.
    cfg.vm.box_url = "http://files.vagrantup.com/precise64.box"

    # Forward a port from the guest to the host, which allows for outside
    # computers to access the VM, whereas host only networking does not.
    cfg.vm.forward_port 80, 8080
    # To access our website, we can open a web browser on our workstation 
    # and go to http://localhost:8001. 
    cfg.vm.forward_port 8000, 8001

    # Enable provisioning with chef solo, specifying a cookbooks path 
    # (relative to this Vagrantfile), and adding some recipes and/or 
    # roles.
    #
    cfg.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = "cookbooks"
      # compilers
      chef.add_recipe "apt"
      chef.add_recipe "build-essential"
      # openssl is a requirement for postgresql
      chef.add_recipe "openssl"
      # postgresql database server
      chef.add_recipe "postgresql::client"
      chef.add_recipe "postgresql::server"
      # git and vim for virtual environment editing
      chef.add_recipe "git"
      chef.add_recipe "vim"
      # python plus pip and virtualenv
      chef.add_recipe "python::pip"
      chef.add_recipe "python::virtualenv"
      # zlib, libjpeg, and libfreetype are necessary for PIL
      chef.add_recipe "zlib"
      chef.add_recipe "chef-cookbook-libjpeg"
      chef.add_recipe "chef-cookbook-libfreetype"
      # xapian plain text search engine
      chef.add_recipe "chef-cookbook-xapian"
      # tie it all together
      chef.add_recipe "chef-cookbook-djangonewproj"
  
      # Assign the password 'thisisapassword' to psql user 'postgres'
      # Set the default python version to 2.7.3
      chef.json = { 
        :postgresql => {
          :version  => "9.1",
          :listen_address => "*",
          :hba => [
            { :method => "trust", :address => "0.0.0.0/0" },
            { :method => "trust", :address => "::1/0" }
          ],
          :password => {
            :postgres => "thisisapassword"
          }
        },
        :python => {
          :version => '2.7.3',
          :distribute_install_py_version => '2.7'
        }
      }
    end
  end
end
