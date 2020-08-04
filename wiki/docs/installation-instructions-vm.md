## How to Install D3A using a Virtual Machine (useful especially on Windows)

### Prerequisites

#####  Windows environment settings
1. Enable [Intel Virtualization](https://stackoverflow.com/a/34305608/13507565) on your computer in [BIOS](https://2nwiki.2n.cz/pages/viewpage.action?pageId=75202968).
2. Go to your [Windows Features](https://www.windowscentral.com/how-manage-optional-features-windows-10) setting and disable Windows Hypervisor Platform (or Hyper-V) and enable Virtual Machine Platform.


##### Install VirtualBox and Vagrant
It is recommended to use Chocolatey as a package management tool for Windows.

1. Install [chocolatey](https://chocolatey.org/) 
2. Install Virtualbox from a Windows console
```
choco install virtualbox
```
3. Install Vagrant
- This is a software wrapper around virtualbox and other supervisors, that allows easy creation, download, and installation of virtual machines.
```
choco install vagrant
```

### Install the D3A
After vagrant is installed, clone the d3a repository on your local machine.

```
git clone https://github.com/gridsingularity/d3a
```

### Steps to Execute D3A via Vagrant
Follow the steps below on a Windows console in order to run the d3a on Windows machine via Vagrant:
1.	```cd d3a/vagrant```: go to the directory where you have vagrant file for d3a
2.	```vagrant up```: start your virtual machine
3.	```vagrant ssh```: get remote access to your virtual machine
4.	```source envs/d3a/bin/activate```: activate the d3a environment used to run simulations in one terminal
5.	```cd d3a```: switch to d3a repository
6.	```d3a run```: start playing around with d3a (```d3a run --help``` could help you understand the command line interface)
7.	```exit```: come out of your remote virtual machine once you are finished running d3a
8.	```vagrant halt```: shut down your virtual machine



### Setting Up the API Client for Custom Trading Strategies (Optional)

Open a second terminal, activate vagrant with vagrant ssh, and activate the api client if you'd like to experiment with custom trading or grid fee strategies:

```
source envs/api-client/bin/activate
```

You may now follow the instructions on the [API documentation](api.md) file to get started with custom trading strategies
