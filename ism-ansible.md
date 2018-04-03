Ansible Fujitsu ServerView Infrastructure Manager Modules
===========================
#### Modules

 * [ism_firmware_list - List Retrieval for Firmware.](#ism_firmware_list)
 * [ism_firmware_update - Firmware Updates.](#ism_firmware_update)
 * [ism_maintenance_mode_setting - Changing from/to Maintenance Mode.](#ism_maintenance_mode_setting)
 * [ism_profile_assignment - Assigning Profiles to Nodes.](#ism_profile_assignment)
 * [ism_power_on - Instruction to Power-on.](#ism_power_on)
 * [ism_refresh_node_info - Refreshing Node Information.](#ism_refresh_node_info)
 * [ism_get_inventory_info - Retrieving Inventory Information.](#ism_get_inventory_info)
 * [ism_get_profile_info - Retrieving Profile Information](#ism_get_profile_info)
 * [ism_get_power_status - Retrieving Power Status](#ism_get_power_status)
---

<a name="ism_firmware_list">ism_firmware_list
-----------------

List Retrieval for Firmware



#### Synopsis

Retrieves the summary of the firmware registered to ServerView Infrastructure Manager.  
The list of retrieved information is specified for the parameter of firmware update module (ism_firmware_update.py).


#### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0


#### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:-:|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and Host name of the operation.<br>[[Note1]](#note-1-1) [[Note2]](#note-1-2)|
|firmware_type|-|None|・BIOS<br>・iRMC<br>・FC<br>・CNA<br>・ETERNUS DX<br>・LAN Switch|When specifies the firmware type, the list of the specified firmware type is output. The list of all firmware is output when omitting it.|

<a name="note-1-1">[Note1]  
Specify the IP address of the operation node registered in ServerView Infrastructure Manager or the host name (FQDN) for its IP address.  
When the OS information of the operation node that is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-1-2">[Note2]  
Presently IPv6 is not supported. To the connection with ServerView Infrastructure Manager, specify the IP address of IPv4 or host name (FQDN) that are available for name resolution of IPv4.

#### Examples

```yaml
- name: Execution of ism_firmware_list
   ism_firmware_list:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    firmware_type: "iRMC"
   register: ism_firmware_list_result
- debug: var=ism_firmware_list_result
```

#### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|:--|
|ism_firmware_list|dict|Always.|Retrieval result of the firmware list|
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
|MessageInfo|list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output.|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|

#### Return Values (Abnormal)
When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output.|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message was produced is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|IsmBody|dict|Always, but can be null.|API processing results|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|

Case except the above.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|string|Always, but can be null.|Message except API processing results.|

#### Notes

- Refer to the following URL for the information regarding parameter setting in config file and inventory file.  
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for the information regarding sample playbook using ism_firmware_list.  
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_list.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_list.yml)

---

<a name="ism_firmware_update">ism_firmware_update
-------------------

Firmware Updates



#### Synopsys

Commences updating process firmware registered to ServerView Infrastructure Manager.

#### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.


#### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:-:|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation. [[Note1]](#note-2-1) [[Note2]](#note-2-2)|
|firmware_update_list|〇|None|None|Array data of dictionary type that specifies updated firmware.<br>Firmware_name, repository_name, firmware_version, and operation_mode are specified for an element of this dictionary type.|
|firmware_name|〇|None|None|Firmware name<br>[[Note3]](#note-2-3)|
|repository_name|〇|None|None|Repository name<br>[[Note3]](#note-2-3)|
|firmware_version|-|None|None|Firmware version<br>[[Note3]](#note-2-3)|
|operation_mode|〇|None|・Online<br>・Offline|Supported modes<br>- Online: Online update<br>- Offline: Offline update<br>[[Note3]](#note-2-3)|

<a name="note-2-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of operation node registered in ServerView Infrastructure Manager.  
When the OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-2-2">[Note2]  
Presently IPv6 is not supported. For the connection with ServerView Infrastructure Manager, specify the IP address of IPv4 or host name (FQDN) that are available for name resolution of IPv4.

<a name="note-2-3">[Note3]  
Multiple firmware can be updated at the same time by specifying the multiple firmware.  
In that case, specifies all the same values (either of Online or Offline) for operation_mode.  
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


#### Examples

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

#### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|Ism_firmware_update|string|Always. "Success"|Firmware update result|

#### Return Values (Abnormal)
When the REST-API response of ServerView Infrastructure Manager is an error.


|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information on the date and time when the corresponding message displayed is output.|
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

- Refer to the following URL for the information regarding parameter setting in config file and inventory file.  
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for the information regarding sample playbook using ism_firmware_update.  
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_update.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_update.yml)
- Refer to the following URL for the information regarding sample playbook using ism_firmware_online_update.  
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_online_update.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_online_update.yml)
- Refer to the following URL for the information regarding sample playbook using ism_firmware_offline_update.  
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_offline_update.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_offline_update.yml)
- Refer to the following URL for the information regarding sample playbook using ism_firmware_easy_update.  
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_easy_update.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_easy_update.yml)

---

<a name="ism_maintenance_mode_setting">ism_maintenance_mode_setting
-----------------

Changing from/to Maintenance Mode



#### Synopsis

Changes the maintenance mode of a node.  
A node with its maintenance mode in "Maintenance" cannot perform retrieval of node information for monitoring and regular schedule or notification of events.


#### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0


#### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:-:|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation. <br>[[Note1]](#note-3-1) [[Note2]](#note-3-2)|
|mode|〇|None|・On<br>・Off|Maintenance mode<br>“On”： Setting<br>“Off”： Release|

<a name="note-3-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of operation node registered in ServerView Infrastructure Manager.    
When the OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-3-2">[Note2]  
Presently IPv6 is not supported. For the connection with ServerView Infrastructure Manager,  
specify the IP address of IPv4 or host name (FQDN) that are available for name resolution of IPv4.


#### Examples

```yaml
- name: Set Maintenance Mode
   ism_maintenance_mode_setting:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    mode: "On"
   register: ism_maintenance_mode_setting_result
- debug: var=ism_maintenance_mode_setting_result
```

#### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|ism_maintenance_mode|string|Always "Success"|Maintenance mode setting result|

#### Return Values (Abnormal)

When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output|
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

- Refer to the following URL for the information regarding parameter setting in config file and inventory file.  
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for the information regarding sample playbook using ism_maintenance_mode.  
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_update.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_firmware_update.yml)

---

<a name="ism_profile_assignment">ism_profile_assignment
-----------------

Assigning Profiles for Nodes



#### Synopsis

Assigns specified profiles for the specified nodes managed by ServerView Infrastructure Manager.


#### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0


#### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:-:|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation.<br>[[Note1]](#note-4-1) [[Note2]](#note-4-2)|
|ism_profile_name|〇|None|None|Profile name.|
|assign_mode|-|None|・Normal<br>・Advanced|Specifies assign mode.<br>- Normal: Usual assignment<br>- Advanced: Advanced assignment<br>When this setting is omitted or null, operations will be carried out as Normal.<br>[[Note3]](#note-4-3) |
|advanced_kind|-|None|・ForcedAssign<br>・WithoutHardwareAccess<br>・OnlineAssign|Specifies the assign profile name for operation node. Refer to [[Table1]](#table-4-1) for the combination that can be specified.<br>Specifies type of advanced application.<br>To be specified when the AssignMode is 'Advanced'.<br>- ForcedAssign: Forced assignment<br>- WithoutHardwareAccess: The application intended to be applied<br>- OnlineAssign: Online assignment<br>ForcedAssign cannot be used in first-time application.<br>When IOVirtualization or OSInstallation is included in the AssignRange, OnlineAssign cannot be used.|
|assign_range|-|None|・BIOS<br>・iRMC<br>・MMB<br>・IOVirtualization<br>・OSInstallation|Records types of Profile for assignment.<br>If the AssignMode is Advanced, "BIOS," "iRMC," "MMB,"<br>"IOVirtualization" and/or "OSInstallation" can be specifiedeither individually or together.<br>E.g.) ["BIOS","iRMC"]<br>When this setting is omitted or null, all types of profile in ProfileData are assigned.<br>Refer to [[Table1]](#table-4-1) for the combination that can be specified.|

<a name="note-4-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of operation node registered in ServerView Infrastructure Manager.  
When the OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-4-2">[Note2]  
Presently IPv6 is not supported. For the connection with ServerView Infrastructure Manager,   
specify the IP address of IPv4 or host name (FQDN) that are available for name resolution of IPv4.

<a name="note-4-3">[Note3]  
Specify the Normal for the usual assignment.  
Specify the Advanced for the advanced assignment.  
For the usual assignment and advanced assignment, refer to "2.2.3 Profile Management" in "FUJITSU Software ServerView Infrastructure Manager V2.2 User's Manual".  
http://www.fujitsu.com/jp/products/software/infrastructure-software/infrastructure-software/serverviewism/technical/index.html

<a name="table-4-1">[Table 1]

|assign_mode|advanced_kind|assign_range|
|:--|:--|:--|
|Normal|Cannot be specified<br>(Even if specified, it will be disregarded)|Cannot be specified<br>(Even if specified, it will be disregarded)|
|Advanced|ForcedAssign<br>(It can be specified, only when the profile has been applied.) (*2)|・BIOS<br>・iRMC<br>・MMB<br>・IOVirtualization|
|Advanced|WithoutHardwareAccess|・BIOS<br>・iRMC<br>・MMB<br>・IOVirtualization<br>・OSInstallation|
|Advanced|OnlineAssign|・BIOS<br>・iRMC<br>・MMB|

(*2)  
When the profile is unassigned and if you specify the ForcedAssign, REST-API returns the error.

【Example 1】  

```yaml
- name: Execution of ism_profile_assignment
   ism_profile_assignment:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    ism_profile_name: "profileA"
   register: ism_profile_assignment_result
- debug: var=ism_profile_assignment_result
```

【Example 2】  
A case of specified value of the assign_range is only one.

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

【Example 3】  
A case of specified value of the assign_range is two or more.

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


#### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|ism_profile_assignment|string|Always. "Success"|Profile assignment result|

#### Return Values (Abnormal)
When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are<br>output.<br>If there is no information available, only the key names are output|
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

- Refer to the following URL for the information regarding parameter setting in config file and inventory file.  
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for the information regarding sample playbook using ism_profile_assignment.  
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_profile_assignment.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_profile_assignment.yml)

---

<a name="ism_power_on">ism_power_on
-----------------

Instruction for Power-on



#### Synopsis

Instructions for Power-on of the specified nodes managed by ServerView Infrastructure Manager.


#### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0


#### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:-:|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation. [[Note1]](#note-5-1) [[Note2]](#note-5-2)

<a name="note-5-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in ServerView Infrastructure Manager is specified.   
When the OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-5-2">[Note2]  
Presently IPv6 is not supported. For the connection with ServerView Infrastructure Manager,   
specify the IP address of IPv4 or host name (FQDN) that are available for the name resolution of IPv4.

#### Examples

```yaml
- name: Execution of ism_power_on
   ism_power_on:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
   register: ism_power_on_result
- debug: var=ism_power_on_result
```







#### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|ism_power_on|string|Always. "Success"|The execution result of power supply On is output.|

#### Return Values (Abnormal)
When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output|
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

- Refer to the following URL for the information regarding parameter setting in config file and inventory file<br>[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for the information regarding sample playbook using ism_power_on<br>[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_power_controls.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_power_controls.yml)
 
---
<a name="#ism_refresh_node_info">ism_refresh_node_info
------------------
Refreshing Node Information



#### Synopsis

Refreshes the node information of the nodes managed by ServerView Infrastructure Manager.  
It is used to refresh the inventory information, such as after a firmware update.


#### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0


#### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:-:|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation. <br>[[Note1]](#note-6-1) [[Note2]](#note-6-2)

<a name="note-6-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in ServerView Infrastructure Manager.   
When the OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-6-2">[Note2]  
Presently IPv6 is not supported. For the connection with ServerView Infrastructure Manager,  
specify the IP address of IPv4 or host name (FQDN) that are available for name resolution of IPv4.


#### Examples

```yaml
- name: Execution of ism_refresh_node_info
   ism_refresh_node_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.25"
   register: ism_refresh_node_info_result
- debug: var=ism_refresh_node_info_result
```

#### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|ism_refresh_node_info|string|Always "Success"|Node information refreshing result are output.|

#### Return Values (Abnormal)
When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType are output.|
|IsmBody|dict|Always.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|
|ContinueKey|string|If the applicable log exceeds 1000 as the search result, it outputs the value. If the search result is 1000 or less, it outputs null.|Continued Read Key|
|Logs|dict-list|Always.|List of Log Information|
|Id|string|Always.|Log ID<br>Range: 1-999999|
|Level|string|Always.|Importance|
|Message|string|Always, but can be null.|Message|
|MessageId|string|Always.|Message ID|
|OccurrenceDate|string|Always.|Time and date of occurence<br>YYYY-MM-DDThh:mm:ss.xxxZ (date:year-month-day,<br>time:hour-minute-second-millisecond. T and Z represent both<br>separator characters and UTC in ISO8601 format.)|
|Operator|string|Always, but can be null.|Operator|
|TargetInfo|dict|Always, but can be null.|Target Information|
|Name|string|Always.|Resource name|
|ResourceId|integer|Always.|Resource name|
|ResourceIdType|string|Always.|Type of Resource ID|
|Type|string|Always.|Types of Operation Logs|
|RowCounter|integer|Always.|Total Search Queries|
|MessageInfo|dict-list|Always.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output |
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message displayed is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|SchemaType|string|Always.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|


Case except the above.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|string|Always, but can be null.|Message except API processing results|

#### Notes

- Refer to the following URL for the information regarding parameter setting in config file and inventory file.  
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for the information regarding sample playbook using ism_refresh_node_info.  
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_refresh_node_info.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_refresh_node_info.yml)

---

<a name="ism_get_inventory_info">ism_get_inventory_info
-----------------

Retrieving Inventory Information



#### Synopsis

Retrieves the detailed inventory information of the nodes managed by ServerView Infrastructure Manager.

It is used to retrieve the firmware information, such as after a firmware is update.

#### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0


#### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:-:|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation. [[Note1]](#note-7-1) [[Note2]](#note-7-2)|
|level|-|All|・Top<br>・All|Retrieves process level<br><br>Assigns if VariableData should be obtained. Unless specified, it operates by All.[[Note3]](#note-7-3)<br><br>-Top: No information on VariableData<br>-All:VariableData available|
|target|-|None|Type of detailed information [[Note3]](#note-7-3)|Specifystype of detailed information<br><br>Assign parameters inside VariableData. Displays only specified information. Specify All for the retrieving process level. [[Note3]](#note-7-3)<br><br>Example of assignment)<br>/nodes/{nodeid}/inventory?level=All&target=Firmware -><br>Displays only Firmware in VariableData.|

<a name="note-7-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in ServerView Infrastructure Manager is specified.  
When the OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-7-2">[Note2]  
Presently IPv6 is not supported. For the connection with ServerView Infrastructure Manager,  
specify the IP address of IPv4 or host name (FQDN) that are available for the name resolution of IPv4.

<a name="note-7-3">[Note3]  
For details, refer to "4.6.3 Separate Retrieval for Nodes Detailed Information" in "FUJITSU Software ServerView Infrastructure Manager V2.2 REST API Reference Manual".  
[http://www.fujitsu.com/jp/products/software/infrastructure-software/infrastructure-software/serverviewism/technical/index.html](http://www.fujitsu.com/jp/products/software/infrastructure-software/infrastructure-software/serverviewism/technical/index.html)

【Example 1】  
Case in specifying "Top"(not retrieving the detailed information)

```yaml
- name: Execution of ism_get_inventory_info
   ism_get_inventory_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    level: "Top"
   register: ism_get_inventory_info_result
- debug: var=ism_get_inventory_info_result
```

【Example 2】  
Case in specifying "All" (retrieving all the detailed information)

```yaml
- name: Execution of ism_get_inventory_info
   ism_get_inventory_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    level: "All"
   register: ism_get_inventory_info_result
- debug: var=ism_get_inventory_info_result
```

【Example 3】  
Case in specifying “level=All&target=Firmware” (retrieving the detailed information of firmware)

```yaml
- name: Execution of ism_get_inventory_info
   ism_get_inventory_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    level: "All"
    target: "Firmware"
   register: ism_get_inventory_info_result
- debug: var=ism_get_inventory_info_result
```


#### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|ism_get_inventory_info|dict|Always.|Retrieval result of the Inventory Information|
|IsmBody|dict|Always.|API processing results|
|Node|dict|Always.|Node detailed information|
|HardwareLogTarget|integer|Always.|Node log collection availability-disavailability information<br>Used in log management function.<br>- 0: Disable<br>- 1: Enable<br>|
|MacAddress|string|Always, but can be null.|MAC address of a node|
|Manufacture|string|Always, but can be null.|Vendor Name|
|Name|string|Always, but can be null.|System name|
|NodeId|integer|Always.|Node ID|
|ProductName|string|Always, but can be null.|Product Name|
|Progress|string|Always.|Progress of Retrieval of Node Information<br>- Updating: During retrieval. Displays the information<br>retrieved last time.<br>- Complete: Retrieval finished Displays the most up-todated information.<br>- Error: Failed to retrieve information. Information will not be renewed.|
|RaidLogTarget|integer|Always.|RAID Log Collection Possibility Information<br>Used in log management function.<br>- 0: Disable<br>- 1: Enable|
|SerialNumber|string|Always, but can be null.|Serial Number|
|ServerViewLogTarget|integer|Always.|ServerView Log Collection Availability-Unavailability<br>Information<br>Used in log management function.<br>- 0: Disable<br>- 1: Enable|
|SoftwareLogTarget|integer|Always.|OS Log Collection Possibility Information<br>Used in log management function.<br>- 0: Disable<br>- 1: Enable|
|UpdateDate|string|Always.|Update time and date|
|VariableData|dict|Always.|Detailed Information<br>When level is all, it is output.<br>Can omit the key when level is Top.<br>[[Note3]](#note-7-3)|
|MessageInfo|dict-list|Always.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message displayed is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|SchemaType|string|Always.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|


#### Return Values (Abnormal)
When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message displayed is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|IsmBody|dict|Always, but can be null.|API processing results|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|

Case other than the above.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|string|Always, but can be null.|Message except API processing results|

#### Notes

- Refer to the following URL for the information regarding the parameter setting in config file and inventory file.  
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for the information regarding sample playbook using ism_get_inventory_info.  
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_get_inventory_info.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_get_inventory_info.yml)
                                                                                         
---

<a name="ism_get_profile_info">ism_get_profile_info
-----------------

Retrieving Profile Information



#### Synopsis

Retrieves the profile information of the ISM managed nodes.  
It is used to confirm the profile information assigned in the node, such as after the profile is assigned.

#### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0


#### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:-:|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation. [[Note1]](#note-8-1)[[Note2]](#note-8-2)
|status|-|None|・assigned<br>・mismatch<br>・processing<br>・canceling<br>・canceled<br>・error|Specifies the assigned status<br>- assigned: assignment complete<br>- mismatch: status that existing assigned profile was edited but the setting was not yet assigned. (there is a difference between the profile and the device)<br><br>(there is a difference between the profile and the device)<br>- processing: 'assigned/unassigned' processing in progress<br>- canceling: cancellation of 'assigned/unassigned' is in progress<br>- canceled: cancellation of 'assigned/unassigned' is complete<br>- error: 'assigned/unassigned' has failed<br>If Choice is not specified, the profile information of the operation target node is output regardless of the assigned status of the profile.|

<a name="note-8-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in ServerView Infrastructure Manager is specified.  
When the OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-8-2">[Note2]  
Presently IPv6 is not supported. For the connection with ServerView Infrastructure Manager,  
specify the IP address of IPv4 or host name (FQDN) that are available for the name resolution of IPv4.

 

【Example】  
When retrieving the assigned profile information.

```yaml
- name: Getting Profile Information
   ism_get_profile_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    status: "assigned"
   register: ism_get_profile_info_result
- debug: var=ism_get_profile_info_result
```

#### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|ism_get_profile_info|dict|Always.|Retrieval result of the profile Information|
|IsmBody|dict|Always.|API processing results|
|ProfileList|dict-list|Always.|Profile List<br>The maximum value is 1000.|
|AssignedNodeId|integer|Always.|Node ID Assigned|
|CategoryId|string|Always.|Category ID|
|Description|string|Always.|Description of Profile|
|HistoryList|dict-list|Always, but can be null.|When editing is carried out during assignment, the profile as it was before editing is returned.<br>The maximum value is 1.|
|ProfileId|string|Always.|When editing is carried out during assignment, the profile as it was before editing is returned.|
|InternalStatus|dict|Always.|Internal Status|
|BiosStatus|string|Always.|Displays the assignment status for BIOS Profiles.<br>- invalid: profile unregistered<br>- unassigned: profile not yet assigned<br>- assigned: profile assignment complete<br>- reassign: profile update available<br>- processing: assignment in process<br>If there is no output result, the keys will be omitted.|
|IovStatus|string|Always.|Displays the assignment status for IOVirtualization<br>profiles.<br>- invalid: profile unregistered<br>- unassigned: profile not yet assigned<br>- assigned: profile assignment complete<br>- reassign: profile update available<br>- processing: assignment in process<br>If there is no output result, the keys will be omitted.|
|IrmcStatus|string|Always.|Displays the assignment status for iRMC Profiles.<br>- invalid: profile unregistered<br>- unassigned: profile not yet assigned<br>- assigned: profile assignment complete<br>- reassign: profile update available<br>- processing: assignment in process<br>Output when the CategoryId is 1(Server-BX), 2(Server-CX), 3(Server-RX), or 5(Server-PRIMEQUEST3000B).<br>If there is no output result, the keys will be omitted.|
|MmbStatus|string|Always.|Displays the assignment status for MMB Profiles.<br>- invalid: profile unregistered<br>- unassigned: profile not yet assigned<br>- assigned: profile assignment complete<br>- reassign: profile update available<br>- processing: assignment in process<br>Output when the CategoryId is 4(Server-PRIMEQUEST2000-Partition) or 6(Server-PRIMEQUEST3000E-Partition).<br>If there is no output result, the keys will be omitted.|
|OsStatus|string|Always.|Displays the assignment status for OS Profiles.<br>- invalid: profile unregistered<br>- unassigned: profile not yet assigned<br>- assigned: profile assignment complete<br>- reassign: profile update available<br>- processing: assignment in process<br>If there is no output result, the keys will be omitted.|
|PathName|string|Always.|Path Name for this profile group|
|ProfileGroupId|string|Always.|Profile Group ID that it currently belongs to|
|ProfileId|string|Always.|Profile ID|
|ProfileName|string|Always.|Profile Name|
|ReferencePolicyList|dict-list|Always, but can be null.|Policy List used in the succession referenced<br>The maximum value is 2000.|
|PolicyId|string|Always.|Policy ID used in the succession referenced|
|Status|string|Always.|Displays the assigned status.<br>- assigned: assignment complete<br>- mismatch: an assigned profile is edited and takes on unassigned status (there is a finite difference between the profile and the device)<br>- processing: 'assigned/unassigned' processing in progress<br>- canceling: cancellation of 'assigned/unassigned' is in progress<br>- canceled: cancellation of  assigned/unassigned' is complete<br>- error: 'assigned/unassigned' has failed|
|TimeStampInfo|dict|Always.|Time Stamp Information|
|Assigned|string|Always, but can be null.|Time of Last Assignment|
|Register|string|Always.|Registration Time|
|Update|string|Always.|Time of Last Update|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message displayed is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|


#### Return Values (Abnormal)
When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message displayed is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|IsmBody|dict|Always, but can be null.|API processing results|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|

Case other than the above.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|string|Always, but can be null.|Message except API processing results|
#### Notes

- Refer to the following URL for the information regarding the parameter setting in config file and inventory file.  
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for the information regarding sample playbook using ism_get_profile_info.  
[https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_get_profile_info.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_get_profile_info.yml)

---

<a name="ism_get_power_status">ism_get_power_status
-----------------

Retrieving Power Status


#### Synopsis

Retrieves the power status of the ISM managed node.  
It is used to confirm the power status of the node, such as after the operation of power.

#### Requirements

- Ansible >= 2.4.0.0
- python >= 2.6
- ServerView Infrastructure Manager >= 2.2.0


#### Options

|Parameter|Required|Default|Choices|Comments|
|:--|:-:|:--|:--|:--|
|config|〇|None|None|Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.|
|hostname|〇|None|None|Specifies the IP address and host name of the operation. [[Note1] ](#note-9-1)[[Note2]](#note-9-2)|

<a name="note-9-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in ServerView Infrastructure Manager is specified.  
When the OS information of the operation node is registered in ServerView Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-9-2">[Note2]  
Presently IPv6 is not supported. For the connection with ServerView Infrastructure Manager,  
specify the IP address of IPv4 or host name (FQDN) that are available for the name resolution of IPv4.

 

【Example】

```yaml
- name: Getting Power Status
   ism_get_power_status:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
   register: ism_get_power_status_result
- debug: var=ism_get_power_status_result
```

#### Return Values (Normal)

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|ism_get_power_status|dict|Always.|Retrieval result of the power status information|
|IsmBody|dict|Always.|API processing results|
|Parts|dict-list|Always, but can be null.|List of Power Sources|
|Name|string|Always.|Name of Power Source<br>Sets PowerManagement.|
|PowerChoices|string-list|Always, but can be null.|Choices of Power Sources<br>All choices that are operational are set. The choices are<br>PowerOn, Reset, and Shutdown.<br>Operational choices other than PowerOn, Reset, and Shutdown are different according to the node.<br>It becomes an empty list ([ ]) when it is unable to operate.|
|PowerStatus|string|Always, but can be null.|Status of Power Sources<br>The value of either On, Off, Standby or Unknown is set.|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output.|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message displayed is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|


#### Return Values (Abnormal)
When the REST-API response of ServerView Infrastructure Manager is an error.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|dict|Always, but can be null.|MessageInfo, IsmBody, and SchemaType|
|MessageInfo|dict-list|Always, but can be null.|Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output|
|Timestamp|string|Always, but can be null.|Date & time information<br>Information of the date and time when the corresponding message displayed is output.|
|MessageId|string|Always, but can be null.|Message ID<br>A unique ID is output for each message.|
|API|string|Always, but can be null.|API type<br>The API type is output in the format "Method name URI".|
|Message|string|Always, but can be null.|API processing results<br>API processing results are output as response parameters.|
|IsmBody|dict|Always, but can be null.|API processing results|
|SchemaType|string|Always, but can be null.|The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.|

Case other than the above.

|Name|Type|Returned|Description|
|:--|:--|:--|:--|
|msg|string|Always, but can be null.|Message except API processing results|

#### Notes

- Refer to the following URL for the information regarding the parameter setting in config file and inventory file.  
[https://github.com/fujitsu/ism-ansible/blob/master/Readme.md](https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)
- Refer to the following URL for the information regarding sample playbook using ism_get_power_status.  
  [https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_get_power_status.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_get_power_status.yml)  
  [https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_power_on_and_wait.yml](https://github.com/fujitsu/ism-ansible/blob/master/examples/ism_power_on_and_wait.yml)
