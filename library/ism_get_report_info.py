#!/usr/bin/python
# coding: UTF-8

#######
# Copyright FUJITSU LIMITED 2019
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ism_get_report_info
short_description: Get the report information of Infrastructure Manager.
description:
    - "Provides an interface for get the report information of Infrastructure Manager."
version_added: "2.4"
author: "Munenori Maeda (@XXXXXXXXX)"
options:
    config:
      description:
        - Specifies the full path for the described setting file
          of the connection information of Infrastructure Manager.
      required: true
    hostname:
      description:
        - Specify the host name (FQDN) for the IP address or
          the IP address of Operation node registered in Infrastructure Manager is specified.
          When OS information of the operation node is registered in Infrastructure Manager,
          the host name (FQDN) for the IP address of OS information orthe IP address can be
          specified.
          IPv6 is not supported. Specify a host name that can be resolved by IPv4 or IPv4.
      required: true
requirements:
    - "python >= 2.6"
    - "ISM >= 2.2.0"
notes:
    - "The setting method of the setting file specified in the config parameter is in the following
      location:
      U(https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)"
'''

EXAMPLES = '''
- name: Execution of ism_get_report_info
  ism_get_report_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.10"
  register: ism_get_report_info_result
- debug: var=ism_get_report_info_result
'''

RETURN = '''
ism_node_count:
    description: The node count is returned.
    returned: Always
    type: integer
ism_node_info:
    description: The execution result of get node information is returned.
    returned: Always
    type: dict
ism_inventory_info:
    description: The execution result of get inventory information is returned.
    returned: Always
    type: dict
ism_firmware_info:
    description: The execution result of get firmware information is returned.
    returned: Always
    type: dict
ism_status_count:
    description: The node counts of each status is returned.
    returned: Always
    type: dict
ism_alarm_status_count:
    description: The node counts of each alarm status is returned.
    returned: Always
    type: dict
time:
    description: The execution time is returned.
    returned: Always
    type: string
'''

# import
import traceback
import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon


class IsmGetReportInfo():

    module = AnsibleModule(
        argument_spec=dict(
            config=dict(required=True),
            hostname=dict(required=True)
        )
    )

    def __init__(self):
        self.__present()

    def __present(self):
        try:
            self.common = IsmCommon(self.module)

            self.common.preProcess(self.module.params,
                                   usableEssential=True, NodeCheck=False)

            node_info = self.getNodeInfo()

            inventory_info = self.getInventoryInfo()

            status_info, alarm_info, node_ids = self.countNodeStatus(node_info)

            firmware_info = self.getUpdatableFirmwareInfo(node_ids)

            time_stamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

            self.module.exit_json(changed=False,
                                  ism_node_count=len(node_info['IsmBody']['Nodes']),
                                  ism_node_info=node_info,
                                  ism_inventory_info=inventory_info,
                                  ism_firmware_info=firmware_info,
                                  ism_status_count=status_info,
                                  ism_alarm_status_count=alarm_info,
                                  time=time_stamp)

        except Exception as e:
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
        finally:
            # ISM logout
            self.common.ismLogout()

    """
    @Description Function to get inventory infomation
    @return      dict json_data
    """
    def getInventoryInfo(self):
        self.module.debug("***** getInventoryInfo Start *****")

        # Create query param
        dict_param = dict()
        dict_param['level'] = "All"
        dict_param['target'] = "Firmware"

        param = self.common.getQueryParam(dict_param)

        # Get REST URL
        rest_url = self.common.getRestUrl(self.common.NODES_REST_URL, "inventory" + param)

        # REST API execution
        json_data = self.common.execRest(rest_url, self.common.GET, self.common.RESPONSE_CODE_200)

        # Filter not supported values on Essential mode
        self.common.filterEssentialModeForInventoryArray(json_data)

        self.module.debug("***** getInventoryInfo End *****")

        return json_data

    """
    @Description Function to get node infomation
    @return      dict json_data
    """
    def getNodeInfo(self):
        self.module.debug("***** getNodeInfo Start *****")

        # Get REST URL
        rest_url = self.common.getRestUrl(self.common.NODES_REST_URL)

        # REST API execution
        json_data = self.common.execRest(rest_url, self.common.GET, self.common.RESPONSE_CODE_200)

        # Filter not supported values on Essential mode
        self.common.filterEssentialModeForNodeListArray(json_data)

        self.module.debug("***** getNodeInfo End *****")

        return json_data

    """
    @Description Function to count node status and correct node id
    @return      dict status_info, dict alarm_info, array node_ids
    """
    def countNodeStatus(self, node_info):
        self.module.debug("***** countNodeStatus Start *****")

        status_info = {
            'Error': 0,
            'Warning': 0,
            'Unknown': 0,
            'Updating': 0,
            'Normal': 0
        }
        alarm_info = {
            'Error': 0,
            'Warning': 0,
            'Info': 0,
            'Normal': 0
        }

        node_ids = []

        for node in node_info['IsmBody']['Nodes']:
            # status
            if node['Status'] in status_info:
                status_info[node['Status']] += 1
            # alarm
            if node['AlarmStatus'] in alarm_info:
                alarm_info[node['AlarmStatus']] += 1

            node_ids.append("nodeid=" + str(node['NodeId']))

        self.module.debug("***** countNodeStatus End *****")

        return status_info, alarm_info, node_ids

    """
    @Description Function to get updatable firmware infomation
    @param       array node id list
    @return      dict json_data
    """
    def getUpdatableFirmwareInfo(self, node_ids):
        self.module.debug("***** getUpdatableFirmwareInfo Start *****")

        rest_url = None
        node_exist = None

        if len(node_ids) > 0:
            # nodes exist
            node_exist = True
            rest_url = self.common.getRestUrl(self.common.FIRMWARE_URL
                                              + "list?" + "&".join(node_ids))
        else:
            # node not exist
            node_exist = False
            rest_url = self.common.getRestUrl(self.common.FIRMWARE_URL + "list")

        # REST API execution
        json_data = self.common.execRest(rest_url, self.common.GET, self.common.RESPONSE_CODE_200)

        if not node_exist:
            # clear firmwarelist
            json_data["IsmBody"]["FirmwareList"] = []

        self.module.debug("***** getUpdatableFirmwareInfo End *****")

        return json_data


if __name__ == '__main__':
    IsmGetReportInfo()
