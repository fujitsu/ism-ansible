Ansible Modules for ServerView Infrastructure Manager
=====================================================

Modules to manage ServerView Infrastructure Manager using Ansible playbooks.

Requirements
------------

- Ansible Server
  - Ansible 2.4 or later
  - Python  2.6 or later
- Fujitsu Software ServerView Infrastructure Manager
  - 2.2.0


### Examples

Sample playbooks and instructions on how to run the modules can be found in the examples directory.

Setup
-----

To run the Ansible modules and sample playbooks provided in this project, you should execute the following steps:

### 1. Clone the repository
    
Run on the Ansible Server:

```shell
$ cd /etc/ansible
$ git clone https://github.com/fujitsu/ism-ansible.git
```

### 2. Configure the ANSIBLE_LIBRARY environmental variable

Set the environment variables `ANSIBLE_LIBRARY` and `ANSIBLE_MODULE_UTILS`, `PYTHONPATH`, specifying the library full path from the cloned project.

Run on the Ansible Server:

```shell
$ export ANSIBLE_LIBRARY=/etc/ansible/ism-ansible/library
$ export ANSIBLE_MODULE_UTILS=/etc/ansible/ism-ansible/library/module_utils/
$ export PYTHONPATH=$PYTHONPATH:$ANSIBLE_LIBRARY
```

### 3. Certificate assignment for ServerView Infrastructure Manager

Acquire the certificate used for https communication and assign in the Ansible server. 

For information on how to assign certificates, refer to "3.1.1 Preparation" in
"FUJITSU Software ServerView Infrastructure Manager V2.2 REST API Reference Manual".

### 4. Setting of config file

