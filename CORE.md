Core module of the project, contains the framework and basic scripts that provide the logic of the system.
Description of the main components of CLD, their scope, features of work and purpose.

# cld
The main application for accessing instances moves under the control of CLD. The utility allows you to use a pattern or run discovery, search across all instances, and quickly access desired instances. Examples of using:
```
cld #CLI,WEB
cld prod 1.2. #CLI,WEB
cld --groups=gcloud prod --debug #CLI,WEB
cld prod 1.2. --list 
cld prod 1.2. --groups=default --list --json --beauty
```
An example of choosing an instance for connecting via SSH using the cld utility:
```
root@cld.example.com ~ $  cld billing.example.com 
Please select instance to enter
1) billing.example.com_x.x.x.x_22_root
#? 1
You had chosen default billing.example.com_x.x.x.example_22_root

root@billing.example.com:~# 
```
This utility serves as a fast and reliable way to connect via SSH to any kind of servers and users, in addition, it allows you to customize connection settings based on access keys and username/password.

# cld-add
The utility that allows you to add a new instance to the CLD. In the process of adding, interactive data entry is implemented - connection ip address, port, username and password. After adding a new instance to `cld` with `cld-add`, you can access it quickly and conveniently later.
An example of adding a new instance `new-server.example.com` using the `cld-add` utility:
```
root@cld.example.com ~ $  cld-add
Please enter the VALUE for INSTANCE_NAME variable using [A-Za-z0-9.-]+ - symbols
EXAMPLE: server1.example.com
#: new-server.example.com

Please enter the VALUE for INSTANCE_IP variable using [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} - symbols
EXAMPLE: 1.2.3.4
#: 1.2.3.4

Please enter the VALUE for INSTANCE_PORT variable using [0-9]{2,5} - symbols
EXAMPLE: 22
#: 22

Please enter the VALUE for INSTANCE_USER variable using [A-Za-z0-9@.-]+ - symbols
EXAMPLE: root
#: root

new-server.example.com_1.2.3.4_22_root written to file /var/cld/access/groups/default/clouds
```

# cld-auditor
The utility is a service that monitors the status and parameters of cld systems. It controls all changes to the access matrix.

# cld-creds
The utility allows you to quickly generate a list of access parameters for CLD instances. The list is formed in human readable or defined application format.
The utility can work both in console mode and if it is configured to work with telegram/slack/mattermost/discord and others - the output will be generated and sent to the messenger.
An example of a real use of the `cld-creds` utility:
```
root@cld.example.com ~ $  cld-creds new
Host: new-server.example.com
ip: 1.2.3.4
port: 22
user: root
root@cld.example.com ~ $
```

# cld-edit
The utility allows you to edit groups of lists of instances managed by CLD. Running the `cld-edit` command in the console will provide a list of existing groups. By default, only one `default` group is used. When you select the `default` group, an editor will open with a list of all instances in this group. Then you can edit the required line and save.

# cld-getpasswd
The utility is used to obtain data about system users. It is possible to display values from the columns: group, bot, modules, utilities, etc. The main objective of this utility is to simplify the interaction of the access matrix with other utilities.
Usage example - getting groups in which the cld user with `admin` login is located:
```
root@cld.example.com ~ $  cld-getpasswd admin -g
default,panel
```

# cld-groupadd
The utility allows you to create a new group for subsequent management in cld. Working with groups allows you to simplify access for individual users, form a group, for example, for developer users, organize separate access to cld instances for them.

# cld-groupdel
A utility that allows you to delete an already created and existing cld group.

# cld-groupparser
The utility performs parsing scripts for groups marked as "parsing". It is a utility for ensuring the work of the internal logic of cld.

# cld-initpasswd
The utility initializes users created through the cld tools in `/var/cld/creds/passwd` as operating system users, updates and generates entries in the files `/etc/sudoers` and `~/.bashrc`

# cld-modulecreate
The utility allows you to create a new module in interactive mode, in the process you will need to enter the name of the new module cld, a brief description of the purpose of the module, after which the necessary module structure, file directories will be generated, the access matrix will be updated, the primary generation of the module documentation will be performed. The process may take some time.
An example of creating a new module using the `cld-modulecreate` utility:
```
root@cld.example.com ~ $  cld-modulecreate
Please enter new CLD MODULE name using only 'a-z 0-9' symbols
Example: somename
#? demomodule

Please enter the two/three words DESCRIPTION for new module using only 'A-z 0-9' symbols
Example: Short description
#? module for demo case

Files created:
/var/cld/modules/demomodule/api.py
/var/cld/modules/demomodule/bot.py
/var/cld/modules/demomodule/web.py
/var/cld/modules/demomodule/README.md
/var/cld/modules/demomodule/web/demomodule.html
/var/cld/modules/demomodule/bin/cld-demomoduletool

Update users permissions according access matrix /var/cld/creds/passwd

Update documentation
Module documentation will available by the link soon: https://devcld.example.com/doc#tag/demomodule

Module demomodule is ready
Restarting systemd cld services - it can take up to 15 seconds
root@cld.example.com ~ $  
```

# cld-modules
The utility returns a list of available modules and tools in the current cld configuration.
An example of using the cld-modules utility:
```
root@cld.example.com ~ $  cld-modules
cld:
cld
cld-add
cld-auditor
cld-creds
...

access:
cld-accesslistdeploy
cld-activateiptoken
...

backup:
cld-backup
cld-backupreport

cm:
cld-cm
cld-cmbackupcheck
...
```

