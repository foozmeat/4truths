# -*- mode: ruby -*-
# vi: set ft=ruby :

#
# generic
#

boxes = [
    {:name => "3truths.vagrant.panic.com", :eth1 => "172.28.128.3", :mem => "1024", :cpu => "2"},
]

required_plugins = %w( vagrant-hostmanager-ext )
required_plugins.each do |plugin|
  system "vagrant plugin install #{plugin}" unless Vagrant.has_plugin? plugin
end

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.box = "panic1804"
    config.vm.box_url = "https://builds.panic.com/files/vagrant/panic1804/metadata.json"

    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
    config.hostmanager.manage_guest = true
    config.hostmanager.include_offline = true
    config.hostmanager.ignore_private_ip = false

    config.vm.provider "virtualbox" do |vb|
        vb.customize ['modifyvm', :id, '--natnet1', '10.0.10.0/24']
        vb.linked_clone = true
    end

    config.ssh.private_key_path = "~/.ssh/vagrant_rsa"
    config.ssh.username = "vagrant"



    # 3truths.vagrant.panic.com
    config.vm.define "3truths.vagrant.panic.com" do |host_config|
      host_config.vm.hostname = "3truths.vagrant.panic.com"

      host_config.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--memory", boxes[0][:mem]]
        v.customize ["modifyvm", :id, "--cpus", boxes[0][:cpu]]
        v.customize ["modifyvm", :id, "--nictype1", "virtio"]
        v.customize ["modifyvm", :id, "--nictype2", "virtio"]
        v.customize ["modifyvm", :id, "--uartmode1", "file", "/dev/null" ]
        v.name = "3truths"
      end

      host_config.vm.network :private_network, ip: boxes[0][:eth1]
    end

end
