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
module: ism_refresh_node_info
short_description: Update the node information of ServerView Infrastructure Manager.
description:
    - "Provides an interface for update the node information of ServerView Infrastructure Manager."
version_added: "2.4" 
author: "Nakamura Takayuki (@nakamura-taka)"
options:
    config:
      description:
        - Specifies the full path for the described setting file of the connection information of ServerView Infrastructure Manager.
      required: true
    hostname:
      description:
        - Specify the host name (FQDN) for the IP address or the IP address of Operation node registered in ServerView Infrastructure Manager is specified.
          When OS information of the operation node is registered in ServerView Infrastructure Manager,
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
- name: Execution of ism_refresh_node_info
  ism_refresh_node_info:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.25"
  register: ism_refresh_node_info_result
- debug: var=ism_refresh_node_info_result
'''

RETURN = '''
ism_refresh_node_info_result:
    description: The execution result of node information update is returned.
    returned: Always, Success
    type: string
    sample: Success
'''

# import
import time
import datetime
import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon
from ansible.module_utils.ism_user_settings import IsmUserSettingsValue

class IsmRefreshNodeInfo():
    
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
            
            # Refresh node info execution
            result = self.execRefreshNodeInfo(common)
            
            # ISM logout
            common.ismLogout()
            
            # return json
            changed_result = False
            args = dict(
                ism_refresh_node_info = result
            )
            
            self.module.log("ism_refresh_node_info successful completion")
            self.module.exit_json(changed=changed_result, **args)
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    """
    @Description Function to refresh node infomation
    @param       class common
    @return      string result
    """
    def execRefreshNodeInfo(self, common):
        try :
            self.module.debug("***** execRefreshNodeInfo Start *****")
            
            # Get REST URL
            rest_url = common.getRestUrl(common.NODES_REST_URL, common.getNodeId() + "/inventory/refresh")
            
            # REST API execution
            param = " '' "
            json_data = common.execRest(rest_url, common.POST, common.RESPONSE_CODE_201, param)
            refresh_date = json_data["IsmBody"]["RefreshDate"]
            
            # Get inventory info
            result = self.getInventoryInfo(common, refresh_date)
            
            self.module.log("execRefreshNodeInfo success")
            self.module.debug("***** execRefreshNodeInfo End *****")
            
            return result
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    """
    @Description Function to get inventory infomation
    @param       class common
    @param       string refresh_date
    @return      string success
    """
    def getInventoryInfo(self, common, refresh_date):
        try :
            self.module.debug("***** getInventoryInfo Start *****")
            
            now = datetime.datetime.now()
            start_time = long(time.mktime(now.timetuple()))
            time_out = long(start_time) + long(IsmUserSettingsValue.REFRESH_NODE_INFO_TIME_OUT)
            
            # Get REST URL
            rest_url = common.getRestUrl(common.NODES_REST_URL, common.getNodeId() + "/inventory?level=Top")
            
            # Waiting for progress
            self.module.debug("***** waiting for progress Start *****")
            
            progress = ""
            while True:
                now = datetime.datetime.now()
                now_time = long(time.mktime(now.timetuple()))
                
                if long(now_time) < long(time_out):
                    # REST API execution
                    json_data = common.execRest(rest_url, common.GET, common.RESPONSE_CODE_200)
                    progress = json_data["IsmBody"]["Node"]["Progress"]
                    
                    # End loop if progress is Complete or Error
                    if progress == "Complete" or progress == "Error":
                        self.module.debug("***** waiting for progress End *****")
                        break
                else:
                    # The loop ends with fail_json. Errors are received by upper exception.
                    self.module.log("waiting for progress timeout: " + str(IsmUserSettingsValue.REFRESH_NODE_INFO_TIME_OUT) + "s")
                    self.module.fail_json(msg="waiting for progress timeout: " + str(IsmUserSettingsValue.REFRESH_NODE_INFO_TIME_OUT) + "s")
                    
                # Execute sleep
                time.sleep(common.ISM_REFRESH_NODE_INFO_SLEEP_SECOND)
                
            self.module.debug("***** getInventoryInfo End *****")
            
            if progress == "Error":
                event_log_list = self.execEventLogList(common, refresh_date)
                self.module.fail_json(msg=event_log_list)
            else:
                return "Success"
                
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    """
    @Description Function to get event log list
    @param       class common
    @param       string refresh_date
    @return      dict json_data
    """
    def execEventLogList(self, common, refresh_date):
        try :
            self.module.debug("***** execEventLogList Start *****")
            
            # Get REST URL
            rest_url = common.getRestUrl(common.EVENT_LOG_LIST_REST_URL, \
                       "?loglevel=error\&start=" + refresh_date + "\&resourceidtype=NodeId\&resourceid=" + common.getNodeId())
            
            # REST API execution
            json_data = common.execRest(rest_url, common.GET, common.RESPONSE_CODE_200)
            
            self.module.debug("***** execEventLogList End *****")
            
            return json_data
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
IsmRefreshNodeInfo()
