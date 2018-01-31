#!/usr/bin/python
#coding: UTF-8

#######
# Copyright FUJITSU LIMITED 2017-2018
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

# import
import json
import re
import copy
import socket
from os import path
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon
from ansible.module_utils.ism_user_settings import IsmUserSettingsValue

class IsmFirmwareList():
    
    # rest url
    FIRMWARE_LIST_REST_URL = "/ism/api/v2/system/settings/firmware/list"

    # receiving args
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(required=True),
            hostname=dict(required=True),
            firmware_type=dict(required=False, choices=['BIOS','iRMC','FC','CNA','ETERNUS DX','LAN Switch','ETERNUS AF','PRIMEQUEST'])
        )
    )
    
    def __init__(self):
       self.__present()
       
    def __present(self):
        try :
            self.module.log("argument_spec with config=" + str(self.module.params['config']) + " hostname=" + str(self.module.params['hostname']) + " firmware_type=" + str(self.module.params['firmware_type']))
            
            # instance of common class
            common = IsmCommon(self.module)
            
            # convert parameters to unicode string
            self.module.params['config'] = common.covert_unicode(self.module.params['config'])
            self.module.params['hostname'] = common.covert_unicode(self.module.params['hostname'])
            self.module.params['firmware_type'] = common.covert_unicode(self.module.params['firmware_type'])
            
            # config file open
            try :
                config_path = path.abspath(self.module.params['config'])
                f = open(config_path)
            except Exception as e:
                self.module.log("file open error: " + str(config_path) + ", e=" + str(e))
                self.module.fail_json(msg="file open error: " + str(config_path))
            
            # config loads
            try :
                json_data = json.load(f)
            except Exception as e:
                f.close()
                self.module.log("Not json format data: " + str(config_path) + ", e=" + str(e))
                self.module.fail_json(msg="It is not json format data: " + str(config_path))
                
            f.close()
            
            # ip transformation
            match = re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', self.module.params['hostname'])
            if match == None:
                try :
                    self.module.params['hostname'] = socket.gethostbyname(self.module.params['hostname'])
                    self.module.debug("Host name is converted to IP address: " + str(self.module.params['hostname']))
                except Exception as e:
                    self.module.log("ip transformation error: IP address=" + str(self.module.params['hostname']) + ", e=" + str(e))
                    self.module.fail_json(msg="Host name could not be converted to IP address: " + str(self.module.params['hostname']))
                    
            # ISM login
            common.ismLogin(json_data)
            
            # get node OS
            common.getNodeOS()
            
            # get node hard
            if common.getNodeId() == "":
                common.getNodeHard()
                
            # node check
            if common.getNodeId() == "":
                self.module.log("The target host name was not found.: " + str(self.module.params['hostname']))
                self.module.fail_json(msg="The target host name was not found.: " + str(self.module.params['hostname']))
            else:
                self.module.debug("node_id: " + str(common.getNodeId()))
                
            # firmware list execution
            result = self.execFirmwareList(common)
            
            # ISM logout
            common.ismLogout()
            
            # return json
            changed_result = False
            self.module.log("ism_firmware_list successful completion")
            self.module.exit_json(changed=changed_result, ism_firmware_list=result)
            
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
    def execFirmwareList(self, common):
        try :
            self.module.debug("***** execFirmwareList Start *****")
            
            # get rest url
            rest_url = common.getRestUrl(IsmFirmwareList.FIRMWARE_LIST_REST_URL, "?nodeid=" + common.getNodeId())
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + common.getSessionId() + "' "
            
            # execute rest
            exec_command = common.COMMAND + rest_url + common.HEADER + add_head + common.GET + common.HTTP_RESPONSE_CODE + common.CERTIFICATE + "'" + common.singleEscape(common.getIsmCertificate()) + "'"
            self.module.debug("exec_command = " + exec_command)
            
            (rc, stdout, stderr) = common.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + str(stdout))
            
            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
                
            exec_firmwarelist_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if exec_firmwarelist_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if exec_firmwarelist_result.group(2) == "200":
                    try :
                        json_data = json.loads(exec_firmwarelist_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.fail_json(msg="Not json format data: " + exec_firmwarelist_result.group(1))
                else:
                    self.module.log("Response Code=" + exec_firmwarelist_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=exec_firmwarelist_result.group(1))
                
            if self.module.params['firmware_type'] != None:
                list_firmware_type = copy.deepcopy(json_data)
                del list_firmware_type["IsmBody"]["FirmwareList"]
                list_firmware_type["IsmBody"]["FirmwareList"] = []
                
                for list in json_data["IsmBody"]["FirmwareList"]:
                    if list["FirmwareType"] == self.module.params['firmware_type']:
                        list_firmware_type["IsmBody"]["FirmwareList"].append(list)
                            
                list_firmware_name = copy.deepcopy(list_firmware_type)
                del list_firmware_name["IsmBody"]["FirmwareList"]
                list_firmware_name["IsmBody"]["FirmwareList"] = []
                
                i = 0
                for list in list_firmware_type["IsmBody"]["FirmwareList"]:
                    if i == 0:
                        list_firmware_name["IsmBody"]["FirmwareList"].append(list)
                    elif list_firmware_type["IsmBody"]["FirmwareList"][i-1]["FirmwareName"] != list["FirmwareName"]:
                        list_firmware_name["IsmBody"]["FirmwareList"].append(list)
                    i += 1
                        
                self.module.log("execFirmwareList success")
                self.module.debug("***** execFirmwareList End *****")
                
                return list_firmware_name
            else:
                self.module.log("execFirmwareList success")
                return json_data
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
IsmFirmwareList()
