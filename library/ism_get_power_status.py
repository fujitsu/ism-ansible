#!/usr/bin/python
#coding: UTF-8

#######
# Copyright FUJITSU LIMITED 2018
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
module: ism_get_power_status
short_description: Get the power status of Infrastructure Manager.
description:
    - "Provides an interface for get the power status of Infrastructure Manager."
version_added: "2.4" 
author: "Nakamura Takayuki (@nakamura-taka)"
options:
    config:
      description:
        - Specifies the full path for the described setting file of the connection information of Infrastructure Manager.
      required: true
    hostname:
      description:
        - Specify the host name (FQDN) for the IP address or the IP address of Operation node registered in Infrastructure Manager is specified.
          When OS information of the operation node is registered in Infrastructure Manager,
          the host name (FQDN) for the IP address of OS information or the IP address can be specified.
          IPv6 is not supported. Specify a host name that can be resolved by IPv4 or IPv4.
      required: true
requirements:
    - "python >= 2.6"
    - "ISM >= 2.2.0"
notes:
    - "The setting method of the setting file specified in the config parameter is in the following location:
       U(https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)"
'''

EXAMPLES = '''
- name: Getting Power Status
  ism_get_power_status:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
  register: ism_get_power_status_result
- debug: var=ism_get_power_status_result
'''

RETURN = '''
ism_get_power_status:
    description: The execution result of power status acquisition is returned.
    returned: Always
    type: dict
'''

# import
import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon
from ansible.module_utils.ism_user_settings import IsmUserSettingsValue

class IsmGetPowerStatus():

    # Receiving args
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(required=True),
            hostname=dict(required=True)
        )
    )
    
    def __init__(self):
       self.__present()
       
    def __present(self):
        try :
            self.module.log("argument_spec with config=" + str(self.module.params['config']) + " hostname=" + str(self.module.params['hostname']))
            
            # Instance of common class
            common = IsmCommon(self.module)
            
            # Pre-process
            common.preProcess(self.module.params)
            
            # Get power status execution
            result = self.getPowerStatus(common)
            
            # ISM logout
            common.ismLogout()
            
            # Return json
            changed_result = False
            self.module.log("ism_get_power_status successful completion")
            self.module.exit_json(changed=changed_result, ism_get_power_status=result)
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    """
    @Description Function to get power status
    @param       class common
    @return      dict json_data
    """
    def getPowerStatus(self, common):
        try :
            self.module.debug("***** getPowerStatus Start *****")
            
            # Get REST URL
            rest_url = common.getRestUrl(common.NODES_REST_URL, common.getNodeId() + "/power")
            
            # REST API execution
            json_data = common.execRest(rest_url, common.GET, common.RESPONSE_CODE_200)
            
            self.module.log("getPowerStatus success")
            self.module.debug("***** getPowerStatus End *****")
            
            return json_data
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
IsmGetPowerStatus()
