Cloud manage module provides such functionality as creation, configuration and management of KVM servers on hypervisors running "Proxmox VE (Virtualization Management Platform)". The existing toolkit allows in the console mode to carry out all basic operations with KVM servers located on hypervisors under the control of CLD.

This module is a complete cycle of interaction with KVM, starting with flexible configuration of the creation stage and ending with control, management and scaling. Everything you ever needed for comfortable work on maintaining your own architecture is available within this module.

The main functionality of the `cm` module is described below:
 - Creation of KVM in real algorithm by means of the `cld-cmcreate` utility. During the creation process, the necessary data will be requested, which must be entered in order to run. Also, if necessary, it is possible to specify arguments on the command line, outside of the interactive mode:
The process begins with the operating system selection stage:
```
root@cld.example.com ~ $ cld-cmcreate
Please choose HYPERVISOR
Please choose OS
1) CENTOS7 3) DEBIAN9 5) FREEBSD11 7) UBUNTU18
2) UBUNTU16 4) FEDORA28 6) CENTOS6 8) CENTOS8
#?
```
As you can see from the example, there is quite an extensive list of different operating systems available for selection (`Centos, Debian, Ubuntu, Fedora, FreeBSD`) popular versions. As new versions of operating systems are released, the list will be updated and offer the latest templates. Operating system templates are loaded onto the hypervisor running ProxMox VE automatically using the built-in system for working with OS templates in CLD.
The next parameter that must be entered at the creation stage is the name of the KVM:
```
Please enter the VIRTUAL MACHINE NAME using only 'a-z 0-9 - .' symbols
Example: example.com
#?
```
You specify the information in this field yourself using the pattern `a-z 0-9 - .`.
In the next step, you will be able to specify the number of CPU cores required, the amount of RAM required, and the amount of disk space. Next, you will be prompted to enter the external ip address of the server and the MAC address. Having entered all these data, CLD will start creating KVM.

- In addition to simple and quick installation - CLD offers a basic configuration of the operating system, which includes parameters for optimizing and speeding up the OS, correct settings for network interfaces, applying rules for secure access to the OS.

- Within this module, support for creating several types of file systems (`zfs, lvm, qcow2`) is available, it is recommended to use `zfs` - it has high quality and stability when working in production, which is confirmed by real use cases in various high-loaded systems.

- CLD also controls the assignment and operation of ip addresses for each KVM installed at the deployment stage. This is a useful and important step to ensure secure, correct and controlled network operation within the entire system.

- For greater security and fault tolerance - a QEMU guest agent is installed in each OS, all management capabilities are available from the hypervisor. QEMU guest agent has extensive functionality that allows you to finely organize work with KVM, as well as easily solve emerging problems.

- As part of the creation process, a serial port with autologin option is connected for each KVM during deployment, a serial console is configured in all OS templates 

- If necessary, it is possible to change the root password on KVM in soft (without rebooting) and hard modes (by mounting the file system on the switched off KVM).

- Using the `cld-cmmigrate` utility included in the `cm` module - KVM migration between hypervisors in interactive and direct mode (zfs), (other file systems via shared network storage) is available. The process is as simple and informative as possible, all you need to migrate KVM from one hypervisor to another is to select KVM, specify the hypervisor and the final patch, after that the migration process will begin. The migration is as informative as possible, all progress will be displayed in the console so that you can control it.
```
root@cld.example.com ~ $  cld-cmmigrate
KVM_SET is not defined - parsing hypervisors
Please choose KVM to migrate
1) kvm.example.com_10001_HPR-ovh-4-ns3852080
#? 1
```
- The `cm` module includes the `cld-cmcontrol` utility for centralized management of all KVM servers (start, stop, reset, kill). Work example:
```
root@cld.example.com ~ $  cld-cmcontrol
KVM_SET is not defined - parsing hypervisors
Please choose KVM to control
1) kvm.example.com_10001_HPR-ovh-4-ns3852080
#? 1

Command is not defined
Please choose COMMAND to kvm.example.com_10001_HPR-ovh-4-ns3852080
1) start
2) stop
3) reset
4) resume
5) suspend
#? 
```
- The `cm` module includes support for the largest hosting providers, such as API OVH, Hetzner, Online.net (full support for functionality: ordering ip addresses, migrating ip addresses between services, creating MAC addresses).

- ProxMox VE has a built-in backup system for KVM servers. The backup process does not always complete successfully and may depend on a number of factors with which it is associated. To solve this problem, we have implemented another utility. The `cm` module includes the `cmbackupcheck` utility, its main task is to check KVM backups on hypervisors on a daily basis. The results of the check are sent to telegrams or by mail, contain all the necessary information that allows you to visually understand the situation with backups. Report example:
```
Hypervisor backup status:
HPR-ovh-4-nsXXXX
OK - jenkins.srv - Last 2022_01_30 0.99G - online
OK - vagrant.srv - 6.63G - online
OK - pagerduty.srv - Last 2021_12_26 637.81G - online
OK - prometheus.srv - 2.74G - online
OK - ganglia.srv - 10.95G - online
OK - snort.srv - 2.36G - online
OK - splunk.srv - 46.60G - online
OK - nagios.srv - 26.13G - online
BACKUP NOT FOUND - rabbitmq.srv
...
```
- Trying to control the entire cycle of working with KVM, starting from the creation stage, we have provided scripts for deploying hypervisors (debian 9, debian 10), full OS configuration, network settings, network storages as part of the `cm` module.

As part of the work on this module, we conducted a lot of tests, found out weaknesses and tried to foresee almost everything. The work of this module has been tested on a lot of projects in real work.
