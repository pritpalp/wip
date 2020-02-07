# Vagrant

Can create single file virtual environments with Vagrant.

## Pre-req's

* VirtualBox (6.0 and below)
* HomeBrew

Vagrant can use VirtualBox to create the virtual environments
HomeBrew to install

## Installation

```Bash
$ brew cask install vagrant
```

## How to use

There's really only one file needed. The *Vagrantfile*

To create a Vagrantfile you can use the following:
```Bash
$ vagrant init
```
This will create a file with a very basic config.

This is the minimum *Vagrantfile*:
```bash
Vagrant.configure("2") do |config|
   config.vm.box = "ubuntu/trusty64"
end
```

Line 15 in the file specifies the vm to create, eg the following would create a vm with ubuntu/bionic64:
```Bash
config.vm.box = "ubuntu/bionic64"
```

Once you've done that, you can spin up the vm if you want:
```Bash
$ vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Importing base box 'ubuntu/trusty64'...
==> default: Matching MAC address for NAT networking...
==> default: Checking if box 'ubuntu/trusty64' version '20190514.0.0' is up to date...
==> default: Setting the name of the VM: vagrant_default_1580230059400_70012
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default:
    default: Vagrant insecure key detected. Vagrant will automatically replace
    default: this with a newly generated keypair for better security.
    default:
    default: Inserting generated public key within guest...
    default: Removing insecure key from the guest if it's present...
    default: Key inserted! Disconnecting and reconnecting using new SSH key...
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
    default: The guest additions on this VM do not match the installed version of
    default: VirtualBox! In most cases this is fine, but in rare cases it can
    default: prevent things such as shared folders from working properly. If you see
    default: shared folder errors, please make sure the guest additions within the
    default: virtual machine match the version of VirtualBox you have installed on
    default: your host and reload your VM.
    default:
    default: Guest Additions Version: 4.3.40
    default: VirtualBox Version: 6.0
==> default: Mounting shared folders...
    default: /vagrant => /Users/pritpalp/Projects/wip/vagrant
```
Now you want to connect to your vm, you use:
```Bash
$ vagrant ssh
```
Use control + d to exit or just type exit.

If you've browse to the */vagrant* directory, you will be in the directory that you created the Vagrantfile in

To check the status:
```bash
$ vagrant status
Current machine states:

default                   not created (virtualbox)

The environment has not yet been created. Run `vagrant up` to
create the environment. If a machine is not created, only the
default provider will be shown. So if a provider is not listed,
then the machine is not created for that environment.
```

To stop/remove the machine:
```bash
$ vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
```

There is also 'vagrant halt' and 'vagrant help'

If you want to run a script (containing a load of command, like installing updates and apache etc) you can do this by creating the script file in the same place as your Vagrantfile.

Creating a *bootsrap.sh*:
```bash
#!/usr/bin/env bash

apt-get update

apt-get install -y nmon

if ! [ -L /var/www ]; then
	rm -rf /var/www
	ln -fs /vagrant /var/www
fi
```
Then in your *Vagrantfile*  add this in before the "end":
```bash
config.vm.provision :shell, path: "bootstrap.sh"
```
The script will be executed when you provision the vm with "vagrant up"

You can also do this inline in the *Vagrantfile*:
```bash
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.provision "shell", inline: <<-SHELL
     apt-get update
     apt-get install -y nmon
  SHELL
end
```

You can expose ports as well via the *Vagrantfile*, for example to map port 4567 to 80 on the vagrant box:
```bash
config.vm.network :forwarded_port, guest: 80, host:4567
```
