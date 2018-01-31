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
import socket
from os import path
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon
from ansible.module_utils.ism_user_settings import IsmUserSettingsValue

class IsmPowerOn():
    
    # rest url
    POWER_CONTROL_REST_URL = "/ism/api/v2/nodes/"
    
    # receiving args
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
            
            # instance of common class
            common = IsmCommon(self.module)
            
            # convert parameters to unicode string
            self.module.params['config'] = common.covert_unicode(self.module.params['config'])
            self.module.params['hostname'] = common.covert_unicode(self.module.params['hostname'])
            
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
            if match is None:
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
                self.module.debug("node_id: " + common.getNodeId())
                
            # check powercontrol
            chk = self.checkPowerControl(common)
            
            # power on execution
            if chk is True:
                result = self.powerOn(common)
                changed_result = True
            else:
                result = "Success"
                changed_result = False
            
            # ISM logout
            common.ismLogout()
            
            # return json
            args = dict(
                ism_power_on = result
            )
            self.module.log("ism_power_on successful completion")
            self.module.exit_json(changed=changed_result, **args)
            
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
    def checkPowerControl(self, common):
        try :
            self.module.debug("***** checkPowerControl Start *****")
            
            result = True
            
            # get rest url
            rest_url = common.getRestUrl(IsmPowerOn.POWER_CONTROL_REST_URL, common.getNodeId() + "/power")
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + common.getSessionId() + "' "
            
            # execute rest
            exec_command = common.COMMAND + rest_url + common.HEADER + add_head + common.HTTP_RESPONSE_CODE + common.CERTIFICATE + "'" + common.singleEscape(common.getIsmCertificate()) + "'" 
            self.module.debug("exec_command = " + exec_command)
            
            (rc, stdout, stderr) = common.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)
            
            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
                
            check_power_control_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if check_power_control_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if check_power_control_result.group(2) == "200":
                    try :
                        json_data = json.loads(check_power_control_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.fail_json(msg="Not json format data: " + check_power_control_result.group(1))
                else:
                    self.module.log("Response Code=" + check_power_control_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=check_power_control_result.group(1))
            
            if len(json_data["IsmBody"]["Parts"]) != 0:
                if json_data["IsmBody"]["Parts"][0]["PowerStatus"] is not None and json_data["IsmBody"]["Parts"][0]["PowerStatus"] == "On":
                    result = False
                
            self.module.debug("***** checkPowerControl End *****")
            
            return result
            
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
    def powerOn(self, common):
        try :
            self.module.debug("***** powerOn Start *****")
            
            result = ""
            
            # get rest url
            rest_url = common.getRestUrl(IsmPowerOn.POWER_CONTROL_REST_URL, common.getNodeId() + "/power")
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + common.getSessionId() + "' "
            
            # execute rest
            param = " '{\"IsmBody\":{\"Parts\":[{\"Name\" :\"PowerManagement\", \"PowerStatus\":\"PowerOn\"}]}}' "
            exec_command = common.COMMAND + rest_url + common.HEADER + add_head + common.PATCH + param + common.HTTP_RESPONSE_CODE + common.CERTIFICATE + "'" + common.singleEscape(common.getIsmCertificate()) + "'" 
            self.module.debug("exec_command = " + exec_command)
            
            (rc, stdout, stderr) = common.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)
            
            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
                
            power_on_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if power_on_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if power_on_result.group(2) == "200":
                    result = "Success"
                else:
                    self.module.log("Response Code=" + power_on_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=power_on_result.group(1))
                
            self.module.log("powerOn success")
            self.module.debug("***** powerOn End *****")
            
            return result
            
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
IsmPowerOn()
