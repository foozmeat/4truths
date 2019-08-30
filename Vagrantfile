# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.box = "generic/ubuntu1804"

    config.vm.provider "virtualbox" do |vb|
        vb.linked_clone = true
        vb.customize ['modifyvm', :id, '--natnet1', '10.0.10.0/24']
    end

    config.vm.network :private_network, ip: '172.28.128.3'

    config.vm.synced_folder ".", "/root/4truths"

end
