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

class IsmMaintenanceModeSetting():

    # rest url
    MAINTENANCE_MODE_REST_URL = "/ism/api/v2/nodes/"
    NODE_DATA_REST_URL = "/ism/api/v2/nodes/"
    
    # receiving args
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(required=True),
            hostname=dict(required=True),
            mode=dict(required=True, choices=['On','Off'])
        )
    )
    
    def __init__(self):
        self.__present()
        
    def __present(self):
        try :
            self.module.log("argument_spec with config=" + str(self.module.params['config']) + " hostname=" + str(self.module.params['hostname']) + " mode=" + str(self.module.params['mode']))
            
            # instance of common class
            common = IsmCommon(self.module)
            
            # convert parameters to unicode string
            self.module.params['config'] = common.covert_unicode(self.module.params['config'])
            self.module.params['hostname'] = common.covert_unicode(self.module.params['hostname'])
            self.module.params['mode'] = common.covert_unicode(self.module.params['mode'])
            
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
            
            # License Check
            common.licenseCheck(usable_essential = True)
            
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
            
            # Check type and model of node are supporetd on Essential mode
            common.checkNodeSupportedOnEssential()
                
            mode = ""
            if self.module.params['mode'] == "On":
                mode = "Maintenance"
            elif self.module.params['mode'] == "Off":
                mode = "Normal"
            else:
                self.module.log("A value other than On or Off is specified for mode parameter: " + str(self.module.params['mode']))
                self.module.fail_json(msg="A value other than On or Off is specified for mode parameter: " + str(self.module.params['mode']))
                
            # check maintenance mode
            chk = self.checkMaintenanceMode(common, mode)
            
            # set maintenance mode
            if chk is True:
                result = self.maintenanceModeSetting(common, mode)
                changed_result = True
            else:
                result = "Success"
                changed_result = False
                
            # ISM logout
            common.ismLogout()
                
            # return json
            args = dict(
                ism_maintenance_mode = result
            )
            self.module.log("ism_maintenance_mode successful completion")
            self.module.exit_json(changed=changed_result, **args)
                
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
    def checkMaintenanceMode(self, common, mode):
        try :
            self.module.debug("***** checkMaintenanceMode Start *****")
            
            result = True
            
            # get rest url
            rest_url = common.getRestUrl(IsmMaintenanceModeSetting.NODE_DATA_REST_URL, common.getNodeId())
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + common.getSessionId() + "' "
            
            # execute rest
            exec_command = common.COMMAND + rest_url + common.HEADER + add_head + common.GET + common.HTTP_RESPONSE_CODE + common.CERTIFICATE + "'" + common.singleEscape(common.getIsmCertificate()) + "'"
            self.module.debug("exec_command = " + exec_command)
            
            (rc, stdout, stderr) = common.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)
            
            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
            
            check_maintenancce_mode_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if check_maintenancce_mode_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if check_maintenancce_mode_result.group(2) == "200":
                    try :
                        json_data = json.loads(check_maintenancce_mode_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.fail_json(msg="Not json format data: " + check_maintenancce_mode_result.group(1))
                else:
                    self.module.log("Response Code=" + check_maintenancce_mode_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=check_maintenancce_mode_result.group(1))
                
            if json_data["IsmBody"]["Node"]["MaintenanceMode"] == mode:
                result = False
            
            self.module.debug("***** checkMaintenanceMode End *****")
            
            return result
        except Exception, e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
    def maintenanceModeSetting(self, common, mode):
        try :
            self.module.debug("***** maintenanceModeSetting Start *****")
            
            # get rest url
            rest_url = common.getRestUrl(IsmMaintenanceModeSetting.MAINTENANCE_MODE_REST_URL, common.getNodeId()) + "/maintenancemode"
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + common.getSessionId() + "' "
            
            # execute rest
            param = " '{\"IsmBody\": {\"Node\": {\"MaintenanceMode\" : \"" + mode + "\"}}}' "
            exec_command = common.COMMAND + rest_url + common.HEADER + add_head + common.PATCH + param + common.HTTP_RESPONSE_CODE + common.CERTIFICATE + "'" + common.singleEscape(common.getIsmCertificate()) + "'"
            self.module.debug("exec_command = " + exec_command)
            
            (rc, stdout, stderr) = common.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)
            
            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
            
            maintenancce_mode_setting_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if maintenancce_mode_setting_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if maintenancce_mode_setting_result.group(2) == "200":
                    result = "Success"
                else:
                    self.module.log("Response Code=" + maintenancce_mode_setting_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=maintenancce_mode_setting_result.group(1))
            
            self.module.log("maintenanceModeSetting success")
            self.module.debug("***** maintenanceModeSetting End *****")
            
            return result
        except Exception, e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
IsmMaintenanceModeSetting()
