# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.box = "generic/ubuntu1804"

    config.vm.provider "virtualbox" do |vb|
        vb.linked_clone = true
    end

    config.vm.synced_folder ".", "/root/4truths"

end
