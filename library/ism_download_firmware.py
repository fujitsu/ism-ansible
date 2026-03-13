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
module: ism_download_firmware
short_description: Get the download firmware of Infrastructure Manager.
description:
    - "Provides an interface for get the download firmware of Infrastructure Manager."
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
    - "ISM >= 2.3.0"
notes:
    - "The setting method of the setting file specified in the config parameter is in the following location:
       U(https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)"
'''

EXAMPLES = '''
- name: Downloading Firmware
  ism_download_firmware:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.10"
    download_list: "{{ firmware_download_list }}"
  register: ism_download_firmware_result
- debug: var=ism_download_firmware_result
'''

RETURN = '''
ism_download_firmware:
    description: The execution result of Download Firmware is returned.
    returned: Always
    type: dict
'''

# import
import traceback
import re
import time
import datetime
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon
from ansible.module_utils.ism_user_settings import IsmUserSettingsValue

class IsmDownloadFirmware():
    
    # Receiving args
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(required=True),
            hostname=dict(required=True),
            download_list=dict(required=True , type='list')
        )
    )
    
    def __init__(self):
       self.__present()
       
    def __present(self):
        try :
            self.module.log("argument_spec with config=" + str(self.module.params['config']) + " hostname=" + str(self.module.params['hostname']) + " download_list=" + str(self.module.params['download_list']))
            
            # Instance of common class
            common = IsmCommon(self.module)

            # Parameter chack hash list
            required_keys = ["firmware_name","firmware_version"]
            common.covert_unicode_hash_list(self.module.params['download_list'],required_keys)
            
            # Pre-process
            common.preProcess(self.module.params,NodeCheck = False,
                              usableEssential = True)
            
            # Get download firmware execution
            downloaded_list = self.DownloadedFirmwareList(common)

            # Get check firmware execution
            target_list = self.CheckFirmwareList(common, downloaded_list)

            if len(target_list) == 0:
                task_result = "Success"
                changed_result = False
            else:
                # Download Firmware
                task_result = self.DownloadFirmware(common ,target_list)
                changed_result = True
            
            # ISM logout
            common.ismLogout()
            
            # Return json
            self.module.log("ism_download_firmware successful completion")
            self.module.exit_json(changed=changed_result, ism_download_firmware=task_result)
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    """
    @Description Function to Download Firmware List
    @param       class common
    @return      dict json_data
    """
    def DownloadedFirmwareList(self, common):
        try :
            self.module.debug("***** DownloadFirmwareList Start *****")
            
            # Get REST URL
            rest_url = common.getRestUrl(common.FIRMWARE_URL, "list")
            
            # REST API execution
            json_data = common.execRest(rest_url, common.GET, common.RESPONSE_CODE_200 )
            
            self.module.log("DownloadFirmwareList success")
            self.module.debug("***** DownloadFirmwareList End *****")
            
            return json_data
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))

    """
    @Description Function to Check Firmware List
    @param       class common list downloaded_list
    @return      list param_array
    """
    def CheckFirmwareList(self, common ,downloaded_list ):
        try :
            self.module.debug("***** CheckFirmwareList Start *****")

            dict_param = dict()
            
            argument_list = self.module.params['download_list']
            
            param_array = []
            for argument in argument_list:
                found = False
                for downloaded in downloaded_list["IsmBody"]["FirmwareList"]:
                    if ((downloaded["FirmwareName"] == argument['firmware_name']) \
                        and (downloaded["FirmwareVersion"] == argument['firmware_version'])):
                        found = True
                        break
                        
                if found == False:
                    param_tmp = {}
                    param_tmp["FirmwareName"] = argument["firmware_name"]
                    param_tmp["FirmwareVersion"] = argument["firmware_version"]
                    param_array.append(param_tmp)
            
            self.module.log("CheckFirmwareList success")
            self.module.debug("***** CheckFirmwareList End *****")
            
            return param_array
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))

    """
    @Description Function to Download Firmware
    @param       class common list downloaded_list
    @return      list param_array
    """
    def DownloadFirmware(self, common , target_list):
        try :
            self.module.debug("***** DownloadFirmware Start *****")
            
            # Get REST URL
            rest_url = common.getRestUrl(common.FIRMWARE_URL, "ftsfirmware/download/")
            self.module.log("URL:" + str(rest_url))
            self.module.log("target_list:" + str(target_list))
            self.module.log("param_tmp:" + str(target_list))

            param = { "IsmBody" : 
                        { "ComponentList" : target_list}
                    }
            
            param_str = "\'" + json.dumps(param) + "\'"
            
            self.module.debug("param:" + str(param_str))
            
            # REST API execution
            json_data = common.execRest(rest_url, common.POST, common.RESPONSE_CODE_201 , param_str) 
            
            task_id = json_data["IsmBody"]["TaskId"]
            firmware_number = len(target_list)
            task_result = self.taskCheck(common, task_id ,firmware_number )
            
            self.module.log("tasuku_result:" + str(task_result))
            
            self.module.log("DownloadFirmware success")
            self.module.debug("***** DownloadFirmware End *****")
            
            return task_result
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))

    """
    @Description Function to Download Firmware
    @param       class common ,number firmware_number
    @return      string "Success" or "Error"
    """
    def taskCheck(self,common, id ,firmware_number):
        try :
            self.module.debug("***** taskCheck Start *****")
            
            now = datetime.datetime.now()
            unix_time = long(time.mktime(now.timetuple()))
            time_out = long(unix_time) + long(IsmUserSettingsValue.FIRMWARE_DOWNLOAD_TIME_OUT) * firmware_number
            
            # get rest url
            rest_url = common.getRestUrl(common.TASK_INFO_REST_URL, id)
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + common.getSessionId() + "' "
            
            # waiting for task
            self.module.debug("***** waiting for task Start *****")
            while True:
            
                now = datetime.datetime.now()
                now_time = long(time.mktime(now.timetuple()))
                
                if long(now_time) < long(time_out):
                    # execute rest
                    exec_command = common.COMMAND + rest_url + common.HEADER + add_head + common.HTTP_RESPONSE_CODE + common.CERTIFICATE + "'" + common.singleEscape(common.getIsmCertificate()) + "'"
                    self.module.debug("exec_command = " + exec_command)
                    
                    (rc, stdout, stderr) = common.run_command_unicode(exec_command)
                    self.module.debug("rc = " + str(rc))
                    self.module.debug("stdout = " + stdout)
                    
                    if str(rc) != "0":
                        self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                        self.module.fail_json(msg="curl communication error: " + stderr)
                    
                    task_check_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
                    
                    if task_check_result is None:
                        self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.fail_json(msg="REST result is fault: " + stderr)
                    else:
                        if task_check_result.group(2) == "200":
                            try :
                                json_data = json.loads(task_check_result.group(1))
                            except Exception as e:
                                self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                                self.module.fail_json(msg="Not json format data: " + task_check_result.group(1))
                            status = json_data["IsmBody"]["Status"]
                        else:
                            self.module.log("Response Code=" + task_check_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                            self.module.fail_json(msg=task_check_result.group(1))
                            break
                        
                    # end loop if status is complete
                    if status == "Complete" or status == "Cancel-Complete":
                        result = json_data["IsmBody"]["Result"]
                        self.module.debug("***** waiting for task End *****")
                        break
                else:
                    self.module.log("waiting for task timeout: " + str(IsmUserSettingsValue.FIRMWARE_DOWNLOAD_TIME_OUT) + "s")
                    self.module.fail_json(msg="waiting for task timeout: " + str(IsmUserSettingsValue.FIRMWARE_DOWNLOAD_TIME_OUT) + "s")
                    break
                    
                # execute sleep
                time.sleep(common.SLEEP_SECOND)
                
            self.module.debug("***** taskCheck End *****")
            
            if result == "Error":
                errmsg = "[TaskId]=" + id + " "
                for SubTaskInfoList in json_data["IsmBody"]["SubTaskInfoList"]:
                    sub_task_id = SubTaskInfoList["SubTaskId"]
                    message = ""
                    if SubTaskInfoList["Message"] is not None:
                        message =  " [Message]=" + SubTaskInfoList["Message"]
                    action = ""
                    if SubTaskInfoList["Action"] is not None:
                        action = " [Action]=" + SubTaskInfoList["Action"]
                    task_msg = "[SubTaskId]=" + sub_task_id + message + action
                    errmsg = errmsg + task_msg + " "
                    self.module.log(task_msg)
                self.module.fail_json(msg=errmsg)
            else:
                self.module.debug("task result:" + result)
                return result
                
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))


IsmDownloadFirmware()