Account information of ServerView Infrastructure Manager is set to config file(`ism_config.json`).  
`config_setting.sh` is executed with Ansible server as follows.   
The config file is made for the current directory when executing it.   
Refer from [[Note1]](#note-1) to [[Note5]](#note-5).  

Example:

```shell
$ cd /etc/ansible/ism-ansible/
$ chmod +x ./config_setting.sh
$ ./config_setting.sh
    
  Please enter IP address or FQDN:
  <IP address> or <FQDN>
  Please enter port number:
  <Port No>
  Please enter user name:
  <Login user name>
  Please enter password:
  <Login password>
  Please enter full path of certificate file: 
  <full path of certificate file>
  completed
```

In each <> of the example of the above-mentioned, information on ServerView Infrastructure Manager is specified.  
Refer to [[Note6]](#note-6).

Confirm the config file was made. 
  
#### Example of execution with IP address:

```shell
$ cat ./ism_config.json
  {"ip":"192.168.1.10","portNo":"25566",
    "credentials":{"userName":"administrator",
    "password":"U2FsdGVkX18iGtLsngKkgWtQQ3+j0s5W1aSTizoWny8="}, 
    "certificate": "/etc/ansible/ism-ansible/certificate.crt"}
```
Describe pass of the config file in playbook.  
Refer to [[Note7]](#note-7) and [[Note8]](#note-8).
  
Example： 

```yaml
- name: Firmware update
  hosts: servers
  connection: local
      
  tasks:
   - name: Execution of ism_firmware_update
     ism_firmware_update:
       config: "/etc/ansible/ism-ansible/ism_config.json"
```

### 5. Setting of inventory file

The node for the operation is specified for the inventory file.   
The inventory file is arranged in Ansible server. 

Format:

```
  +------------------------------------------------------
  | [<Host group name>]
  | <Operation node1> ism_profile_name=<profile name>
  | <Operation node2> 
  | <Operation node3>
  | ...
  +------------------------------------------------------
```
#### &lt;Host group name&gt;

An arbitrary host group name is specified. 
The one that a lot of hosts were defined as one group host group. 
In Ansible, playbook can be executed for the unit of the host group. 

#### &lt;Operation node&gt;

Host name (FQDN) to IP address or the IP address of Operation node 
registered in ServerView Infrastructure Manager is specified. 
When OS information on Operation node is registered in ServerView Infrastructure Manager, 
host name (FQDN) to IP address of OS information or the IP address can be specified.   
Refer to [[Note9]](#note-9) and [[Note10]](#note-10).

#### &lt;Profile name&gt;

The name of the profile applied to Operation node can be omitted.
When ism_profile_assignment (application of the profile) module is executed, it specifies it. 
In modules other than ism_profile_assignment, it is disregarded even if it specifies it. 
Do not specify key part (`ism_profile_name=`) when omitting it. 

Example: Host group name is servers

- Operation node1
  - IP address of OS information: 192.168.1.11
  - Profile name: profileA
- Operation node2
  - Node IP address: 192.168.1.12
- Operation node3
  - Host name to IP address of OS information: node3-os.test.local
- Operation node4
  - Host name to IP address of node: node4
  
```  
  +---------------------------------------------------
  | [servers]
  | 192.168.1.11 ism_profile_name=profileA
  | 192.168.1.12
  | node3-os.test.local
  | node4
  +---------------------------------------------------
```

Playbook execution
------------------

The following commands are executed with Ansible server. 

```shell
$ ansible-playbook <playbook file path> -i <inventory file path>
```
Example：  
playbook file path ：`/etc/ansible/ism-ansible/examples/ism_firmware_list.yml`  
inventory file path：`/etc/ansible/hosts`
    
```shell
$ ansible-playbook /etc/ansible/ism-ansible/examples/ism_firmware_list.yml -i /etc/ansible/hosts
```

### Processing time of firmware update and profile application setting change

In the module of the application of the firmware update and the profile, the completion meeting of the task is done as internal processing. 
It is revokable in the following ism_user_settings files at the timeout period of the completion meeting of the task. 
Refer to [[Note11]](#note-11).

ism_user_settings file path：`/etc/ansible/ism-ansible/module_utils/ism_user_settings.py`
  
Example:  
Timeout period of firmware update: `14400` (second) (= 4hours)  
Timeout period of application of profile: `18000` (second) (= 5hours)
  
```
  +---------------------------------------------------
  | #!/usr/bin/python
  | #coding: UTF-8
  | 
  | # user_settings_value
  | 
  | '''
  | Set time confirmation for task confirmation
  | '''
  | FIRMWARE_UPDATE_TIME_OUT = 14400
  | 
  | PROFILE_ASSIGNMENT_TIME_OUT = 18000
  +---------------------------------------------------
```

### Notes

<a name="note-1">[Note1]  
When the config file already exists, it is overwrited.

<a name="note-2">[Note2]  
The input value is specified by the alphabet capital letters and small letters,
the figure, and the sign of normal-width.

<a name="note-3">[Note3]  
When input information is changed and set again, playbook and the module are stopped, and the order of the proper move is executed again.

<a name="note-4">[Note4]  
When FQDN is used for the connection with ServerView Infrastructure Manager, 
whether FQDN of ServerView Infrastructure Manager is good at the name resolution beforehand on Ansible server is confirmed.

<a name="note-5">[Note5]  
Presently IPv6 is not supported. To the connection with ServerView Infrastructure Manager,   
specify IP address of IPv4 or host name (FQDN) that can do the name resolution of IPv4. 

<a name="note-6">[Note6]  
It fails in the name resolution of FQDN of ServerView Infrastructure Manager on Ansible server 
when the following errors occur when FQDN of ServerView Infrastructure Manager is specified with `config_setting.sh`.
It deals to do the name resolution, and it executes it again.

Example(For FQDN ism.test.local):

```shell
$ ./ism-ansible/config_setting.sh
  Please enter IP address or FQDN:
  ism.test.local
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
  socket.gaierror: [Errno -2] Name or service not known
```

<a name="note-7">[Note7]  
The config file path is specified by the alphabet capital letters and small letters, the figure, and the sign of normal-width.


<a name="note-8">[Note8]  
Ansible Modules for ServerView Infrastructure Manager is executed on Ansible server. 
Therefore, the specification of "`connection: local`" of playbook is indispensable. 

<a name="note-9">[Note9]  
Presently IPv6 is not supported.  
Specify IP address of IPv4 or host name (FQDN) that can do the name resolution of IPv4. 

<a name="note-10">[Note10]  
When host name (FQDN) is specified, whether the host name (FQDN) is good at the name resolution beforehand on
Ansible server is confirmed. 

<a name="note-11">[Note11]  
There is usually no alterations necessary because time-out time 10800(second)(For = three hours) 
enough for the completion meeting of the task by the initial state is specified. 

[About the software support in this project]  
The software is not supported. 

License
-------

This project is licensed under the GPL v3 license. Please see the [LICENSE](LICENSE) for more information.

Copyright
---------
Copyright FUJITSU LIMITED 2017

API
---

- FUJITSU Software ServerView Infrastructure Manager V2.2 REST API Reference Manual
[https://partners.ts.fujitsu.com/s/primeweb/services/software/ServerView/ism/Pages/default.aspx](https://partners.ts.fujitsu.com/s/primeweb/services/software/ServerView/ism/Pages/default.aspx)