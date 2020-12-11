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

class IsmFirmwareUpdate():

    # constant
    SLEEP_SECOND = 30

    # rest url
    FIRMWARE_LIST_REST_URL = "/ism/api/v2/system/settings/firmware/list"
    FIRMWARE_UPDATE_REST_URL = "/ism/api/v2/nodes/firmware/update"
    TASK_INFO_REST_URL = "/ism/api/v2/tasks/"
    INVENTORY_INFO_REST_URL = "/ism/api/v2/nodes/"

    # receiving args
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(required=True),
            hostname=dict(required=True),
            firmware_update_list=dict(required=True, type="list"),
        ),
                supports_check_mode=True
    )

    def __init__(self):
       self.__present()

    def __present(self):
        try :
            self.module.log("argument_spec with config=" + str(self.module.params['config']) + " hostname=" + str(self.module.params['hostname']) + " firmware_update_list=" + str(self.module.params['firmware_update_list']))

            # instance of common class
            common = IsmCommon(self.module)

            # param check
            common.param_check(self.module.params['firmware_update_list'])

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
                
            # firmware update execution
            firmware_update_list = []
            for update_param_hash in self.module.params['firmware_update_list']:

                if "firmware_version" in update_param_hash:
                    self.module.debug("***** firmwareversion specified *****")

                    if update_param_hash['firmware_version'] == "" or update_param_hash['firmware_version'] == None:
                        # latest firmware version
                        latest_firmware_version = self.getFirmwareVersion(common, update_param_hash['firmware_name'], update_param_hash['operation_mode'])
                        update_param_hash['firmware_version'] = latest_firmware_version

                else:
                    self.module.debug("***** firmwareversion not specified *****")

                    # latest firmware version
                    latest_firmware_version = self.getFirmwareVersion(common, update_param_hash['firmware_name'], update_param_hash['operation_mode'])
                    update_param_hash['firmware_version'] = latest_firmware_version

                # check firmware version
                current_version = self.getCurrentFirmwareVersion(common, update_param_hash['firmware_name'])
                if current_version != update_param_hash['firmware_version']:
                    update_param_hash['firmware_current_version'] = current_version
                    firmware_update_list.append(update_param_hash)

            # firmware update start execution
            if len(firmware_update_list) == 0:
                result = "Success"
                changed_result = False
            else:
                if self.module.check_mode:
                    result = dict( changed=True, original_message='', message="Firmware versions that would be changed: " + str(firmware_update_list))
                    self.module.exit_json(**result)
                else:
                    result = self.firmwareUpdate(common, firmware_update_list)
                    changed_result = True

            # ISM logout
            common.ismLogout()

            # return json
            args = dict(
                ism_firmware_update = result
            )
            self.module.log("ism_firmware_update successful completion")
            self.module.exit_json(changed=changed_result, **args)
        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))

    def getFirmwareVersion(self, common, firmware_name, operation_mode):
        try :
            self.module.debug("***** getFirmwareVersion Start *****")

            result_version = ""

            # get rest url
            rest_url = common.getRestUrl(IsmFirmwareUpdate.FIRMWARE_LIST_REST_URL, "?nodeid=" + common.getNodeId())

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

            get_firmware_list_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))

            if get_firmware_list_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if get_firmware_list_result.group(2) == "200":
                    try :
                        json_data = json.loads(get_firmware_list_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.fail_json(msg="Not json format data: " + get_firmware_list_result.group(1))
                else:
                    self.module.log("Response Code=" + get_firmware_list_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=get_firmware_list_result.group(1))

            for list in json_data["IsmBody"]["FirmwareList"]:
                if (list["FirmwareName"] == firmware_name) and (list["OperationMode"] == operation_mode):
                    result_version = list["FirmwareVersion"]
                    break

            self.module.debug("***** getFirmwareVersion End *****")

            return result_version

        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))

    def getCurrentFirmwareVersion(self, common, firmware_name):
        try :
            self.module.debug("***** getCurrentFirmwareVersion Start *****")

            result = True

            # get rest url
            rest_url = common.getRestUrl(IsmFirmwareUpdate.INVENTORY_INFO_REST_URL, common.getNodeId() + "/inventory/?level=All\&target=Firmware")

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

            check_firmware_version_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))

            if check_firmware_version_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if check_firmware_version_result.group(2) == "200":
                    try :
                        json_data = json.loads(check_firmware_version_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.fail_json(msg="Not json format data: " + check_firmware_version_result.group(1))
                else:
                    self.module.log("Response Code=" + check_firmware_version_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=check_firmware_version_result.group(1))

            if "Firmware" in json_data["IsmBody"]["Node"]["VariableData"]:
                if json_data["IsmBody"]["Node"]["VariableData"]["Firmware"] is not None:
                    for list in json_data["IsmBody"]["Node"]["VariableData"]["Firmware"]:
                        if (list["Name"] == firmware_name):
                            return list["FirmwareVersion"]

            self.module.debug("***** getCurrentFirmwareVersion End *****")

            return result

        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))

    def firmwareUpdate(self, common, firmware_update_list):
        try :
            self.module.debug("***** firmware_update Start *****")

            # get rest url
            rest_url = common.getRestUrl(IsmFirmwareUpdate.FIRMWARE_UPDATE_REST_URL)

            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + common.getSessionId() + "' "

            # create rest param
            param_prefix = " '{\"IsmBody\":{\"UpdateRequest\":["
            param_suffix = "]}}' "
            param_array = []
            for firmwareUpdate_key in firmware_update_list:
                param_tmp = "{\"NodeId\":" + common.getNodeId() + \
                            ",\"FirmwareName\":\"" + common.singleEscape(firmwareUpdate_key['firmware_name']) + \
                            "\",\"RepositoryName\":\"" + common.singleEscape(firmwareUpdate_key['repository_name']) + \
                            "\",\"FirmwareVersion\":\"" + common.singleEscape(firmwareUpdate_key['firmware_version']) + \
                            "\",\"OperationMode\":\"" + firmwareUpdate_key['operation_mode'] + \
                            "\"}"
                param_array.append(param_tmp)
            param = param_prefix + ",".join(param_array) + param_suffix

            # execute rest
            exec_command = common.COMMAND + rest_url + common.HEADER + add_head + common.POST + param + common.HTTP_RESPONSE_CODE + common.CERTIFICATE + "'" + common.singleEscape(common.getIsmCertificate()) + "'"
            self.module.debug("exec_command = " + exec_command)

            (rc, stdout, stderr) = common.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)

            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)

            firmware_update_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))

            if firmware_update_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if firmware_update_result.group(2) == "201":
                    try :
                        json_data = json.loads(firmware_update_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.fail_json(msg="Not json format data: " + firmware_update_result.group(1))
                    task_id = json_data["IsmBody"]["TaskId"]
                else:
                    self.module.log("Response Code=" + firmware_update_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=firmware_update_result.group(1))

            # task check
            task_result = self.taskCheck(task_id, common)

            self.module.log("firmwareUpdate success")
            self.module.debug("***** firmware_update End *****")

            return task_result

        except Exception as e:
            self.module.log(str(e))
            self.module.fail_json(msg=str(e))

    def taskCheck(self, id, common):
        try :
            self.module.debug("***** taskCheck Start *****")

            now = datetime.datetime.now()
            unix_time = long(time.mktime(now.timetuple()))
            time_out = long(unix_time) + long(IsmUserSettingsValue.FIRMWARE_UPDATE_TIME_OUT)

            # get rest url
            rest_url = common.getRestUrl(IsmFirmwareUpdate.TASK_INFO_REST_URL, id)

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
                    self.module.log("waiting for task timeout: " + str(IsmUserSettingsValue.FIRMWARE_UPDATE_TIME_OUT) + "s")
                    self.module.fail_json(msg="waiting for task timeout: " + str(IsmUserSettingsValue.FIRMWARE_UPDATE_TIME_OUT) + "s")
                    break

                # execute sleep
                time.sleep(IsmFirmwareUpdate.SLEEP_SECOND)

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

IsmFirmwareUpdate()
