# Ansible Fujitsu Infrastructure Manager Modules

## Modules

* [ism_firmware_list - List Applicable Firmware.](#ism_firmware_list)
* [ism_firmware_update - Firmware Updates.](#ism_firmware_update)
* [ism_maintenance_mode_setting - Changing from/to Maintenance Mode.](#ism_maintenance_mode_setting)
* [ism_profile_assignment - Assigning Profiles to Nodes.](#ism_profile_assignment)
* [ism_power_on - Instruction to Power-on.](#ism_power_on)
* [ism_refresh_node_info - Refreshing Node Information.](#ism_refresh_node_info)
* [ism_get_inventory_info - Retrieving Inventory Information.](#ism_get_inventory_info)
* [ism_get_profile_info - Retrieving Profile Information.](#ism_get_profile_info)
* [ism_get_power_status - Retrieving Power Status.](#ism_get_power_status)
* [ism_retrieve_download_firmware_info - Retrieving Download Firmware Info.](#ism_retrieve_download_firmware_info)
* [ism_get_download_firmware_list - Retrieving Download Firmware List.](#ism_get_download_firmware_list)
* [ism_download_firmware - Downloading Firmware.](#ism_download_firmware)
* [ism_get_report_info - Retrieving Report Information.](#ism_get_report_info)
* [ism_backup - Backing up ISM-VA.](#ism_backup)
* [ism_copy_profile - Copying Profile.](#ism_copy_profile)

## <a name="ism_firmware_list">ism_firmware_list

List Applicable Firmware

### Synopsis

Retrieves the summary of the applicable firmware registered to Infrastructure Manager.  
The list of retrieved information is specified for the parameter of firmware update module (ism_firmware_update.py).

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.2.0

### Options

<table>
<tbody>
<tr>
  <th>Parameter</th>
  <th>Type</th>
  <th>Required</th>
  <th>Essential Mode</th>
  <th>Default</th>
  <th>Choices</th>
  <th>Comments</th>
</tr>
<tr>
  <td>config</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Specifies the full path for the described setting file of the connection information of Infrastructure Manager.</td>
</tr>
<tr>
  <td>hostname</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Specifies the IP address and te host name of the operation.<br><a href="#note-1-1">[Note1]</a> <a href="#note-1-2">[Note2]</a></td>
</tr>
<tr>
  <td>firmware_type</td>
  <td>string</td>
  <td align="center">No</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>
    <ul>
      <li>BIOS</li>
      <li>iRMC</li>
      <li>FC</li>
      <li>CNA</li>
      <li>ETERNUS DX</li>
      <li>LAN Switch</li>
    </ul>
  </td>
  <td>When specifies the firmware type, the list of the specified firmware type is output. The list of all firmware is output when omitting it.</td>
</tr>
</tbody>
</table>

<a name="note-1-1">[Note1]  
Specify the IP address of the operation node registered in Infrastructure Manager or the host name (FQDN) for its IP address.  
When the OS information of the operation node that is registered in Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-1-2">[Note2]  
Presently IPv6 is not supported. To the connection with Infrastructure Manager, specify the IP address of IPv4 or the host name (FQDN) that are available for the name resolution of IPv4.

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

<table>
<tbody>
<tr>
  <th colspan="4">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="4">ism_firmware_list</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Retrieval result of the firmware list</td>
</tr>
<tr>
  <td rowspan="19"></td>
  <td colspan="3">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API proccessing results</td>
</tr>
<tr>
  <td rowspan="11"></td>
  <td colspan="2">FirmwareList</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>List of Firmware</td>
</tr>
<tr>
  <td rowspan="10"></td>
  <td>DiskUsage</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Disck capacity used by firmware (MB)</td>
</tr>
<tr>
  <td>FirmwareId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware ID</td>
</tr>
<tr>
  <td>FirmwareName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware Name</td>
</tr>
<tr>
  <td>FirmwareType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware type</td>
</tr>
<tr>
  <td>FirmwareVersion</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware version</td>
</tr>
<tr>
  <td>ModelName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Model name</td>
</tr>
<tr>
  <td>NodeId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Node ID</td>
</tr>
<tr>
  <td>OperationMode</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Supported modes</td>
</tr>
<tr>
  <td>RegisterDate</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Time/date of firmware registration</td>
</tr>
<tr>
  <td>RepositoryName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Repository name</td>
</tr>
<tr>
  <td colspan="3">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="2">Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>The date and time when the message occurred is returned.</td>
</tr>
<tr>
  <td colspan="2">MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>A unique ID is returned for each message.</td>
</tr>
<tr>
  <td colspan="2">API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>REST-API<br>REST-API type is returned in the from of a method name URI.</td>
</tr>
<tr>
  <td colspan="2">Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message<br>The message is returned.</td>
</tr>
<tr>
  <td colspan="3">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.</td>
</tr>
</tbody>
</table>

### Return Values (Abnormal)

When the REST-API response of Infrastructure Manager is an error.

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

Case except the above.

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|msg|string|Yes|Not omitted, but null is allowed.|Message except API processing results.|

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_firmware_list.yml](/examples/ism_firmware_list.yml)

## <a name="ism_firmware_update">ism_firmware_update

Firmware Updates

### Synopsys

Commences updating process firmware registered to Infrastructure Manager.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.2.

### Check Mode

Supported

### Options

<table>
<tbody>
<tr>
  <th colspan="2">Parameter</th>
  <th>Type</th>
  <th>Required</th>
  <th>Essential Mode</th>
  <th>Default</th>
  <th>Choices</th>
  <th>Comments</th>
</tr>
<tr>
  <td colspan="2">config</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Specifies the full path for the described setting file of the connection information of Infrastructure Manager.</td>
</tr>
<tr>
  <td colspan="2">hostname</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Specifies the IP address and the host name of the operation.<br><a href="#note-2-1">[Note1]</a> <a href="#note-2-2">[Note2]</a></td>
</tr>
<tr>
  <td colspan="2">firmware_update_list</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Array data of dictionary type that specifies updated firmware.<br>Firmware_name, repository_name, firmware_version, and operation_mode are specified for an element of this dictionary type.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>firmware_name</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Firmware name<br><a href="#note-2-3">[Note3]</a></td>
</tr>
<tr>
  <td>repository_name</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Repository name<br><a href="#note-2-3">[Note3]</a></td>
</tr>
<tr>
  <td>firmware_version</td>
  <td>string</td>
  <td align="center">No</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Firmware version<br><a href="#note-2-3">[Note3]</a></td>
</tr>
<tr>
  <td>operation_mode</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td><ul><li>Online</li><li>Offline</li></ul></td>
  <td>Supported modes<br>- Online: Online update<br>- Offline: Offline update<br><a href="#note-2-3">[Note3]</a></td>
</tr>
</tbody>
</table>

<a name="note-2-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in Infrastructure Manager.  
When the OS information of the operation node is registered in Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-2-2">[Note2]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager, specify the IP address of IPv4 or host name (FQDN) that are available for the name resolution of IPv4.

<a name="note-2-3">[Note3]  
Multiple firmware can be updated simultaneously by specifying the multiple firmware.
In that case, specifies all the same values (either of Online or Offline) for the operation_mode.
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

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|ism_firmware_update|string|Yes|Not omitted. "Success"|Firmware update result|

### Return Values (Normal, Check mode) 

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|ism_firmware_update|string|Yes|Returns a string with the following format.<br><br>Firmware versions that would be changed: &lt;Firmware string that can be updated<a href="#note-2-4">[Note 4]</a>&gt;|The firmware that can be updated will be returned.|

<a name="note-2-4">[Note4]  
The firmware updatable element in the firmware_update_list specified in the argument is converted to a string and returned. The string also contains the value of the current firmware version as firmware_current_version.

### Return Values (Abnormal)

When the REST-API response of Infrastructure Manager is an error.

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

Case other than the above.

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|msg|string|Yes|Not omitted, but null is allowed.|Message except API processing results|

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbooks.  
  [examples/ism_firmware_update.yml](/examples/ism_firmware_update.yml)  
  [examples/ism_firmware_online_update.yml](/examples/ism_firmware_online_update.yml)  
  [examples/ism_firmware_offline_update.yml](/examples/ism_firmware_offline_update.yml)  
  [examples/ism_firmware_easy_update.yml](/examples/ism_firmware_easy_update.yml)

## <a name="ism_maintenance_mode_setting">ism_maintenance_mode_setting

Changing from/to Maintenance Mode

### Synopsis

Changes the maintenance mode of a node.  
A node with its maintenance mode in "Maintenance" cannot perform retrieval of node information for monitoring and regular schedule or notification of events.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.2.0

### Options

|Parameter|Type  |Required|Essential Mode|Default|Choices                         |Comments                                                                                                       |
|:--------|:-----|:------:|:------------:|:------|:-------------------------------|:--------------------------------------------------------------------------------------------------------------|
|config   |string|Yes     |Yes           |None   |None                            |Specifies the full path for the described setting file of the connection information of Infrastructure Manager.|
|hostname |string|Yes     |Yes           |None   |None                            |Specifies the IP address and the host name of the operation. <br>[[Note1]](#note-3-1) [[Note2]](#note-3-2)     |
|mode     |string|Yes     |Yes           |None   |<ul><li>On</li><li>Off</li></ul>|Maintenance mode<br>"On": Setting<br>"Off": Release                                                            |

<a name="note-3-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in Infrastructure Manager.
When the OS information of the operation node is registered in Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-3-2">[Note2]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager,  
specify the IP address of IPv4 or the host name (FQDN) that are available for the name resolution of IPv4.

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

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|ism_maintenance_mode|string|Yes|Not omitted."Success"|Maintenance mode setting result|

### Return Values (Abnormal)

When the REST-API response of Infrastructure Manager is an error.

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

Case except the above.

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|msg|string|Yes|Not omitted, but null is allowed.|Message except API processing results|

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_firmware_update.yml](/examples/ism_firmware_update.yml)

## <a name="ism_profile_assignment">ism_profile_assignment

Assigning Profiles for Nodes

### Synopsis

Assigns specified profiles for the specified nodes managed by Infrastructure Manager.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.2.0
* Other than Essential. (This module is not approved for use in Essential.)

### Options

|Parameter        |Type  |Required|Essential Mode|Default|Choices                                                                                        |Comments                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|:----------------|:-----|:------:|:------------:|:------|:----------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|config           |string|Yes     |No            |None   |None                                                                                           |Specifies the full path for the described setting file of the connection information of Infrastructure Manager.                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|hostname         |string|Yes     |No            |None   |None                                                                                           |Specifies the IP address and the host name of the operation.<br>[[Note1]](#note-4-1) [[Note2]](#note-4-2)                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|ism_profile_name |string|Yes     |No            |None   |None                                                                                           |Profile name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|assign_mode      |string|No      |No            |None   |<ul><li>Normal</li><li>Advanced</li></ul>                                                      |Specifies assign mode.<br>- Normal: Usual assignment<br>- Advanced: Advanced assignment<br>When this setting is omitted or null, operations will be carried out as Normal.<br>[[Note3]](#note-4-3)                                                                                                                                                                                                                                                                                                                                                  |
|advanced_kind    |string|No      |No            |None   |<ul><li>ForcedAssign</li><li>WithoutHardwareAccess</li><li>OnlineAssign</li></ul>              |Specifies the assign profile name for the operation node. Refer to [[Table1]](#table-4-1) for the combination that can be specified.<br>Specifies type of advanced application.<br>To be specified when the AssignMode is 'Advanced'.<br>- ForcedAssign: Forced assignment<br>- WithoutHardwareAccess: The application intended to be applied<br>- OnlineAssign: Online assignment<br>ForcedAssign cannot be used in first-time application.<br>When IOVirtualization or OSInstallation is included in the AssignRange, OnlineAssign cannot be used.|
|assign_range     |string|No      |No            |None   |<ul><li>BIOS</li><li>iRMC</li><li>MMB</li><li>IOVirtualization</li><li>OSInstallation</li></ul>|Records types of Profile for assignment.<br>If the AssignMode is Advanced, "BIOS," "iRMC," "MMB,"<br>"IOVirtualization" and/or "OSInstallation" can be specifiedeither individually or together.<br>E.g.) ["BIOS","iRMC"]<br>When this setting is omitted or null, all types of profile in ProfileData are assigned.<br>Refer to [[Table1]](#table-4-1) for the combination that can be specified.                                                                                                                                                  |

<a name="note-4-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in Infrastructure Manager.  
When the OS information of the operation node is registered in Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-4-2">[Note2]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager, specify the IP address of IPv4 or the host name (FQDN) that are available for the name resolution of IPv4.

<a name="note-4-3">[Note3]  
Specify the Normal for the usual assignment.  
Specify the Advanced for the advanced assignment.  
For the usual assignment and advanced assignment, refer to "2.2.3 Profile Management" in "FUJITSU Software Infrastructure Manager V2.2 User's Manual".  
<http://www.fujitsu.com/jp/products/software/infrastructure-software/infrastructure-software/serverviewism/technical/index.html>

<a name="table-4-1">[Table 1]

|assign_mode|advanced_kind|assign_range|
|:--|:--|:--|
|Normal|Cannot be specified<br>(Even if specified, it will be disregarded)|Cannot be specified<br>(Even if specified, it will be disregarded)|
|Advanced|ForcedAssign<br>(It can be specified, only when the profile has been applied.) (*2)|<ul><li>BIOS</li><li>iRMC</li><li>MMB</li><li>IOVirtualization</li></ul>|
|Advanced|WithoutHardwareAccess|<ul><li>BIOS</li><li>iRMC</li><li>MMB</li><li>IOVirtualization</li><li>OSInstallation</ul>|
|Advanced|OnlineAssign|<ul><li>BIOS</li><li>iRMC</li><li>MMB</li></ul>|

(\*2)  
When the profile is unassigned and if you specify the ForcedAssign, REST-API returns the error.

### Examples

#### Example 1

```yaml
- name: Execution of ism_profile_assignment
  ism_profile_assignment:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    ism_profile_name: "profileA"
  register: ism_profile_assignment_result
- debug: var=ism_profile_assignment_result
```

#### Example 2

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

#### Example 3

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

### Return Values (Normal)

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|ism_profile_assignment|string|No|Not omitted. "Success"|Profile assignment result|

### Return Values (Abnormal)

When the REST-API response of Infrastructure Manager is an error.

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

Case except the above.

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|msg|string|No|Not omitted, but null is allowed.|Message except API processing results|

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_profile_assignment.yml](/examples/ism_profile_assignment.yml)

## <a name="ism_power_on">ism_power_on

Instruction for Power-on

### Synopsis

Instructions for Power-on of the specified nodes managed by Infrastructure Manager.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.2.0

### Options

|Parameter|Type  |Required|Essential Mode|Default|Choices|Comments                                                                                                       |
|:--------|:-----|:------:|:------------:|:------|:------|:--------------------------------------------------------------------------------------------------------------|
|config   |string|Yes     |Yes           |None   |None   |Specifies the full path for the described setting file of the connection information of Infrastructure Manager.|
|hostname |string|Yes     |Yes           |None   |None   |Specifies the IP address and the host name of the operation. [[Note1]](#note-5-1) [[Note2]](#note-5-2)         |

<a name="note-5-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in Infrastructure Manager is specified.
When the OS information of the operation node is registered in Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-5-2">[Note2]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager, specify the IP address of IPv4 or the host name (FQDN) that are available for the name resolution of IPv4.

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

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|ism_power_on|string|Yes|Not omitted. "Success"|The execution result of power supply On is output.|

### Return Values (Abnormal)

When the REST-API response of Infrastructure Manager is an error.

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

Case except the above.

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|msg|string|Yes|Not omitted, but null is allowed.|Message except API processing results|

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_power_controls.yml](/examples/ism_power_controls.yml)

## <a name="ism_refresh_node_info">ism_refresh_node_info

Refreshing Node Information

### Synopsis

Refreshes the node information of the nodes managed by Infrastructure Manager.  
It is used to refresh the inventory information, such as after a firmware update.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.2.0

### Options

|Parameter|Type  |Required|Essential Mode|Default|Choices|Comments                                                                                                       |
|:--------|:-----|:------:|:------------:|:------|:------|:--------------------------------------------------------------------------------------------------------------|
|config   |string|Yes     |Yes           |None   |None   |Specifies the full path for the described setting file of the connection information of Infrastructure Manager.|
|hostname |string|Yes     |Yes           |None   |None   |Specifies the IP address and the host name of the operation. <br>[[Note1]](#note-6-1) [[Note2]](#note-6-2)     |

<a name="note-6-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in Infrastructure Manager.
When the OS information of the operation node is registered in Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-6-2">[Note2]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager,  
specify the IP address of IPv4 or the host name (FQDN) that are available for the name resolution of IPv4.

### Examples

```yaml
- name: Execution of ism_refresh_node_info
  ism_refresh_node_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.25"
  register: ism_refresh_node_info_result
- debug: var=ism_refresh_node_info_result
```

### Return Values (Normal)

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|ism_refresh_node_info|string|Yes|Not omitted."Success"|Node information refreshing result are output.|

### Return Values (Abnormal)

When the REST-API response of Infrastructure Manager is an error.

<table>
<tbody>
<tr>
  <th colspan="5">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="5">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType are output.</td>
</tr>
<tr>
  <td rowspan="21"></td>
  <td colspan="4">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.</td>
</tr>
<tr>
  <td rowspan="14"></td>
  <td colspan="3">ContinueKey</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>If the applicable log exceeds 1000 as the search result, it outputs the value. If the search result is 1000 or less, it outputs null.</td>
  <td>Continued Read Key</td>
</tr>
<tr>
  <td colspan="3">Logs</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>List of Log Information</td>
</tr>
<tr>
  <td rowspan="11"></td>
  <td colspan="2">Id</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Log ID<br>Range: 1-999999</td>
</tr>
<tr>
  <td colspan="2">Level</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Importance</td>
</tr>
<tr>
  <td colspan="2">Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message</td>
</tr>
<tr>
  <td colspan="2">MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Message ID</td>
</tr>
<tr>
  <td colspan="2">OccurrenceDate</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Time and date of occurence<br>YYYY-MM-DDThh:mm:ss.xxxZ (date:year-month-day,<br>time:hour-minute-second-millisecond. T and Z represent both<br>separator characters and UTC in ISO8601 format.)</td>
</tr>
<tr>
  <td colspan="2">Operator</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Operator</td>
</tr>
<tr>
  <td colspan="2">TargetInfo</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Target Information</td>
</tr>
<tr>
  <td rowspan="3"></td>
  <td>Name</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Resource name</td>
</tr>
<tr>
  <td>ResourceId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Resource ID</td>
</tr>
<tr>
  <td>ResourceIdType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Type of Resource ID</td>
</tr>
<tr>
  <td colspan="2">Type</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Types of Operation Logs</td>
</tr>
<tr>
  <td colspan="3">RowCounter</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Total Search Queries</td>
</tr>
<tr>
  <td colspan="4">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="3">Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information of the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td colspan="3">MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>A unique ID is output for each message.</td>
</tr>
<tr>
  <td colspan="3">API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td colspan="3">Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="4">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.</td>
</tr>
</tbody>
</table>

Case except the above.

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|msg|string|Yes|Not omitted, but null is allowed.|Message except API processing results|

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_refresh_node_info.yml](/examples/ism_refresh_node_info.yml)

## <a name="ism_get_inventory_info">ism_get_inventory_info

Retrieving Inventory Information

### Synopsis

Retrieves the detailed inventory information of the nodes managed by Infrastructure Manager.

It is used to retrieve the firmware information, such as after a firmware is update.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.2.0

### Options

|Parameter|Type  |Required|Essential Mode|Default|Choices                                          |Comments                                                                                                                                                                                                                                                                                                                       |
|:--------|:-----|:------:|:------------:|:------|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|config   |string|Yes     |Yes           |None   |None                                             |Specifies the full path for the described setting file of the connection information of Infrastructure Manager.                                                                                                                                                                                                                |
|hostname |string|Yes     |Yes           |None   |None                                             |Specifies the IP address and the host name of the operation. [[Note1]](#note-7-1) [[Note2]](#note-7-2)                                                                                                                                                                                                                         |
|level    |string|No      |Yes           |All    |<ul><li>Top</li><li>All</li></ul>                |Retrieves process level<br><br>Assigns if VariableData should be obtained. Unless specified, it operates by All.[[Note3]](#note-7-3)<br><br>-Top: No information on VariableData<br>-All:VariableData available                                                                                                                |
|target   |string|No      |Yes           |None   |Type of detailed information [[Note3]](#note-7-3)|Specifies type of detailed information<br><br>Assign parameters inside VariableData. Displays only specified information. Specify All for the retrieving process level. [[Note3]](#note-7-3)<br><br>Example of assignment)<br>/nodes/{nodeid}/inventory?level=All&target=Firmware -><br>Displays only Firmware in VariableData.|

<a name="note-7-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in Infrastructure Manager is specified.  
When the OS information of the operation node is registered in Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-7-2">[Note2]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager,  
specify the IP address of IPv4 or the host name (FQDN) that are available for the name resolution of IPv4.

<a name="note-7-3">[Note3]  
For details, refer to "4.6.3 Separate Retrieval for Nodes Detailed Information" in "FUJITSU Software Infrastructure Manager V2.2 REST API Reference Manual".  
<http://www.fujitsu.com/jp/products/software/infrastructure-software/infrastructure-software/serverviewism/technical/index.html>

### Example 1

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

### Example 2

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

### Example 3

Case in specifying "level=All&target=Firmware" (retrieving the detailed information of firmware)

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

### Return Values (Normal)

<table>
<tbody>
<tr>
  <th colspan="4">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="4">ism_get_inventory_info</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Retrieval result of the Inventory Information</td>
</tr>
<tr>
  <td rowspan="21"></td>
  <td colspan="3">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>API processing results</td>
</tr>
<tr>
  <td rowspan="14"></td>
  <td colspan="2">Node</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node detailed information</td>
</tr>
<tr>
  <td rowspan="13"></td>
  <td>HardwareLogTarget</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Node log collection availability-disavailability information<br>Used in log management function.<br>- 0: Disable<br>- 1: Enable</td>
</tr>
<tr>
  <td>MacAddress</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MAC address of a node</td>
</tr>
<tr>
  <td>Manufacture</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Vendor Name</td>
</tr>
<tr>
  <td>Name</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>System name</td>
</tr>
<tr>
  <td>NodeId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node ID</td>
</tr>
<tr>
  <td>ProductName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Product Name</td>
</tr>
<tr>
  <td>Progress</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Progress of Retrieval of Node Information<br>- Updating: During retrieval. Displays the information<br>retrieved last time.<br>- Complete: Retrieval finished Displays the most up-todated information.<br>- Error: Failed to retrieve information. Information will not be renewed.</td>
</tr>
<tr>
  <td>RaidLogTarget</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>RAID Log Collection Possibility Information<br>Used in log management function.<br>- 0: Disable<br>- 1: Enable</td>
</tr>
<tr>
  <td>SerialNumber</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Serial Number</td>
</tr>
<tr>
  <td>ServerViewLogTarget</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>ServerView Log Collection Availability-Unavailability<br>Information<br>Used in log management function.<br>- 0: Disable<br>- 1: Enable</td>
</tr>
<tr>
  <td>SoftwareLogTarget</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>OS Log Collection Possibility Information<br>Used in log management function.<br>- 0: Disable<br>- 1: Enable</td>
</tr>
<tr>
  <td>UpdateDate</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Update time and date</td>
</tr>
<tr>
  <td>VariableData</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Detailed Information<br>When level is all, it is output.<br>Can omit the key when level is Top.<br><a href="#note-7-3">[Note3]</a></td>
</tr>
<tr>
  <td colspan="3">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="2">Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information of the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td colspan="2">MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>A unique ID is output for each message.</td>
</tr>
<tr>
  <td colspan="2">API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td colspan="2">Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="3">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.</td>
</tr>
</tbody>
</table>

### Return Values (Abnormal)

When the REST-API response of Infrastructure Manager is an error.

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

Case other than the above.

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|msg|string|Yes|Not omitted, but null is allowed.|Message except API processing results|

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_get_inventory_info.yml](/examples/ism_get_inventory_info.yml)

## <a name="ism_get_profile_info">ism_get_profile_info

Retrieving Profile Information

### Synopsis

Retrieves the profile information of the ISM managed nodes.
It is used to confirm the profile information assigned in the node, such as after the profile is assigned.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.2.0
* Other than Essential. (This module is not approved for use in Essential.)

### Options

|Parameter|Type  |Required|Essential Mode|Default|Choices                                                                                                        |Comments                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|:--------|:-----|:------:|:------------:|:------|:--------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|config   |string|Yes     |No            |None   |None                                                                                                           |Specifies the full path for the described setting file of the connection information of Infrastructure Manager.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|hostname |string|Yes     |No            |None   |None                                                                                                           |Specifies the IP address and the host name of the operation. [[Note1]](#note-8-1)[[Note2]](#note-8-2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|status   |string|No      |No            |None   |<ul><li>assigned</li><li>mismatch</li><li>processing</li><li>canceling</li><li>canceled</li><li>error</li></ul>|Specifies the assigned status<br>- assigned: assignment complete<br>- mismatch: status that existing assigned profile was edited but the setting was not yet assigned. (there is a difference between the profile and the device)<br><br>(there is a difference between the profile and the device)<br>- processing: 'assigned/unassigned' processing in progress<br>- canceling: cancellation of 'assigned/unassigned' is in progress<br>- canceled: cancellation of 'assigned/unassigned' is complete<br>- error: 'assigned/unassigned' has failed<br>If Choice is not specified, the profile information of the operation target node is output regardless of the assigned status of the profile.|

<a name="note-8-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in Infrastructure Manager is specified.  
When the OS information of the operation node is registered in Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-8-2">[Note2]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager,  
specify the IP address of IPv4 or host name (FQDN) that are available for the name resolution of IPv4.

### Examples

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

### Return Values (Normal)

<table>
<tbody>
<tr>
  <th colspan="5">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="5">ism_get_profile_info</td>
  <td>dict</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Retrieval result of the profile Information</td>
</tr>
<tr>
  <td rowspan="30"></td>
  <td colspan="4">IsmBody</td>
  <td>dict</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>API processing results</td>
</tr>
<tr>
  <td rowspan="23"></td>
  <td colspan="3">ProfileList</td>
  <td>dict-list</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Profile List<br>The maximum value is 1000.</td>
</tr>
<tr>
  <td rowspan="22"></td>
  <td colspan="2">AssignedNodeId</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Node ID Assigned</td>
</tr>
<tr>
  <td colspan="2">CategoryId</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Category ID</td>
</tr>
<tr>
  <td colspan="2">Description</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Description of Profile</td>
</tr>
<tr>
  <td colspan="2">HistoryList</td>
  <td>dict-list</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>When editing is carried out during assignment, the profile as it was before editing is returned.<br>The maximum value is 1.</td>
</tr>
<tr>
  <td></td>
  <td>ProfileId</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Profile ID</td>
</tr>
<tr>
  <td colspan="2">InternalStatus</td>
  <td>dict</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Internal Status</td>
</tr>
<tr>
  <td rowspan="5"></td>
  <td>BiosStatus</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Displays the assignment status for BIOS Profiles.
- invalid: profile unregistered<br>- unassigned: profile not yet assigned<br>- assigned: profile assignment complete<br>- reassign: profile update available<br>- processing: assignment in process<br>If there is no output result, the keys will be omitted.</td>
</tr>
<tr>
  <td>IovStatus</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Displays the assignment status for IOVirtualization profiles.<br>- invalid: profile unregistered<br>- unassigned: profile not yet assigned<br>- assigned: profile assignment complete<br>- reassign: profile update available<br>- processing: assignment in process<br>If there is no output result, the keys will be omitted.</td>
</tr>
<tr>
  <td>IrmcStatus</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Displays the assignment status for iRMC Profiles.<br>- invalid: profile unregistered<br>- unassigned: profile not yet ass<br>igned
- assigned: profile assignment complete<br>
- reassign: profile update available<br>- processing: assignment in process
Output when the CategoryId is 1(Server-BX), 2(Server-CX), 3(Server-RX), or 5(Server-PRIMEQUEST3000B).<br>If there is no output result, the keys will be omitted.</td>
</tr>
<tr>
  <td>MmbStatus</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Displays the assignment status for MMB Profiles.<br>- invalid: profile unregistered<br>- unassigned: profile not yet assigned<br>- assigned: profile assignment complete<br>- reassign: profile update available<br>- processing: assignment in process<br>Output when the CategoryId is 4(Server-PRIMEQUEST2000-Partition) or 6(Server-PRIMEQUEST3000E-Partition).<br>
If there is no output result, the keys will be omitted.</td>
</tr>
<tr>
  <td>OsStatus</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Displays the assignment status for OS Profiles.<br>- invalid: profile unregistered<br>- unassigned: profile not yet assigned<br>- assigned: profile assignment complete<br>- reassign: profile update available<br>- processing: assignment in process<br>If there is no output result, the keys will be omitted.</td>
</tr>
<tr>
  <td colspan="2">PathName</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Path Name for this profile group</td>
</tr>
<tr>
  <td colspan="2">ProfileGroupId</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Profile Group ID that it currently belongs to</td>
</tr>
<tr>
  <td colspan="2">ProfileId</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Profile ID</td>
</tr>
<tr>
  <td colspan="2">ProfileName</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Profile Name</td>
</tr>
<tr>
  <td colspan="2">ReferencePolicyList</td>
  <td>dict-list</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Policy List used in the succession referenced<br>The maximum value is 2000.</td>
</tr>
<tr>
  <td></td>
  <td>PolicyId</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Policy ID used in the succession referenced</td>
</tr>
<tr>
  <td colspan="2">Status</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Displays the assigned status.<br>- assigned: assignment complete<br>- mismatch: an assigned profile is edited and takes on unassigned status (there is a finite difference between the profile and the device)<br>- processing: 'assigned/unassigned' processing in progress<br>- canceling: cancellation of 'assigned/unassigned' is in progress<br>- canceled: cancellation of assigned/unassigned' is complete<br>- error: 'assigned/unassigned' has failed</td>
</tr>
<tr>
  <td colspan="2">TimeStampInfo</td>
  <td>dict</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Time Stamp Information</td>
</tr>
<tr>
  <td rowspan="3"></td>
  <td>Assigned</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Time of Last Assignment</td>
</tr>
<tr>
  <td>Register</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Registration Time</td>
</tr>
<tr>
  <td>Update</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Time of Last Update</td>
</tr>
<tr>
  <td colspan="4">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="3">Timestamp</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information of the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td colspan="3">MessageId</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>A unique ID is output for each message.</td>
</tr>
<tr>
  <td colspan="3">API</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td colspan="3">Message</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="4">SchemaType</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.</td>
</tr>
</tbody>
</table>

### Return Values (Abnormal)

When the REST-API response of Infrastructure Manager is an error.

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

Case other than the above.

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|msg|string|No|Not omitted, but null is allowed.|Message except API processing results|

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_get_profile_info.yml](/examples/ism_get_profile_info.yml)

## <a name="ism_get_power_status">ism_get_power_status

Retrieving Power Status

### Synopsis

Retrieves the power status of the ISM managed node.  
It is used to confirm the power status of the node, such as after the operation of power.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.2.0

### Options

|Parameter|Type  |Required|Esential Mode|Default|Choices|Comments                                                                                                       |
|:--------|:-----|:------:|:-----------:|:------|:------|:--------------------------------------------------------------------------------------------------------------|
|config   |string|Yes     |Yes          |None   |None   |Specifies the full path for the described setting file of the connection information of Infrastructure Manager.|
|hostname |string|Yes     |Yes          |None   |None   |Specifies the IP address and host name of the operation. [[Note1]](#note-9-1)[[Note2]](#note-9-2)              |

<a name="note-9-1">[Note1]  
Specify the host name (FQDN) for the IP address or the IP address of the operation node registered in Infrastructure Manager is specified.  
When the OS information of the operation node is registered in Infrastructure Manager, the host name (FQDN) for the IP address of the OS information or the IP address can be specified.

<a name="note-9-2">[Note2]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager,  
specify the IP address of IPv4 or the host name (FQDN) that are available for the name resolution of IPv4.

### Examples

```yaml
- name: Getting Power Status
  ism_get_power_status:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
  register: ism_get_power_status_result
- debug: var=ism_get_power_status_result
```

### Return Values (Normal)

<table>
<tbody>
<tr>
  <th colspan="4">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="4">ism_get_power_status</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Retrieval result of the power status information</td>
</tr>
<tr>
  <td rowspan="11"></td>
  <td colspan="3">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>API processing results</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="2">Parts</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>List of Power Sources</td>
</tr>
<tr>
  <td rowspan="3"></td>
  <td>Name</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Name of Power Source<br>Sets PowerManagement.</td>
</tr>
<tr>
  <td>PowerChoices</td>
  <td>string-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Choices of Power Sources<br>All choices that are operational are set. The choices are PowerOn, Reset, and Shutdown.<br>Operational choices other than PowerOn, Reset, and Shutdown are different according to the node.<br>It becomes an empty list ([ ]) when it is unable to operate.</td>
</tr>
<tr>
  <td>PowerStatus</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Status of Power Sources<br>The value of either On, Off, Standby or Unknown is set.</td>
</tr>
<tr>
  <td colspan="3">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>
If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="2">Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information of the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td colspan="2">MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>A unique ID is output for each message.</td>
</tr>
<tr>
  <td colspan="2">API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
<tr>
  <td colspan="2">Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="3">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.</td>
</tr>
</tbody>
</table>

### Return Values (Abnormal)

When the REST-API response of Infrastructure Manager is an error.

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

Case other than the above.

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|msg|string|Yes|Not omitted, but null is allowed.|Message except API processing results|

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbooks.  
  [examples/ism_get_power_status.yml](/examples/ism_get_power_status.yml)  
  [examples/ism_power_on_and_wait.yml](/examples/ism_power_on_and_wait.yml)

## <a name="ism_retrieve_download_firmware_info">ism_retrieve_download_firmware_info

Retrieving the downloadable firmware information

### Synopsis

Updates the information of downloadable firmware.  
It is used before retrieving the information of downloadable firmware.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.3.0

### Options

|Parameter|Type  |Required|Essential Mode|Default|Choices|Comments                                                                                                                                            |
|:--------|:-----|:------:|:------------:|:------|:------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
|config   |string|Yes     |Yes           |None   |None   |Specifies the full path for the described setting file of the connection information of Infrastructure Manager.                                     |
|hostname |string|Yes     |Yes           |None   |None   |Specifies the IP address and the host name of the operation.<br>[[Note1]](#note-10-1)[[Note2]](#note-10-2)[[Note3]](#note-10-3)[[Note4]](#note-10-4)|

<a name="note-10-1">[Note1]  
Specify the IP address or the hostname of the ISM server.

<a name="note-10-2">[Note2]  
The information of downloadable firmware is unique in each ISM server
and no need to update the firmware of each ISM node.
Specify the ISM server information for the hostname to operate only once for each ISM server.

<a name="note-10-3">[Note3]  
This module connects to ISM with the information specified in the "config" parameter.
Therefore, misconfiguration of the "hostname" parameter does not affect the behavior of this module.

<a name="note-10-4">[Note4]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager, specify the IP address of IPv4 or the host name (FQDN) that are available for the name resolution of IPv4.

### Examples

```yaml
- name: Retrieving Download Firmware Info
  ism_retrieve_download_firmware_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.10"
  register: ism_retrieve_download_firmware_info_result
- debug: var= ism_retrieve_download_firmware_info_result
```

### Return Values (Normal)

<table>
<tbody>
<tr>
  <th colspan="2">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="2">ism_retrieve_download_firmware_info_result</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Specifies the full path for the described setting file of the connection information of Infrastructure Manager.</td>
</tr>
<tr>
  <td rowspan="3"></td>
  <td>IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted. empty dict.</td>
  <td>API processing results.<br>Return only key name when no API processing results.</td>
</tr>
<tr>
  <td>MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted. empty list.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td>SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted. null</td>
  <td>The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.</td>
</tr>
</tbody>
</table>

### Return Values (Abnormal)

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_retrieve_download_firmware_info.yml](/examples/ism_retrieve_download_firmware_info.yml)

## <a name="ism_get_download_firmware_list">ism_get_download_firmware_list

Retrieving Firmware

### Synopsis

Retrieves the information of downloadable firmware.  
It is used after update of the information of downloadable firmware.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.3.0

### Options

|Parameter|Type   |Required|Essential Mode|Default|Choices                             |Comments                                                                                                                                                                      |
|:--------|:------|:------:|:------------:|:------|:-----------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|config   |string |Yes     |Yes           |None   |None                                |Specifies the full path for the described setting file of the connection information of Infrastructure Manager.                                                               |
|hostname |string |Yes     |Yes           |None   |None                                |Specifies the IP address and the host name of the operation.<br>[[Note1]](#note-11-1)[[Note2]](#note-11-2)[[Note3]](#note-11-3)[[Note4]](#note-11-4)                          |
|filter   |boolean|No      |Yes           |False  |<ul><li>True</li><li>False</li></ul>|True: Retrieves information of downloadble firmware for each node registered in ISM.<br>False: Retrieves information of all the downloadble firmware.<br>[[Note5]](#note-11-5)|

<a name="note-11-1">[Note1]  
Specify the IP address or the hostname of the ISM server.

<a name="note-11-2">[Note2]  
The information of downloadable firmware is unique in each ISM server and no need to update the firmware for each node registered in ISM.  
Specify the information of an ISM server to "hostname" parameter and run once for each ISM server.

<a name="note-11-3">[Note3]  
This module connects to ISM with the information specified in the "config" parameter.  
Therefore, misconfiguration of the "hostname" parameter does not affect the behavior of this module.

<a name="note-11-4">[Note4]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager, specify the IP address of IPv4 or the host name (FQDN) that are available for the name resolution of IPv4.

<a name="note-11-5">[Note5]  
True : Retrieves information of the latest firmware for each node registered in ISM from firmwares provided by Global Flash.  
False: Retrieves information of all the firmwares provided by Global Flash.

### Examples

```yaml
- name: Getting Download Firmware List
  ism_get_download_firmware_list:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.10"
    filter:True
  register: ism_get _download_firmware_list_result
- debug: var= ism_get_download_firmware_list_result
```

### Return Values (Normal)

<table>
<tbody>
<tr>
  <th colspan="4">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="4">ism_get_download_firmware_list</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Downloadable firmware list</td>
</tr>
<tr>
  <td rowspan="15"></td>
  <td colspan="3">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>API processing results.<br>Return only key name when no API processing results.</td>
</tr>
<tr>
  <td rowspan="8"></td>
  <td colspan="2">FirmwareList</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted. but can be an empty list.</td>
  <td>List of Firmware</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td>FirmwareId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Firmware ID</td>
</tr>
<tr>
  <td>ModelName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Model name</td>
</tr>
<tr>
  <td>FirmwareName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware type</td>
</tr>
<tr>
  <td>FirmwareType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Firmware name</td>
</tr>
<tr>
  <td>FirmwareVersion</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Firmware version</td>
</tr>
<tr>
  <td>RepositoryPath</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Path to firmware on FTS repository</td>
</tr>
<tr>
  <td>RegisterDate</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Firmware Update Date</td>
</tr>
<tr>
  <td colspan="3">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output.<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="2">Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information of the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td colspan="2">MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>A unique ID is output for each message.</td>
</tr>
<tr>
  <td colspan="2">API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td colspan="2">Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="3">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name containing the JSON schema (JSON schema file name) that displays the entire HTTP body structure is output.</td>
</tr>
</tbody>
</table>

### Return Values (Abnormal)

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_get_download_firmware_list.yml](/examples/ism_get_download_firmware_list.yml)

## <a name="ism_download_firmware">ism_download_firmware

Downloading Firmware

### Synopsis

Downloads firmware.  
It is used to download the firmware before firmware update.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* Infrastructure Manager >= 2.3.0

### Options

<table>
<tbody>
<tr>
  <th colspan="2">Parameter</th>
  <th>Type</th>
  <th>Required</th>
  <th>Essential Mode</th>
  <th>Default</th>
  <th>Choices</th>
  <th>Comments</th>
</tr>
<tr>
  <td colspan="2">config</td>
  <td>string</td>  
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Specifies the full path for the described setting file of the connection information of Infrastructure Manager.</td>
</tr>
<tr>
  <td colspan="2">hostname</td>
  <td>string</td>  
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Specifies the IP address and host name of the operation.<br><a href="#note-12-1">[Note1]</a><a href="#note-12-2">[Note2]</a><a href="#note-12-3">[Note3]</a><a href="#note-12-4">[Note4]</a></td>
</tr>
<tr>
  <td colspan="2">firmware_list</td>
  <td>dict-list</td>  
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>List for specifying firmware to download.<br>
Specify firmware_name and firmware_version as elements of this list.<br><a href="#note-12-5">[Note5]</a></td>
</tr>
<tr>
  <td rowspan="2"></td>
  <td>firmware_name</td>
  <td>string</td>  
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Specify the name of firmware</td>
</tr>
<tr>
  <td>firmware_version</td>
  <td>string</td>  
  <td align="center">Yes</td>
  <td align="center">Yes</td>
  <td>None</td>
  <td>None</td>
  <td>Specify the version of firmware</td>
</tr>
</tbody>
</table>

<a name="note-12-1">[Note1]  
Specify the IP address or the hostname of the ISM server.

<a name="note-12-2">[Note2]  
If it is the same firmware, it can be used commonly among nodes. No need to download in each node registered in ISM.  
Therefore, execute this module once.

<a name="note-12-3">[Note3]  
This module connects to ISM with information specified in "config" parameter.  
Therefore, misconfiguration of "hostname" parameter does not affect the behavior of this module.

<a name="note-12-4">[Note4]  
Presently IPv6 is not supported. For the connection with Infrastructure Manager, specify the IP address of IPv4 or the host name (FQDN) that are available for the name resolution of IPv4.

<a name="note-12-5">[Note5]  
Multiple firmware can be downloaded simultaneously by specifying the multiple firmware.

### Examples

```yaml
- name: Download Firmware
  hosts: ism_server
  connection: local
  vars:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    firmware_download_list:
      - firmware_name: "RX300 S8_iRMC"
        firmware_version: "8.13F&3.71"
      - firmware_name: "RX300 S8_BIOS"
        firmware_version: "R1.11.0"

  tasks:
    - name: Downloading Firmware
      ism_download_firmware:
        config: "{{ config }}"
        hostname: "{{ inventory_hostname }}"
        download_list: "{{ firmware_download_list }}"
      register: ism_download_firmware_result
    - debug: var=ism_download_firmware_result
```

### Return Values (Normal)

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|ism_download_firmware|string|Yes|Not omitted."Success."|Returns execution result of firmware download.|

### Return Values (Abnormal)

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_download_firmware.yml](/examples/ism_download_firmware.yml)

## <a name = "ism_get_report_info"> ism_get_report_info

Retrieving report

### Synopsis

Retrieving ISM report information.  
Outputs file for the Report information comparison tool.  
Refer to [Readme.md - Report information comparison tool](/Readme.md#report-information-comparison-tool).

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* ISM >= 2.2.0

### Options

|Parameter|Type  |Required|Essential Mode|Default|Choices|Comments                                                                                                                                           |
|:--------|:-----|:------:|:------------:|:------|:------|:--------------------------------------------------------------------------------------------------------------------------------------------------|
|config   |string|Yes     |Yes           |None   |None   |Specifies the full path to the configuration file that contains the ISM connection information.                                                    |
|hostname |string|Yes     |Yes           |None   |None   |Specifies the IP address or hostname of the ISM server. <br>[[Note1]](#note-15-1) [[Note2]](#note-15-2) [[Note3]](#note-15-3) [[Note4]](#note-15-4)|

<a name="note-15-1">[Note1]  
 Specifies the IP address of the ISM server or the hostname to that IP address.

<a name="note-15-2">[Note2]  
 The backup files are information unique to the ISM server and do not need to be retrieved for each operational node.  
For this reason, hostname must be set to the information of the ISM server so that it runs only once per ISM server.

<a name="note-15-3">[Note3]  
IPv6 is not supported. Specifies the IPv4 or IPv4 resolvable host name.

<a name="note-15-4">[Note4]  
 Communication with ISM inside the module uses the information in the configuration file specified in config.  
Therefore, any incorrect information specified in hostname does not affect the operation of the module.

### Examples

```yaml
- name: Execution of ism_get_report_info
  ism_get_report_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.10"
  register: ism_get_report_info_result
- debug: var=ism_get_report_info_result
```

### Return Values (Normal)

<table>
<tbody>
<tr>
  <th colspan="6">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="6">ism_node_count</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>The number of nodes registered with ISM is returned.</td>
</tr>
<tr>
  <td colspan="6">ism_node_info</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>The result of obtaining node information is returned.</td>
</tr>
<tr>
  <td rowspan="52"></td>
  <td colspan="5">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>REST-API Processing Results<br>The REST-API results are returned.</td>
</tr>
<tr>
  <td rowspan="45"></td>
  <td colspan="4">Nodes</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node Information</td>
</tr>
<tr>
  <td rowspan="44"></td>
  <td colspan="3">NodeId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node ID</td>
</tr>
<tr>
  <td colspan="3">Name</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node name</td>
</tr>
<tr>
  <td colspan="3">Type</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node type</td>
</tr>
<tr>
  <td colspan="3">Model</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Model Name</td>
</tr>
<tr>
  <td colspan="3">IpAddress</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>IP address</td>
</tr>
<tr>
  <td colspan="3">IpVersion</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>IP version of the IP address<br>- V4: IPv4<br>- V6: IPv6</td>
</tr>
<tr>
  <td colspan="3">WebUrl</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Main WebURL(WebUI of the device, etc.)</td>
</tr>
<tr>
  <td colspan="3">Urls</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted. but can be an empty list.</td>
  <td>Additional WebURL Information</td>
</tr>
<tr>
  <td rowspan="2"></td>
  <td colspan="2">Url</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>WebURL</td>
</tr>
<tr>
  <td colspan="2">UrlName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>WebURL Name</td>
</tr>
<tr>
  <td colspan="3">Description</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Description</td>
</tr>
<tr>
  <td colspan="3">NodeTagList</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted. but can be an empty list.</td>
  <td>Node Tag Information</td>
</tr>
<tr>
  <td></td>
  <td colspan="2">NodeTag</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node Tag Name</td>
</tr>
<tr>
  <td colspan="3">ManagementLanOption</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Management LAN information(ISM 2.4.0.b or later)<br>The output is the management LAN to use when PXE booting the server.</td>
</tr>
<tr>
  <td rowspan="5"></td>
  <td colspan="2">ManagementLanMode</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Management LAN designated mode (ISM 2.4.0.b or later)<br>- null: Not specified. When PXE booting, the port with the smaller order of slot 0 is used.<br>- MACAddress: MAC address<br>- Adapter: Adapter</td>
</tr>
<tr>
  <td colspan="2">AdapterInfo</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Information about the adapter used as the management LAN (ISM 2.4.0.b or later)</td>
</tr>
<tr>
  <td rowspan="2"></td>
  <td>SlotIndex</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Slot Number (ISM 2.4.0.b or later)</td>
</tr>
<tr>
  <td>PortIndex</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Port Number (ISM 2.4.0.b or later)</td>
</tr>
<tr>
  <td colspan="2">MACAddress</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MAC address to use as the management LAN (ISM 2.4.0.b or later)</td>
</tr>
<tr>
  <td colspan="3">RackInfo</td>
  <td>dict</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Rack mounting location information</td>
</tr>
<tr>
  <td rowspan="3"></td>
  <td colspan="2">RackId</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Rack ID</td>
</tr>
<tr>
  <td colspan="2">Position</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Mounting position (Unit Number)<br>The bottom unit number occupied by the node.</td>
</tr>
<tr>
  <td colspan="2">OccupySize</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Number of rack occupied units</td>
</tr>
<tr>
  <td colspan="3">MountType</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>PDU mount type<br>- Rack: Same type as normal nodes<br>- 0U: Rack side mount type</td>
</tr>
<tr>
  <td colspan="3">PduPosition</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Not used</td>
</tr>
<tr>
  <td colspan="3">Outlet</td>
  <td>dict-list</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>PDU connection information list<br>Not currently supported.</td>
</tr>
<tr>
  <td rowspan="2"></td>
  <td colspan="2">PowerSocket</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Socket Number<br>Not currently supported.</td>
</tr>
<tr>
  <td colspan="2">NodeId</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Node ID to connect<br>Not currently supported.</td>
</tr>
<tr>
  <td colspan="3">SlotNum</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Slot number in the chassis<br>For CX servers, BX server blades, and connection blades, this is set automatically when node information is obtained.</td>
</tr>
<tr>
  <td colspan="3">ParentNodeId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Node ID of the parent node<br>Set automatically when node information is obtained. For BX server blades and connection blades, this is set when obtaining node information for the BX chassis.</td>
</tr>
<tr>
  <td colspan="3">ParentFabricId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Node ID of the owning fabric node<br>For fabric switches, this is set automatically when the node information for the fabric is retrieved.</td>
</tr>
<tr>
  <td colspan="3">ChildNodeList</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Child Node Information<br>Contains the nodes with which child nodes are related.</td>
</tr>
<tr>
  <td rowspan="3"></td>
  <td colspan="2">NodeId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Node ID of the child node</td>
</tr>
<tr>
  <td colspan="2">Type</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Node type of the child node</td>
</tr>
<tr>
  <td colspan="2">SlotNum</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Slot number in the chassis</td>
</tr>
<tr>
  <td colspan="3">Fabric</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Switch node information that makes up the fabric</td>
</tr>
<tr>
  <td></td>
  <td colspan="2">NodeId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node ID of the switch node</td>
</tr>
<tr>
  <td colspan="3">Status</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node Status<br>- Error: Error<br>- Warning: Warning<br>- Unknown: No Communication<br>- Normal: Normal<br>- Updating: Communication in proggress</td>
</tr>
<tr>
  <td colspan="3">AlarmStatus</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Alarm status of the node<br>If there is an underlying node (ChildNodeList or Fabric), it displays the status with the highest severity, including the underlying node.<br>- Error: Error<br>- Warning: Warning<br>- Info: Information<br>- Normal: No notification<br>Status priority: Normal &lt; Info &lt; Warning &lt; Error</td>
</tr>
<tr>
  <td colspan="3">MaintenanceMode</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Maintenance Mode<br>- Normal: Normal mode<br>- Maintenance: maintenance mode</td>
</tr>
<tr>
  <td colspan="3">NodeGroupId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node Group ID</td>
</tr>
<tr>
  <td colspan="3">UniqInfo</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Specific information for internal management</td>
</tr>
<tr>
  <td colspan="3">AdditionalData</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Internal Management Information (ISM 2.4.0.b or later)</td>
</tr>
<tr>
  <td colspan="3">UpdateDate</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Last Update Time</td>
</tr>
<tr>
  <td colspan="5">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Message Information<br>Errors, warnings, and notification messages resulting from the processing of REST-API are returned.<br>If the information does not exist, only the key name is returned.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="4">Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the time stamp of the message is returned.</td>
</tr>
<tr>
  <td colspan="4">MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>A unique ID is returned for each message.</td>
</tr>
<tr>
  <td colspan="4">API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API Type<br>The API type is returned in the form of a method name URI.</td>
</tr>
<tr>
  <td colspan="4">Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message<br>The message is returned.</td>
</tr>
<tr>
  <td colspan="5">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>The file name (JSON Schema File Name) containing the JSON schema representing the overall structure of the HTTP body is returned.</td>
</tr>
<tr>
  <td colspan="6">ism_inventory_info</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>The inventory information retrieval result is returned.</td>
</tr>
<tr>
  <td rowspan="35"></td>
  <td colspan="5">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>REST-API Processing Results<br>The REST-API processing results are returned.<br>If the information does not exist, only the key name is returned.</td>
</tr>
<tr>
  <td rowspan="28"></td>
  <td colspan="4">Nodes</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node inventory information</td>
</tr>
<tr>
  <td rowspan="27"></td>
  <td colspan="3">HardwareLogTarget</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>Node log collection availability information<br>Used with the Log Management feature.<br>- 0: Not allowed<br>- 1: Allowed</td>
</tr>
<tr>
  <td colspan="3">MacAddress</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MAC Address of the device</td>
</tr>
<tr>
  <td colspan="3">Manufacture</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Vendor Name</td>
</tr>
<tr>
  <td colspan="3">Name</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>System Name</td>
</tr>
<tr>
  <td colspan="3">NodeId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Node ID</td>
</tr>
<tr>
  <td colspan="3">ProductName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Model Name</td>
</tr>
<tr>
  <td colspan="3">Progress</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Progress of node information acquisition<br>- Updating: Retrieving. Displays information previously captured.<br>- Complete: Retrieved. Displays the latest information.<br>- Error: Failed to get information. The information is not updated.</td>
</tr>
<tr>
  <td colspan="3">RaidLogTarget</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>RAID log collection availability information<br>Used with the Log Management feature.<br>- 0: Not allowed<br>- 1: Allowed</td>
</tr>
<tr>
  <td colspan="3">SerialNumber</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Serial Number</td>
</tr>
<tr>
  <td colspan="3">ServerViewLogTarget</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>ServerView log collection availability information<br>Used with the Log Management feature.<br>- 0: Not allowed<br>- 1: Allowed</td>
</tr>
<tr>
  <td colspan="3">SoftwareLogTarget</td>
  <td>integer</td>
  <td align="center">No</td>
  <td>Not omitted.</td>
  <td>OS log collection availability information<br>Used with the Log Management feature.<br>- 0: Not allowed<br>- 1: Allowed</td>
</tr>
<tr>
  <td colspan="3">UpdateDate</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Modified</td>
</tr>
<tr>
  <td colspan="3">VariableData</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Learn more</td>
</tr>
<tr>
  <td rowspan="14"></td>
  <td colspan="2">Firmware</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware Information</td>
</tr>
<tr>
  <td rowspan="13"></td>
  <td>Name</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware Name</td>
</tr>
<tr>
  <td>SlotId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Slot ID</td>
</tr>
<tr>
  <td>Model</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Model Name</td>
</tr>
<tr>
  <td>Type</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware Type</td>
</tr>
<tr>
  <td>FirmwareVersion</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware Version</td>
</tr>
<tr>
  <td>Slot</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Slot Number</td>
</tr>
<tr>
  <td>Segment</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Segment</td>
</tr>
<tr>
  <td>Bus</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Bus Number</td>
</tr>
<tr>
  <td>Device</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Device Number</td>
</tr>
<tr>
  <td>Function</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Function Number</td>
</tr>
<tr>
  <td>Version</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>iRMC Version<br>Display for PRIMERGY servers.</td>
</tr>
<tr>
  <td>ParentName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Installation source information</td>
</tr>
<tr>
  <td>Unified</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Unified Model</td>
</tr>
<tr>
  <td colspan="5">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Message Information<br>Errors, warnings, and notification messages resulting from the processing of REST-API are returned.<br>If the information does not exist, only the key name is returned.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="4">Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the time stamp of the message is returned.</td>
</tr>
<tr>
  <td colspan="4">MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>A unique ID is returned for each message.</td>
</tr>
<tr>
  <td colspan="4">API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API Type<br>The API type is returned in the form of a method name URI</td>
</tr>
<tr>
  <td colspan="4">Messaage</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message<br>The message is returned.</td>
</tr>
<tr>
  <td colspan="5">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>The file name (JSON Schema File Name) containing the JSON schema representing the overall structure of the HTTP body is returned.</td>
</tr>
<tr>
  <td colspan="6">ism_firmware_info</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>The firmware information retrieval result is returned.</td>
</tr>
<tr>
  <td rowspan="18"></td>
  <td colspan="5">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>REST-API Processing Results<br>The REST-API proccesing retrieval result is returned.</td>
</tr>
<tr>
  <td rowspan="11"></td>
  <td colspan="4">FirmwareList</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>A list of available firmware updates will be returned.</td>
</tr>
<tr>
  <td rowspan="10"></td>
  <td colspan="3">DiskUsage</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Disk space used by firmware (MB)</td>
</tr>
<tr>
  <td colspan="3">FirmwareId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware ID</td>
</tr>
<tr>
  <td colspan="3">FirmwareName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware Name</td>
</tr>
<tr>
  <td colspan="3">FirmwareType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware Type</td>
</tr>
<tr>
  <td colspan="3">FirmwareVersion</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware Version</td>
</tr>
<tr>
  <td colspan="3">ModelName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Model Name</td>
</tr>
<tr>
  <td colspan="3">NodeId</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Node ID</td>
</tr>
<tr>
  <td colspan="3">OperationMode</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Supported mode</td>
</tr>
<tr>
  <td colspan="3">RegisterDate</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Firmware registration date and time</td>
</tr>
<tr>
  <td colspan="3">RepositoryName</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Repository Name</td>
</tr>
<tr>
  <td colspan="5">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages resulting from the processing of REST-API are returned.<br>If the information does not exist, only the key name is returned.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="4">Tiemstamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>The date and time when the message occurred is returned.</td>
</tr>
<tr>
  <td colspan="4">MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>A unique ID is returned for each message.</td>
</tr>
<tr>
  <td colspan="4">API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API Type<br>The API type is returned in the form of a method name URI.</td>
</tr>
<tr>
  <td colspan="4">Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message<br>The message is returned.</td>
</tr>
<tr>
  <td colspan="5">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name (JSON Schema File Name) containing the JSON schema representing the overall structure of the HTTP body is returned.</td>
</tr>
<tr>
  <td colspan="6">ism_status_count</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes in each status</td>
</tr>
<tr>
  <td rowspan="5"></td>
  <td colspan="5">Error</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes with status Error</td>
</tr>
<tr>
  <td colspan="5">Warning</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes with status Warning</td>
</tr>
<tr>
  <td colspan="5">Unknown</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes with status Unknown</td>
</tr>
<tr>
  <td colspan="5">Updating</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes with status Updating</td>
</tr>
<tr>
  <td colspan="5">Normal</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes with status Normal</td>
</tr>
<tr>
  <td colspan="6">ism_alarm_staus_count</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes in each alarm status</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td colspan="5">Error</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes with an alarm status of Error</td>
</tr>
<tr>
  <td colspan="5">Warning</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes with an alarm status of Warning</td>
</tr>
<tr>
  <td colspan="5">Info</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes with an alarm status of Info</td>
</tr>
<tr>
  <td colspan="5">Normal</td>
  <td>integer</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>Number of nodes with an alarm status of Normal</td>
</tr>
<tr>
  <td colspan="6">Time</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted.</td>
  <td>The date and time (Local time) format when the module was executed is as follows:<br>&lt;Year>-&lt;Month>-&lt;Days>T&lt;Hour>:&lt;Minutes>:&lt;Seconds></td>
</tr>
</tbody>
</table>

### Return Values (Abnormal)

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">Yes</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Sample playbook.  
  [examples/ism_get_report_info.yml](/examples/ism_get_report_info.yml)

## <a name = "ism_backup"> ism_backup

Backing up ISM-VA

### Synopsis

Perform a backup of ISM-VA.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.7
* pexpect >= 4.7 (Python Library)
* ISM >= 2.2.0.c

### Options

|Parameter|Type   |Required|Essential Mode|Default|Choices|Comments                                                                                                                                                                                                                                                                                                                    |
|:--------|:------|:------:|:------------:|:------|:------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|config   |string |Yes     |Yes           |None   |None   |Specifies the full path to the configuration file that contains the ISM connection information.<br>[[Note1]](#note-16-1)                                                                                                                                                                                                    |
|hostname |string |Yes     |Yes           |None   |None   |Specifies the IP address or hostname of the ISM server. <br> [[Note2]](#note-16-2) [[Note3]](#note-16-3) [[Note4]](#note-16-4) [[Note5]](#note-16-5)                                                                                                                                                                        |
|dest_dir |string |Yes     |Yes           |None   |None   |Specifies the full path to the destination directory for the backup files. <br> The backup file name is automatically set in the following format. <br>- Format<br>&nbsp; ism&lt;ISM Version\>-backup-&lt;Backup Datetime\>.tar.gz <br>- Example<br>&nbsp; ism2.5.0.03-backup-20191219041611.tar.gz<br>[[Note6]](#note-16-6)|
|timeout  |integer|No      |Yes           |0      |None   |Specifies an integer timeout to wait for the backup to complete. The unit is seconds. If it is less than or equal to zero or omitted, no timeout is performed.<br>[[Note7]](#note-16-7)                                                                                                                                     |

<a name="note-16-1">[Note1]  
Use single-byte uppercase and lowercase letters, numbers, and symbols.

<a name="note-16-2">[Note2]  
 Specifies the IP address of the ISM server or the hostname to that IP address.

<a name="note-16-3">[Note3]  
 The backup files are information unique to the ISM server and do not need to be retrieved for each operational node.  
For this reason, hostname must be set to the information of the ISM server so that it runs only once per ISM server.

<a name="note-16-4">[Note4]  
IPv6 is not supported. Specifies the IPv4 or IPv4 resolvable host name.

<a name="note-16-5">[Note5]  
 Communication with ISM inside the module uses the information in the configuration file specified in config.  
Therefore, any incorrect information specified in hostname does not affect the operation of the module.

<a name="note-16-6">[Note6]  
Specify a previously created directory.

<a name="note-16-7">[Note7]  
If a timeout occurs, the following error message is output:<br>
```waiting for backup timeout: <Timeout Seconds>s```<br>
Increase the timeout period and try again.

### Examples

```yaml
- name: Backing up ISM
  ism_backup:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.102.206"
    dest_dir: "/tmp"
    timeout: 0
  register: ism_backup_result
- debug: var=ism_backup_result
```

### Return Values (Normal)

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|ism_backup_file|string|Yes|Not omitted.|The collected backup file will be returned with the full path.|

### Return Values (Abnormal)

|Name|Type|Essential Mode|Returned|Description|
|:--|:--|:--:|:--|:--|
|msg|string|Yes|Not omitted, but null is allowed.|An error message is returned during the backup process.|

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Sample playbook.  
  [examples/ism_backup.yml](/examples/ism_backup.yml)

## <a name = "ism_copy_profile"> ism_copy_profile

 Copying Profile

### Synopsis

 Copying Profile.

### Requirements

* Ansible >= 2.4.0.0
* Python >= 2.6
* ISM >= 2.2.0

### Options

|Parameter              |Type  |Required|Essential Mode|Default|Choices|Comments                                                                                                                      |
|:----------------------|:-----|:------:|:------------:|:------|:------|:-----------------------------------------------------------------------------------------------------------------------------|
|config                 |string|Yes     |No            |None   |None   |Specifies the full path to the configuration file that contains the ISM connection information.<br>[[Note1]](#note-17-1)      |
|ism_source_profile_name|string|Yes     |No            |None   |None   |Specifies the name of the profile to copy from.                                                                               |
|ism_profile_name       |string|Yes     |No            |None   |None   |Specifies the destination profile name.                                                                                       |
|ism_profile_data       |dict  |No      |No            |None   |None   |Specifies the value to change when copying.<br>If omitted, no changes are made.<br>[[Note2]](#note-17-2) [[Note3]](#note-17-3)|

<a name="note-17-1">[Note1]  
Use single-byte uppercase and lowercase letters, numbers, and symbols.

<a name="note-17-2">[Note2]  
Refer to and specify the following REST-API request parameters "ProfileData".  
FUJITSU Software Infrastructure Manager REST API Reference Manual  

* Add Profile  
  <http://www.fujitsu.com/jp/products/software/infrastructure-software/infrastructure-software/serverviewism/technical/index.html>

<a name="note-17-3">[Note3]  
When specifying the password information, use "ansible" as the encryption key and use the following Linux command example to specify AES 256 + Base 64 + MD5 encrypted values.  

Command:  

```shell
echo -n '<Password>' | openssl enc -aes-256-cbc -e -base64 -md md5 -pass pass:ansible  
```

Command Example:  

```shell
$ echo -n 'password' | openssl enc -aes-256-cbc -e -base64 -md md5 -pass pass:ansible  
U2FsdGVkX186qfuegUxjCcApbUWJ6r51xKGj7RmmwsA=
```

### Examples

```yaml
- name: Copy Profile
  hosts: servers
  gather_facts: no
  connection: local
  vars:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    ism_source_profile_name: "SourceProfile"
    ism_profile_data:
      Server-RX:
        OSInstallation:
          Windows:
            OsIndividualConfig:
              BasicSettings:
                ComputerName: "{{ ism_computer_name }}"
              NetworkInterface:
                IPv4:
                  Address: "{{ ism_os_ip_address }}"
  tasks:
    - name: Copying Profile
      ism_copy_profile:
        config: "{{ config }}"
        ism_source_profile_name: "{{ ism_source_profile_name }}"
        ism_profile_name: "{{ ism_profile_name }}"
        ism_profile_data: "{{ ism_profile_data }}"
      register: ism_copy_profile_result
    - debug: var=ism_copy_profile_result
```

### Return Values (Normal)

| Name | Type | Essential Mode | Returned |Description|
|:--|:--|:--:|:--|:--|
|ism_copy_profile|dict|No|Always returns "Success".|The result of the copy of profile is returned.|

### Return Values (Abnormal)

<table>
<tbody>
<tr>
  <th colspan="3">Name</th>
  <th>Type</th>
  <th>Essential Mode</th>
  <th>Returned</th>
  <th>Description</th>
</tr>
<tr>
  <td colspan="3">msg</td>
  <td>dict</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>MessageInfo, IsmBody, and SchemaType</td>
</tr>
<tr>
  <td rowspan="7"></td>
  <td colspan="2">MessageInfo</td>
  <td>dict-list</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message information<br>Errors, warnings, and notification messages regarding API processing are output<br>If there is no information available, only the key names are output.</td>
</tr>
<tr>
  <td rowspan="4"></td>
  <td>Timestamp</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Date and time information<br>Information on the date and time when the corresponding message displayed is output.</td>
</tr>
<tr>
  <td>MessageId</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>Message ID<br>
A unique ID is output for each message.</td>
</tr>
<tr>
  <td>API</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API type<br>The API type is output in the format "Method name URI".</td>
</tr>
<tr>
  <td>Message</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>API processing results<br>API processing results are output as response parameters.</td>
</tr>
<tr>
  <td colspan="2">IsmBody</td>
  <td>dict</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The processing result of REST-API is output.</td>
</tr>
<tr>
  <td colspan="2">SchemaType</td>
  <td>string</td>
  <td align="center">No</td>
  <td>Not omitted, but null is allowed.</td>
  <td>The file name where the JSON schema that shows the globular conformation of the HTTP body described is output.</td>
</tr>
</tbody>
</table>

### Notes

* Parameter setting in config file.  
  [Readme.md - 4. Setting config file](/Readme.md#4-setting-config-file)
* Parameter setting in inventory file.  
  [Readme.md - 5. Setting inventory file](/Readme.md#5-setting-inventory-file)
* Sample playbook.  
  [examples/ism_copy_profile.yml](/examples/ism_copy_profile.yml)
