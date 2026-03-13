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
import time
import datetime
import socket
from os import path
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon
from ansible.module_utils.ism_user_settings import IsmUserSettingsValue

class IsmProfileAssignment():

    # constant
    SLEEP_SECOND = 10
    
    # rest url
    PROFILE_LIST_REST_URL = "/ism/api/v2/profiles/profiles"
    PROFILE_DATA_REST_URL = "/ism/api/v2/profiles/profiles/"
    PROFILE_ASSIGNMENT_REST_URL = "/ism/api/v2/nodes/"
    TASK_INFO_REST_URL = "/ism/api/v2/tasks/"
    
    # receiving args
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(required=True),
            hostname=dict(required=True),
            ism_profile_name=dict(required=True),
            assign_mode=dict(required=False, choices=['Normal','Advanced'], default="Normal"),
            advanced_kind=dict(required=False, choices=['ForcedAssign','WithoutHardwareAccess','OnlineAssign']),
            assign_range=dict(required=False, type='list')
        )
    )
    
    def __init__(self):
       self.__present()
       
    def __present(self):
        try :
            self.module.log("argument_spec with config=" + str(self.module.params['config']) + " hostname=" + str(self.module.params['hostname']) + " ism_profile_name=" + str(self.module.params['ism_profile_name']) + " assign_mode=" + str(self.module.params['assign_mode']) + " advanced_kind=" + str(self.module.params['advanced_kind']) + " assign_range=" + str(self.module.params['assign_range']))
            
            # instance of common class
            common = IsmCommon(self.module)
            
            # convert parameters to unicode string
            self.module.params['config'] = common.covert_unicode(self.module.params['config'])
            self.module.params['hostname'] = common.covert_unicode(self.module.params['hostname'])
            self.module.params['ism_profile_name'] = common.covert_unicode(self.module.params['ism_profile_name'])
            self.module.params['assign_mode'] = common.covert_unicode(self.module.params['assign_mode'])
            self.module.params['advanced_kind'] = common.covert_unicode(self.module.params['advanced_kind'])
            if self.module.params['assign_range'] is not None:
                for key in self.module.params['assign_range']:
                    key = common.covert_unicode(key)
                    
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
            
            # License Check
            common.licenseCheck()
            
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
                
            # get profileId
            profile_id = self.getProfileId(common)
            
            if profile_id == "":
                self.module.log("Profile name matching the profile name of the parameter could not be found. profile name:" + self.module.params['ism_profile_name'])
                self.module.fail_json(msg="Profile name matching the profile name of the parameter could not be found. profile name:" + self.module.params['ism_profile_name'])
                
            if self.module.params['assign_mode'] == "Advanced" and self.module.params['advanced_kind'] == "ForcedAssign":
                # profile assignment execution
                result = self.profileAssignment(common, profile_id)
                changed_result = True
            else:
                # check profile assignment
                chk = self.checkProfileAssignment(common, profile_id)
                
                # profile assignment execution
                if chk is True:
                    result = self.profileAssignment(common, profile_id)
                    changed_result = True
                else:
                    result = "Success"
                    changed_result = False
                
            # ISM logout
            common.ismLogout()
            
            # return json
            args = dict(
                ism_profile_assignment = result
            )
            self.module.log("ism_profile_assignment successful completion")
            self.module.exit_json(changed=changed_result, **args)
            
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
    def getProfileId(self, common):
        try :
            self.module.debug("***** getProfileId Start *****")
            
            profile_id = ""
            
            # get rest url
            rest_url = common.getRestUrl(IsmProfileAssignment.PROFILE_LIST_REST_URL)
            
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
                
            get_profile_id_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if get_profile_id_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if get_profile_id_result.group(2) == "200":
                    try :
                        json_data = json.loads(get_profile_id_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.fail_json(msg="Not json format data: " + get_profile_id_result.group(1))
                else:
                    self.module.log("Response Code=" + get_profile_id_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=get_profile_id_result.group(1))
                
            for list in json_data["IsmBody"]["ProfileList"]:
                if list["ProfileName"] == self.module.params['ism_profile_name']:
                    profile_id = list["ProfileId"]
                    
            self.module.debug("profile_id: " + profile_id)
            self.module.debug("***** getProfileId End *****")
            
            return profile_id
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
    def checkProfileAssignment(self, common, profile_id):
        try :
            self.module.debug("***** checkProfileAssignment Start *****")
            
            result = True
            
            # get rest url
            rest_url = common.getRestUrl(IsmProfileAssignment.PROFILE_DATA_REST_URL, profile_id)
            
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
                
            check_profile_assignment_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if check_profile_assignment_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if check_profile_assignment_result.group(2) == "200":
                    try :
                        json_data = json.loads(check_profile_assignment_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.fail_json(msg="Not json format data: " + check_profile_assignment_result.group(1))
                else:
                    self.module.log("Response Code=" + check_profile_assignment_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=check_profile_assignment_result.group(1))
                
            if json_data["IsmBody"]["Status"] == "assigned" and str(json_data["IsmBody"]["AssignedNodeId"]) == common.getNodeId():
                result = False
                
            self.module.debug("***** checkProfileAssignment End *****")
            
            return result
            
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
    def profileAssignment(self, common, profile_id):
        try :
            self.module.debug("***** profileAssignment Start *****")
            
            # get rest url
            rest_url = common.getRestUrl(IsmProfileAssignment.PROFILE_ASSIGNMENT_REST_URL, common.getNodeId()) + "/profiles/assign"
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + common.getSessionId() + "' "
            
            # execute rest
            if self.module.params['assign_mode'] == "Advanced":
                advanced_kind = self.module.params['advanced_kind']
                if advanced_kind is None:
                   advanced_kind = ""
                if self.module.params['assign_range'] is None:
                    param = " '{\"IsmBody\": {\"ProfileId\":\"" + profile_id + "\", \"AssignMode\":\"" + self.module.params['assign_mode'] + "\", \"AdvancedKind\":\"" + advanced_kind + "\" }}' "
                else:
                    assign_range_param = ""
                    assign_range_list = map(str, self.module.params['assign_range'])
                    assign_range_param = "\",\"".join(assign_range_list)
                    assign_range_param = "[\"" + assign_range_param + "\"]"
                    param = " '{\"IsmBody\": {\"ProfileId\":\"" + profile_id + "\", \"AssignMode\":\"" + self.module.params['assign_mode'] + "\", \"AdvancedKind\":\"" + advanced_kind + "\", \"AssignRange\":" + common.singleEscape(assign_range_param) + " }}' "
            else:
                param = " '{\"IsmBody\": {\"ProfileId\":\"" + profile_id + "\"}}' "
            exec_command = common.COMMAND + rest_url + common.HEADER + add_head + common.POST + param + common.HTTP_RESPONSE_CODE + common.CERTIFICATE + "'" + common.singleEscape(common.getIsmCertificate()) + "'"
            self.module.debug("exec_command = " + exec_command)
            
            (rc, stdout, stderr) = common.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)
            
            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
            
            profile_assignment_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if profile_assignment_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if profile_assignment_result.group(2) == "201":
                    try :
                        json_data = json.loads(profile_assignment_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.fail_json(msg="Not json format data: " + profile_assignment_result.group(1))
                    task_id = json_data["IsmBody"]["TaskId"]
                else:
                    self.module.log("Response Code=" + profile_assignment_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=profile_assignment_result.group(1))
            
            # task check
            if self.module.params['advanced_kind'] == "WithoutHardwareAccess":
                task_result = "Success"
            else:
                task_result = self.taskCheck(common, task_id)
            
            self.module.log("profileAssignment success")
            self.module.debug("***** profileAssignment End *****")
            
            return task_result
            
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))
            
    def taskCheck(self, common, task_id):
        try :
            self.module.debug("***** taskCheck Start *****")
            
            now = datetime.datetime.now()
            unix_time = long(time.mktime(now.timetuple()))
            time_out = long(unix_time) + long(IsmUserSettingsValue.PROFILE_ASSIGNMENT_TIME_OUT)
            
            # get rest url
            rest_url = common.getRestUrl(IsmProfileAssignment.TASK_INFO_REST_URL, task_id)
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + common.getSessionId() + "' "
            
            # waiting for task
            self.module.debug("***** waiting for task Start *****")
            while True:
            
                now = datetime.datetime.now()
                now_time = long(time.mktime(now.timetuple()))
                
                if long(now_time) < long(time_out):
                    # execute rest
                    exec_command = common.COMMAND + rest_url + common.HEADER + add_head + common.GET + common.HTTP_RESPONSE_CODE + common.CERTIFICATE + "'" + common.singleEscape(common.getIsmCertificate()) + "'"
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
                    self.module.log("waiting for task timeout: " + str(IsmUserSettingsValue.PROFILE_ASSIGNMENT_TIME_OUT) + "s")
                    self.module.fail_json(msg="waiting for task timeout: " + str(IsmUserSettingsValue.PROFILE_ASSIGNMENT_TIME_OUT) + "s")
                    break
                    
                # execute sleep
                time.sleep(IsmProfileAssignment.SLEEP_SECOND)
                
            self.module.debug("***** taskCheck End *****")
            
            if result == "Error":
                errmsg = "[TaskId]=" + task_id + " "
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
            
IsmProfileAssignment()
