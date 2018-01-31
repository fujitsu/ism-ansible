Ansible Modules for ServerView Infrastructure Manager
=====================================================

This is the modules to manage ServerView Infrastructure Manager using Ansible playbooks.


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

### 4. Setting config file

Set the account information of ServerView Infrastructure Manager for the confg file (`ism_config.json`).
Execute `config_setting.sh` with Ansible server as follows.The config file is created in the current directory when executing it.  
Refer from [[Note1]](#note-1) to [[Note5]](#note-5).

Example:

```shell
$ cd /etc/ansible/ism-ansible/
$ chmod +x ./config_setting.sh
$ ./config_setting.sh

> Enter IP address or FQDN:
  <IP address> or <FQDN>
> Enter port number:
  <Port No>
> Enter user name:
  <Login user name>
> Enter password:
  <Login password>
> Enter full path of certificate file:
  <full path of certificate file>
> completed
```

In each example in the above < >, specify the information of ServerView Infrastructure Manager.  
Refer to [[Note6]](#note-6).

Confirm the config file was created.

#### Example of execution with IP address:

```shell
$ cat ./ism_config.json
  {"ip":"192.168.1.10","portNo":"25566",
    "credentials":{"userName":"administrator",
    "password":"U2FsdGVkX18iGtLsngKkgWtQQ3+j0s5W1aSTizoWny8="},
    "certificate": "/etc/ansible/ism-ansible/certificate.crt"}
```
Describe the path of the config file in playbook.  
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

### 5. Setting inventory file

Specify the operation node for the inventory file.
Allocate the inventory file in Ansible server.

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

####  <Host group name>

Specify an arbitrary host group name.
The host group is defined as the multiple hosts united as one group.
In Ansible, the playbook can be executed for the host group unit.

#### <Operation node>

Specify the IP address of the operation node registered in ServerView Infrastructure Manager or the host name (FQDN) for its IP address.
When the OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.  
Refer to [[Note9]](#note-9) and [[Note10]](#note-10).

#### <Profile name>

The name of the profile assigned to the operation node can be omitted.
Specify when the ism_profile_assignment (Profile Assignment) module is executed.
In modules other than ism_profile_assignment, it is disregarded even if it is specified.
Do not specify the key part (`ism_profile_name=`) when omitting it.

Example: Host group name: servers

- Operation node1
  - IP address of OS information: 192.168.1.11
  - Profile name: profileA
- Operation node2
  - Node IP address: 192.168.1.12
- Operation node3
  - Host name for IP address of OS information: node3-os.test.local
- Operation node4
  - Host name for IP address of node: node4

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
playbook file path ：/etc/ansible/ism-ansible/examples/ism_firmware_list.yml  
inventory file path：/etc/ansible/hosts

```shell    
$ ansible-playbook /etc/ansible/ism-ansible/examples/ism_firmware_list.yml -i /etc/ansible/hosts
```

#### Changing processing time of Update Firmware and Profile Assignment settings

In the module of Update Firmware or Profile Assignment, waiting to complete the task in the internal processing.
The timeout period for the process of waiting to complete the task can be changed with the following ism_user_settings file.  
Refer to [[Note11]](#note-11).

ism_user_settings file path： /etc/ansible/ism-ansible/module_utils/ism_user_settings.py

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

#### Notes

<a name="note-1">[Note1]  
When the config file already exists, it will be overwritten.

<a name="note-2">[Note2]  
Specify the input values in single-byte upper-case, lower-case alphabetic letters, numbers, and symbols.

<a name="note-3">[Note3]  
When re-setting by changing the input information, make sure that the playbook and module are stopped, and that the proper procedure is executed again.

<a name="note-4">[Note4]  
When FQDN is used for the connection with ServerView Infrastructure Manager, confirm beforehand whether FQDN of ServerView Infrastructure Manager is available for name resolution on the Ansible server.

<a name="note-5">[Note5]  
Presently IPv6 is not supported. For the connection with ServerView Infrastructure Manager, specify the IP address of IPv4 or host name (FQDN) that are available for name resolution of IPv4.

<a name="note-6">[Note6]  
If the following error occurs when FQDN of ServerView Infrastructure Manager is specified with `config_setting.sh`, name resolution of FQDN of ServerView Infrastructure Manager has failed on the Ansible server. Ensure the action for name resolution and re-execute.

Example(For FQDN ism.test.local):

```shell
$ ./ism-ansible/config_setting.sh
  Enter IP address or FQDN:
  ism.test.local
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
  socket.gaierror: [Errno -2] Name or service not known
```
<a name="note-7">[Note7]  
Specify the config path in single-byte upper-case, lower-case alphabetic letters, numbers and symbols.

<a name="note-8">[Note8]  
Ansible Modules for ServerView Infrastructure Manager is executed on the Ansible server. Therefore, the specification for "Connection: local" of the playbook is mandatory.

<a name="note-9">[Note9]  
Presently IPv6 is not supported. Specify the IP address of IPv4 or host name (FQDN) that are available for name resolution of IPv4.

<a name="note-10">[Note10]  
When the host name (FQDN) is specified, confirm beforehand whether the host name (FQDN) is available for name resolution on the Ansible server is confirmed.

<a name="note-11">[Note11]  
Since the time-out time of 10800(second)(For = three hours), which sufficient for waiting for the task to complete, is specified in the default setting, it is not normally required to be changed.

License
-------

This project is licensed under the GPL v3 license. See the [LICENSE](LICENSE) for more information.

Copyright
---------
Copyright FUJITSU LIMITED 2017


API
---

- FUJITSU Software ServerView Infrastructure Manager V2.2 REST API Reference Manual
[http://www.fujitsu.com/jp/products/software/infrastructure-software/infrastructure-software/serverviewism/technical/](http://www.fujitsu.com/jp/products/software/infrastructure-software/infrastructure-software/serverviewism/technical/)
