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
module: ism_get_profile_info
short_description: Get the profile information of Infrastructure Manager.
description:
    - "Provides an interface for get the profile information of Infrastructure Manager."
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
    status:
      description:
        - Specify the assign state of the profile.
          If there is no designation, the profile information of the operation target node is output regardless of the applied state of the profile.
          C(assigned) acquire the assigned profile information.
          C(mismatch) acquire the mismatch profile information.
          C(processing) acquire profile information during assignment and unassignment.
          C(canceling) acquire profile information during cancel processing.
          C(canceled) acquire profile information of cancel completed.
          C(error) acquire profile information of error.
      choices: ['assigned', 'mismatch', 'processing', 'canceling', 'canceled', 'error']
      required: false
requirements:
    - "python >= 2.6"
    - "ISM >= 2.2.0"
notes:
    - "The setting method of the setting file specified in the config parameter is in the following location:
       U(https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)"
'''

EXAMPLES = '''
- name: Getting Profile Information
  ism_get_profile_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    status: "assigned"
  register: ism_get_profile_info_result
- debug: var=ism_get_profile_info_result
'''

RETURN = '''
ism_get_profile_info:
    description: The execution result of profile information acquisition is returned.
    returned: Always
    type: dict
'''

# import
import copy
import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon
from ansible.module_utils.ism_user_settings import IsmUserSettingsValue

class IsmGetProfileInfo():

    # Receiving args
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(required=True),
            hostname=dict(required=True),
            status=dict(required=False)
        )
    )
    
    def __init__(self):
       self.__present()
       
    def __present(self):
        try :
            self.module.log("argument_spec with config=" + str(self.module.params['config']) + " hostname=" + str(self.module.params['hostname']) + \
                            " status=" + str(self.module.params['status']))
            
            # Instance of common class
            common = IsmCommon(self.module)
            
            # Pre-process
            common.preProcess(self.module.params)
            
            # Get profile info execution
            result = self.getProfileInfo(common)
            
            # ISM logout
            common.ismLogout()
            
            # Return json
            changed_result = False
            self.module.log("ism_get_profile_info successful completion")
            self.module.exit_json(changed=changed_result, ism_get_profile_info=result)
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    """
    @Description Function to get profile infomation
    @param       class common
    @return      dict profile_list
    """
    def getProfileInfo(self, common):
        try :
            self.module.debug("***** getProfileInfo Start *****")
            
            # Create query param
            dict_param = dict()
            dict_param['status'] = self.module.params['status']
            
            param = common.getQueryParam(dict_param)
            
            # Get REST URL
            rest_url = common.getRestUrl(common.PROFILE_LIST_REST_URL, param)
            
            # REST API execution
            json_data = common.execRest(rest_url, common.GET, common.RESPONSE_CODE_200)
            
            profile_list = []
            profile_list = copy.deepcopy(json_data)
            profile_list['IsmBody']['ProfileList'] = []
            
            for key in json_data['IsmBody']['ProfileList']:
                if key['AssignedNodeId'] == int(common.getNodeId()):
                    profile_list['IsmBody']['ProfileList'].append(key)
                    
            self.module.log("getProfileInfo success")
            self.module.debug("***** getProfileInfo End *****")
            
            return profile_list
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
IsmGetProfileInfo()