# cld-mount
A utility for quick and easy mounting of directories on cld instances from other instances under its control. The remote filesystem will be `sshfs` mounted to the `/home/${USER}/mnt/${CLD_INSTANCE}` directory on the cld server. The work is carried out in an interactive mode.
An example of the `cld-mount` utility:
```
root@cld.example.com ~ $  cld-mount
 1) jenkins.srv_194.96.224.91_22_root
 2) vagrant.srv_97.72.19.117_22_root
...
#? 1

Inctance filesystem mounted to 
/home/admin/mnt/jenkins.srv_194.96.224.91_22_root
root@cld.example.com ~ $  
```

# cld-umount
The utility has the opposite effect of the `cld-mount` utility, as its name suggests. It allows you to interactively display the current mount points and unmount them. Work example:
```
root@cld.example.com ~ $  cld-umount
1) jenkins.srv_194.96.224.91_22_root
#? 1

Inctance filesystem unmounted from 
/home/admin/mnt/jenkins.srv_194.96.224.91_22_root
root@cld.example.com ~ $  
```

# cld-sessions
The utility allows you to get a list of running sessions on a cld instance. In addition, the utility allows you to connect to the selected session and in real time and observe what the current user sees.

# cld-setpasswd
The utility allows you to assign a user to participate in the list of groups with access rights to instances and tools. It is also used for the needs of internal utilities.

# cld-update
A utility that allows you to quickly and easily update the current version of the installed cld in automatic mode. In addition, the utility has an `upgrade` argument - allowing you to upgrade to the latest stable version or the version corresponding to the subscription type if you are using a paid plan. The `downgrade` argument is also provided - allowing you to transfer the state of cld to a free plan.
An example of the cld-update command on a business tariff:
```
root@cld.example.com ~ $  cld-update

Current subscription plan is business

Stop services
Check and wait if there current access list deploy
remote: Enumerating objects: 53, done.
remote: Counting objects: 100% (53/53), done.
remote: Compressing objects: 100% (33/33), done.
remote: Total 33 (delta 23), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (33/33), done.
From https://git.classicdeploy.com/cld/business
   974c0f9..a087799  master     -> origin/master
Updating 974c0f9..a087799
Fast-forward
 README.md                                | 43 ++++++++++++++++++++++++-------------------
 bin/cld-groupparser                      | 10 ++++++----
 modules/access/web/access.html           |  2 +-
 modules/backup/web.py                    | 10 +++++++---
 modules/backup/web/backup.html           | 41 ++++++++++++++++++++++++++++++++++++++---
 modules/doc/doc-common.py                |  2 +-
 modules/doc/doc.py                       |  4 ++--
 modules/doc/web/content/doc.css          |  2 --
 modules/etcbackup/README.md              | 14 --------------
 modules/etcbackup/bin/cld-etcbackup      | 61 -------------------------------------------------------------
 modules/etcbackup/bin/cld-etcbackupcheck | 74 --------------------------------------------------------------------------
 modules/etcbackup/init                   | 23 -----------------------
 web/dashboard.py                         | 13 +++++++++++++
 13 files changed, 92 insertions(+), 207 deletions(-)
 delete mode 100644 modules/etcbackup/README.md
 delete mode 100755 modules/etcbackup/bin/cld-etcbackup
 delete mode 100755 modules/etcbackup/bin/cld-etcbackupcheck
 delete mode 100755 modules/etcbackup/init
Update users rights according access matrix /var/cld/creds/passwd
Update private and public documentation
Start services
root@cld.example.com ~ $  
```

# cld-useradd
The utility allows you to create a user, give him a login, password, a list of tools, modules, groups, and instances available to the user.
An example of a simple user creation using the `cld-useradd` utility with one argument:
```
root@cld.example.com ~ $  cld-useradd test1
user: test1
password: GW8rGnhvsdypMNTXZkWv2ve3L

For additional permissions edit file /var/cld/creds/passwd
root@cld.example.com ~ $
```

# cld-userdel
The utility is the opposite of the `cld-useradd` functionality, it allows you to delete the created user by deleting the entry about him in the `/var/cld/creds/passwd` file, as well as delete all associated directories.

# cldx
Utility for direct instance terminal access CLI utility of ClassicDevOps access system. Will choose first one after all filters.

# cldx-bash-notty
Direct instance deploy CLI utility of ClassicDevOps access system. Read pipe input and execute on remote CLD instance.

# cldx-bash-tty
Direct instance deploy CLI utility of ClassicDevOps access system. Read pipe input and execute on remote CLD instance. Require "exit" at the end of input to stop execution. Will choose first one after all filters.

# cldxmount
Direct mount utility for mount filesystems of instance. Remote filesystem mounting by sshfs in /home/${USER}/mnt/${CLD_INSTANCE} directory. If there are several after filtering - the first one will be selected.

# cldxumount
The command is the opposite of `cldxmount`, unmounts the specified remote storage.

# init-main
Utility to initialize all constants required by the system and modules - run all init cld scripts. It is the primary executed command for configuring and provisioning CLD. It is an interactive utility, the process will prompt you to enter all the necessary data. Affects /var/cld/creds/creds and others if configured in module initialization scripts. Using the init-load-constants() and init-string() functions from /var/cld/bin/include/cldfuncs.
