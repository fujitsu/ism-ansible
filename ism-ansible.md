Ansible Fujitsu ServerView Infrastructure Manager Modules
===========================
#### Modules

 * [ism_firmware_list - List Retrieval for Firmware.](#ism_firmware_list)
 * [ism_firmware_update - Firmware Updates.](#ism_firmware_update)
 * [ism_maintenance_mode_setting - Changing from/to Maintenance Mode.](#ism_maintenance_mode_setting)
 * [ism_profile_assignment - Assigning Profiles to Nodes.](#ism_profile_assignment)
 * [ism_power_on - Instruction to Power-on.](#ism_power_on)

---

<a name="ism_firmware_list">ism_firmware_list
-----------------

List Retrieval for Firmware.

### Synopsis

Retrieve the summary of the firmware registered to ServerView Infrastructure Manager.
The list of retrieved information is specified for the parameter of firmware update module (`ism_firmware_update.py`).

### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0

### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:--|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and Host name of the oOperation node are specified.<br> [[Note1]](#note-1-1) [[Note2]](#note-1-2)|
|firmware_type|-|None|<ul><li>BIOS</li><li>iRMC</li><li>FC</li><li>CNA</li><li>ETERNUS DX</li><li>LAN Switch</li></ul>|When specifies the firmware type is specified, the list of the specified firmware type is output. The list of all firmwares is output when omitting it.|


<a name="note-1-1">[Note1]  
Specify the IP address of the operation node registered in ServerView Infrastructure Manager or the host name (FQDN) for its IP address.
When OS information of the operation node that is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of OS information or the IP address can be specified.

<a name="note-1-2">[Note2]  
Presently IPv6 is not supported. To the connection with ServerView Infrastructure Manager,   
specify the IP address of IPv4 or host name (FQDN) that are available for name resolution of IPv4.

### Examples

```yaml
- name: Execution of ism_firmware_list
  ism_firmware_list:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    firmware_type: "iRMC"
  register: ism_firmware_list_result
- debug: var=ism_firmware_list_result
```

### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|:--|
|ism_firmware_list|dict|Always.|Acquisition result of the firmware list|
|IsmBody|dict|Always, but can be null.|API processing results|
|FirmwareList|dict-list|Always, but can be null.|List of Firmware|
|DiskUsage|string|Always, but can be null.|Disk capacity used by firmware (MB)|
|FirmwareId|integer|Always, but can be null.|Firmware ID|
|FirmwareName|string|Always, but can be null.|Firmware name|
|FirmwareType|string|Always, but can be null.|Firmware type|
|FirmwareVersion|string|Always, but can be null.|Firmware version|
|ModelName|string|Always, but can be null.|Model name|
|NodeId|integer|Always, but can be null.|Node ID|
|OperationMode|string|Always, but can be null.|Supported modes|
|RegisterDate|string|Always, but can be null.|Time/date of firmware registration|
|RepositoryName|string|Always, but can be null.|Repository name|
|MessageInfo|list|Always, but can be null.|Message information Errors, warnings, and notification messages regarding API processing are output.If there is no information available, only the key names are output.|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|

### Return Values (Abnormal)

When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are returned|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message was produced is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI"|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters|
|IsmBody|dict|Always, but can be null.|API processing results|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|

Case except the above.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|string|Always, but can be null.|Message except API processing results|

#### Notes

- Refer to the following URL for information regarding parameter setting in config file and inventory file.
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for information regarding sample playbook using ism_firmware_list.
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_list.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_list.yml)

---

<a name="ism_firmware_update">ism_firmware_update
-------------------

Firmware Updates.

### Synopsys

Commences updating process firmware registered to ServerView Infrastructure Manager.

### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.

### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation.<br>[[Note1]](#note-2-1) [[Note2]](#note-2-2)|
|firmware_update_list|〇|None|None|Array data of dictionary type that specifies updated firmware.<br>Firmware_name, repository_name, firmware_version, and operation_mode are specified for an element of this dictionary type.
|firmware_name|〇|None|None|Firmware name<br>[[Note3]](#note-2-3)|
|repository_name|〇|None|None|Repository name<br>[[Note3]](#note-2-3)|
|firmware_version|-|None|None|Firmware version<br>[[Note3]](#note-2-3)|
|operation_mode|〇|None|Online<br>Offline|Supported modes<br>Online: Online update<br>Offline: Offline update <br>[[Note3]](#note-2-3)|

<a name="note-2-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of Operation node registered in ServerView Infrastructure Manager.
When OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of OS information or the IP address can be specified.

<a name="note-2-2">[Note2]  
Presently IPv6 is not supported. To the connection with ServerView Infrastructure Manager, 
specify the IP address of IPv4 or host name (FQDN) that is available for name resolution of IPv4.

<a name="note-2-3">[Note3]  
Multiple firmware can be updated at the same time by specifying multiple firmware.
In that case, specifies all the same values (either of Online or Offline).
The format is as follows.

```yaml
firmware_update_list:
 - firmware_name: Firmware name 1
   repository_name: Import data name 1
   firmware_version: Updated firmware version 1
   operation_mode: Update mode 1
 - firmware_name: Firmware name 2
   repository_name: Import data name 2
   firmware_version: Updated firmware version 2
   operation_mode: Update mode 2
 - firmware_name: Firmware name 3
   repository_name: Import data name 3
   firmware_version: Updated firmware version 3
   operation_mode: Update mode 3
...
```

### Examples

When you update the firmware of iRMC

```yaml
- name: Execution of ism_firmware_update
  ism_firmware_update:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    firmware_update_list:
     - firmware_name: "RX300 S8_iRMC"
       repository_name: "Update DVD 12.17.04.03 Administrator"
       firmware_version: "8.64F&3.72"
       operation_mode: "Online"
  register: ism_firmware_update_result
- debug: var=ism_firmware_update_result
```
When you update the firmware of iRMC and BIOS at the same time

```yaml
- name: Execution of ism_firmware_update
ism_firmware_update:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    firmware_update_list:
     - firmware_name: "RX300 S8_iRMC"
      repository_name: "Update DVD 12.17.04.03 Administrator"
      firmware_version: "8.64F&3.72"
      operation_mode: "Online"
     - firmware_name: "RX300 S8_BIOS"
      repository_name: "Update DVD 12.17.04.03 Administrator"
      firmware_version: "R1.11.0"
      operation_mode: "Online"
  register: ism_firmware_update_result
- debug: var=ism_firmware_update_result
```

### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|Ism_firmware_update|string|Always. "Success"|Firmware update result|

### Return Values (Abnormal)

When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output.|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information on the date and time when the corresponding message was produced is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|IsmBody|dict|Always, but can be null.|The processing result of REST-API is output.|
|SchemaType|string|Always, but can be null.|The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.|

Case other than the above.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|string|Always, but can be null.|Message except API processing results|

#### Notes

- Refer to the following URL for information regarding parameter setting in config file and inventory file. 
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for information regarding sample playbook using ism_firmware_update.
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_update.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_update.yml)

---

<a name="ism_maintenance_mode_setting">ism_maintenance_mode_setting
----------------------------

Changing from/to Maintenance Mode.

### Synopsis

Changes maintenance mode of a node.  
A node with its maintenance mode is "Maintenance" cannot perform retrieval of node information for monitoring and regular schedule as well as notification of events.

### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0

### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:--|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation. <br>[[Note1]](#note-3-1) [[Note2]](#note-3-2)|
|mode|〇|None|On<br>Off|Maintenance mode<br>"On": Setting<br>"Off": Release|

<a name="note-3-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of Operation node registered in ServerView Infrastructure Manager is specified. 
When OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of OS information or the IP address can be specified.

<a name="note-3-2">[Note2]  
Presently IPv6 is not supported. To the connection with ServerView Infrastructure Manager,   
specify the IP address of IPv4 or host name (FQDN) that is available for name resolution of IPv4.

### Examples

```yaml
- name: Set Maintenance Mode
  ism_maintenance_mode_setting:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    mode: "On"
  register: ism_maintenance_mode_setting_result
- debug: var=ism_maintenance_mode_setting_result
```

### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|ism_maintenance_mode|string|Always. "Success"|Maintenance mode setting result|

### Return Values (Abnormal)

When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output.|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information on the date and time when the corresponding message produced is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|IsmBody|dict|Always, but can be null.|API processing results.|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema<br>(JSON schema file name) that displays the entire HTTP body structure is output.|

Case except the above.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|string|Always, but can be null.|Message except API processing results.|

#### Notes

- Refer to the following URL for information regarding parameter setting in config file and inventory file.
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for information regarding sample playbook using ism_maintenance_mode.
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_update.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_update.yml)
 

---

<a name="ism_profile_assignment">ism_profile_assignment
----------------------

Assigning Profiles for Nodes

### Synopsis

Assign specified profiles for the specified nodes managed by ServerView Infrastructure Manager.

### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0

### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:--|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation.<br>[[Note1]](#note-4-1) [[Note2]](#note-4-2)|
|ism_profile_name|〇|None|None|Profile name.|
|assign_mode|-|None|<ul><li>Normal</li><li>Advanced</li></ul>|Specifies assign node.<br> Normal: Normal assign<br>Advanced: Advanced assign When this setting is omitted or null, operations will be carried out as Normal.<br>[[Note3]](#note-4-3)|
|advanced_kind|-|None|<ul><li>ForcedAssign</li><li>WithoutHardwareAccess</li><li>OnlineAssign</li></ul>|Specifies the profile name for operation node. Refer to [[Table 1]](#table-4-1) for the combination that can be specified. Specifies type of advanced application.<br>To be specified when the AssignMode is 'Advanced'.<br>ForcedAssign: Forced assignment<br>WithoutHardwareAccess: The application intended to be applied<br>OnlineAssign: Online application<br>ForcedAssign cannot be used in first-time application.<br>When IOVirtualization or OSInstallation is included in the AssignRange, Online Assign cannot be used.|
|assign_range|-|None|<ul><li>BIOS</li><li>iRMC</li><li>MMB</li><li>IOVirtualization</li><li>OSInstallation</li></ul>|Records types of Profile for assignment. If the AssignMode is Advanced,<br>"BIOS," "iRMC," "MMB,"<br>"IOVirtualization" and/or <br>"OSInstallation" can be specified either individually or together.<br>E.g.) ["BIOS","iRMC"] When this setting is omitted or null, all types of profile in ProfileData are assigned. Refer to [[Table 1]](#table-4-1) for the combination that can be specified.|

<a name="note-4-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of Operation node registered in ServerView Infrastructure Manager.  
When OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of OS information or the IP address can be specified.

<a name="note-4-2">[Note2]  
Presently IPv6 is not supported. To the connection with ServerView Infrastructure Manager,   
specify the IP address of IPv4 or host name (FQDN) that is available for name resolution of IPv4.

<a name="note-4-3">[Note3]  
Specify the Normal for the usual assignment.
Specify the Advanced for the advanced assignment.
For the usual assignment and advanced assignment, refer to "2.2.3 Profile Management" in "FUJITSU Software ServerView Infrastructure Manager V2.2 User's Manual".  
[http://www.fujitsu.com/jp/products/software/infrastructure-software/infrastructure-software/serverviewism/technical/index.html](http://www.fujitsu.com/jp/products/software/infrastructure-software/infrastructure-software/serverviewism/technical/index.html)

<a name="table-4-1">[Table 1]

|assign_mode|advanced_kind|assign_range|
|:--|:--|:--|
|Normal|Cannot be specified<br>(Even if specified, it will be disregarded.)|Cannot be specified<br>(Even if specified, it will be disregarded.)|
|Advanced|ForcedAssign<br>(It can be specified, only when the profile has been applied.)<br> (*2)|<ul><li>BIOS</li><li>iRMC</li><li>MMB</li><li>IOVirtualization</li></ul>|
|Advanced|WithoutHardwareAccess|<ul><li>BIOS</li><li>iRMC</li><li>MMB</li><li>IOVirtualization</li><li>OSInstallation</li></ul>|
|Advanced|OnlineAssign|<ul><li>BIOS</li><li>iRMC</li><li>MMB</li>|

(*2)  
When the profile is unassigned and if you specify the ForcedAssign, REST-API returns the error.


#### Usage example 1

```yaml
- name: Execution of ism_profile_assignment
  ism_profile_assignment:
     config: "/etc/ansible/ism-ansible/ism_config.json"
     hostname: "192.168.1.22"
     ism_profile_name: "profileA"
  register: ism_profile_assignment_result
- debug: var=ism_profile_assignment_result
```

#### Usage example 2

A specified value of the assign_range is one cases.

```yaml
- name: Execution of ism_profile_assignment
  ism_profile_assignment:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    ism_profile_name: "profileA"
    assign_mode: "Advanced"
    advanced_kind: "OnlineAssign"
    assign_range:
      - BIOS
  register: ism_profile_assignment_result
- debug: var=ism_profile_assignment_result
```

#### Usage example 3

A specified value of the assign_range is two or more cases.

```yaml
- name: Execution of ism_profile_assignment
  ism_profile_assignment:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    ism_profile_name: "profileA"
    assign_mode: "Advanced"
    advanced_kind: "OnlineAssign"
    assign_range:
      - BIOS
      - iRMC
  register: ism_profile_assignment_result
- debug: var=ism_profile_assignment_result
```

### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|ism_profile_assignment|string|Always. "Success"|Profile assignment result|

#### Return Values (Abnormal)

When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output.|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message displayed is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results <br>API processing results are output as response parameters.|
|IsmBody|dict|Always, but can be null.|API processing results|
|SchemaType|string|-|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|

Case except the above.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|string|Always, but can be null.|Message except API processing results.|

#### Notes

- Refer to the following URL for information regarding parameter setting in config file and inventory file.
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for information regarding sample playbook using ism_profile_assignment.
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_profile_assignment.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_profile_assignment.yml)

---
 
ism_power_on
------------

Instruction for Power-on.

### Synopsis

Instruction for Power-on of the specified nodes managed by ServerView Infrastructure Manager.

### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0

### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:--|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation.<br>[[Note1]](#note-5-1) [[Note2]](#note-5-2)|

<a name="note-5-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of Operation node registered in ServerView Infrastructure Manager is specified.  
When OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of OS information or the IP address can be specified.

<a name="note-5-2">[Note2]  
Presently IPv6 is not supported. To the connection with ServerView Infrastructure Manager,   
specify the IP address of IPv4 or host name (FQDN) that is available for the name resolution of IPv4.

### Examples

```yaml
- name: Execution of ism_power_on
  ism_power_on:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
  register: ism_power_on_result
- debug: var=ism_power_on_result
```

### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|ism_power_on|string|Always. "Success"|The execution result of power supply On is output.|

### Return Values (Abnormal)

When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information <br>Errors, warnings, and notification messages regarding API processing are output. <br>If there is no information available, only the key names are output.|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message displayed is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|IsmBody|dict|Always, but can be null.|API processing results|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|

Case except the above.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|string|Always, but can be null.|Message except API processing results|

#### Notes

- Refer to the following URL for information regarding parameter setting in config file and inventory file.
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for information regarding sample playbook using ism_power_on.
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_power_controls.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_power_controls.yml)

---

Copyright
---------
Copyright FUJITSU LIMITED 2017