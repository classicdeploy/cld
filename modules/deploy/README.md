The `deploy` module implements a system for managing, monitoring and distributing services, configurations and scripts to remote servers under CLD management.

For simpler, faster and more reliable work - the main element that ensures the execution of tasks within the `deploy` module - are bash scripts. You are free to create bash scripts for delivery and execution on remote servers at your own discretion. The functionality is extremely extensive, it allows you to perform even the most resource-intensive tasks on multiple servers managed by CLD. As part of the work on the creation and testing of this module, we launched the `deploy` module on 1500 different physical vps servers, as a result, we managed to get results that allow us to talk about its high quality performance. The `deploy` module has many areas of application, it allows you not only to make changes on hundreds of servers at the same time, monitor the progress of the execution process, but also perform automatic tests upon completion of the work, processing and displaying the test result for each of the servers involved in the work.

Thus, we can conclude that the `deploy` structure of a module consists of three main components: `templates, deployments and actions`. Further about each in more detail:
Deploy bash scripts to servers in the system.

The module structure consists of templates, deployments and actions. Each of these components makes it possible to compose tasks in an understandable way for subsequent execution on the servers of the system.
+ **cld-template**: templates contain the deployment script itself, a test script, a list of files and folders for a preliminary backup, settings for the deployment process, the template can also contain custom backup and restaurant scripts (for example). Templates have a number of arguments needed to work:
  - `--template=templatename    `:  Name of template
  - `--repoupdate `:  Update template list from connected repository list in file /var/cld/modules/deploy/repo_list
  - `--deploy=deployname    `:  Name of deploy
  - `--clouds=srv_1.2.3.4     `:  Instance pattern or list comma separated
  - `--groups=GROUP1,GROUP2   `:  Filtering by instance groups
  - `--test=0   `:  Execute test script after deploy - 0 is disabled - 1 is enabled
  - `--retry=1  `:  Count of retry deploy attempts per instance if ssh connection not established
  - `--timeout=180      `:  Timeout of deploy script in seconds
  - `--testtimeout=180      `:  Timeout of test script in seconds
  - `--backuptimeout=180    `:  Timeout for backup/custombackup script   
  - `--nextdeploy=deploy2     `:  Using for deploy chains - blank field for single deploy
  - `--nextdeploywait=1     `:  Wait the end of current deploy before start next
  - `--nextdeployargs=--run,--test=1`:  Next deploy arguments comma separated
  - `--backup=0 `:  Backup files of filelist before deploy - 0 is disabled - 1 is enabled
  - `--backuplist=/etc/,/tmp/file `:  List of files and directories for backup before deploy
  - `--custombackup=0`:  Use custom backup script before deploy - 0 is disabled - 1 is enabled
  - `--async=1  `:  Synchronous or asynchronous mode of deploy - 0 is sync - 1 is async
  - `--debug=0  `:  Verbose mode of connect and additional predeploy scripts will put to the output
  
As you can see from the text above, the templates of this module have a very wide functionality that will help you greatly simplify the work associated with performing routine and monotonous operations. Fine-tuning settings will allow you to achieve better results, automate processes for configuration, periodic updates, security audits and much more.


+ **cld-deploy**: is a script containing everything you need to launch an action, it can be created based on a template, or interactively during the first launch, in addition it includes - a list of servers, groups, or a name pattern (cli, api) (for example). Deploy have a number of arguments needed to work:
  - `--run  `:    Start deploy in non-interactive mode - interactive mode all other cases
  - `--deploy=deployname`:    Name of deploy - required if non-interactive mode
  - `--template=templatename        `:    Name of template - to create deploy from template - interactive mode
  - `$1 `:    First PATTERN filtering existing deploys - interactive mode
  - `$2`:    Second PATTERN filtering existing deploys - interactive mode
  - `$3`:    Third PATTERN filtering existing deploys - interactive mode
  - `--debug`:    Verbose output of connection
  - `--clouds=srv_1.2.3.4  `:    Instance pattern or list comma separated
  - `--groups=GROUP1,GROUP2`:    Filtering by instance groups
  - `--test=0`:    Execute test script after deploy - 0 is disabled - 1 is enabled
  - `--testprint=0      `:    Perform test script output after deploy (depend on --test argument) - 0 is disabled - 1 is enabled
  - `--retry=1 `:    Count of retry deploy attempts per instance if ssh connection not established
  - `--timeout=180      `:    Timeout of deploy script in seconds
  - `--testtimeout=180  `:    Timeout of test script in seconds
  - `--backuptimeout=180`:    Timeout for backup/custombackup script
  - `--nextdeploy=deploy2  `:    Using for deploy chains - blank field for single deploy
  - `--nextdeploywait=1 `:    Wait the end of current deploy before start next
  - `--nextdeployargs=--run,--test=1`:    Next deploy arguments comma separated
  - `--backup=0`:    Backup files of filelist before deploy - 0 is disabled - 1 is enabled
  - `--backuplist=/etc/,/tmp/file   `:    List of files and directories for backup before deploy
  - `--custombackup=0   `:    Use custom backup script before deploy - 0 is disabled - 1 is enabled
  - `--async=1 `:    Synchronous or asynchronous mode of deploy - 0 is sync - 1 is async
  - `--debug=0 `:    Verbose mode of connect and additional predeploy scripts will put to the output
  - `--output=full|bw|min  `:    Output deploy format - full is default
  - `--vars=var1=value1,var2=value2 `:    Pass variables to deploy

+ **cld-action**: contain the result of the deployment, including detailed logs (execution time and output of each command in terminal format as in manual line-by-line execution) for all servers, test results (for example). Action have a number of arguments needed to work:
  - `--deploy=deploy_name`:              Name of deploy
  - `--action=action_prefix`:              Action prefix
 
Deployments can be used both for prompt mass installation of something, for example, salt agents, zabbix, or for urgent fixing, monitoring, launching, including the crown, and for full-fledged deployment of applications of any complexity from a template, it can also work in conjunction with a virtualization module, for directly fine-tuning the environment of a virtual machine, immediately after creation, scenarios with sequential execution of deployments are also possible.
