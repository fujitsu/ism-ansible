#!/usr/bin/python
#coding: UTF-8

#######
# Copyright FUJITSU LIMITED 2017-2020
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
import traceback
from os import path
from distutils.version import StrictVersion
from ansible.module_utils.ism_user_settings import IsmUserSettingsValue
from ansible.module_utils.ism_essential_not_supported_model import IsmEssentialNotSupportedModel

# common class
class IsmCommon:

    # constant
    TIME_OUT_SECOND = "60"
    COMMAND = "curl -S -s -m " + TIME_OUT_SECOND + " "
    COMMAND_TIMEOUT_FREE = "curl -S -s -m "
    GET = " -X GET "
    POST = " -X POST -d "
    PATCH = " --request PATCH -d "
    HEADER = " -H 'Content-Type: application/json' "
    HTTP_RESPONSE_CODE = " -w 'ISM_HTTP_RESPONSE_CODE=%{http_code}' "
    CERTIFICATE = " --cacert "
    UNICODE_STRING = "utf-8"
    SLEEP_SECOND = 30
    
    ISM_REFRESH_NODE_INFO_SLEEP_SECOND = 10
    ADD_HEADER = " -H 'X-Ism-Authorization: " 
    RESPONSE_CODE_200 = "200"
    RESPONSE_CODE_201 = "201"
    
    # Parameter check flag of ism monitoring setting module
    ISM_REGISTER_MONITORING_SETTING_PARAMETER_CHECK = True
    
    # Operation mode essential
    OPE_MODE_ESSENTIAL = "Essential"
    
    # rest url
    LOGIN_REST_URL = "/ism/api/v2/users/login"
    GET_NODE_OS_REST_URL = "/ism/api/v2/nodes/os"
    LOGOUT_REST_URL = "/ism/api/v2/users/logout"
    NODE_LIST_REST_URL = "/ism/api/v2/nodes"
    
    NODES_REST_URL = "/ism/api/v2/nodes/"
    EVENT_LOG_LIST_REST_URL = "/ism/api/v2/event/history/event/show"
    PROFILE_LIST_REST_URL = "/ism/api/v2/profiles/profiles"
    FIRMWARE_URL = "/ism/api/v2/system/settings/firmware/"
    FIRMWARE_INVENTORY_REST_URL = "/ism/api/v2/nodes/inventory/"
    TASK_INFO_REST_URL = "/ism/api/v2/tasks/"
    SYSTEM_URL = "/ism/api/v2/system/"
    ISMVA_SETTINGS_URL = "/ism/api/v2/ismva/settings"
    
    # message
    MSG_NO_VALUE_KEY = 'no value key: '
    MSG_MISSING_REQUIRED_ARGUMENTS = 'missing required arguments: '
    MSG_VALUE_OF = 'value of '
    MSG_MUST_BE_ONE_OF = ' must be one of: ' 
    MSG_GOT = ' got: ' 
    MSG_VALID_INPUT_RANGE = 'The valid input range is '
    MSG_NOT_SUPPORT_PARAMETER = 'not support parameter: '
    MSG_NOT_SUPPORTED_PARAMETER_ESSENTIAL = 'not supported parameter on Essential mode: '
    MSG_NOT_SUPPORTED_TYPE_MODE_ESSENTIAL = 'The node type and model are not supported on Essential mode. Node type: {0}, model: {1}'
    MSG_SUPPORT_PARAMETER_DICT = 'Specify the value as a dictionary type. :'
    MSG_SUPPORT_PARAMETER_STR = 'Specify the value as a string type. :'
    
    # monitoring setting add message
    MSG_ENTER_VALUES_IN_THE_RIGHT_FORMAT = 'Enter values in the right format. :'
    MSG_VALUE_SMALLER_UPPER_WARNING  = 'Enter a value smaller than upper_critical. : upper_warning'
    MSG_VALUE_SMALLER_LOWER_WARNING  = 'Enter a value smaller than upper_critical, upper_warning. : lower_warning'
    MSG_VALUE_SMALLER_LOWER_CRITICAL = 'Enter a value smaller than upper_critical, upper_warning, lower_warning. : lower_critical'
    MSG_THERE_ARE_NO_REGISTERABLE_MONITORING_ITEMS = 'There are no registerable monitoring items. :'
    MSG_NO_THRESHOLD_CAN_BE_SET = 'No threshold can be set for this monitoring item. :'
    MSG_IN_ORDER_TO_ENABLE_THRESHOLD_VALUE_MONITORING = 'In order to enable threshold value monitoring, performance monitoring (is_active) should be enabled.'
    MSG_SPECIFIABLE_RANGE_OF_THRESHOLD_VALUE = 'The threshold value can be specified in the range of [-1000000000000~1000000000000].'
    MSG_THE_SIXTH_DECIMAL_PLACE = 'The threshold can be specified up to 6 decimal places.'
    MSG_THRESHOLD_VALUE_MONITORING_IS_DISABLED = 'If the status of Threshold monitoring (is_threshold_monitoring_active) is disabled, the information of the threshold (upper_critical, upper_warning, lower_warning, lower_critical) cannot be specified.'

    ESSENTIAL_NOT_SUPPORTED_KEYS_INVENTORY = [
        'HardwareLogTarget',
        'RaidLogTarget',
        'ServerViewLogTarget',
        'SoftwareLogTarget'
    ]

    ESSENTIAL_NOT_SUPPORTED_KEYS_NODELIST = [
        'MountType',
        'Outlet',
        'PduPosition',
        'RackInfo'
    ]

    OPENSSL_DEC = [u"openssl", u"enc", u"-aes-256-cbc", u"-d", u"-A", u"-base64",
                   u"-md", u"md5", u"-pass"]

    ##
    
    def __init__(self, module):
        self.ism_ip = ""
        self.ism_port_no = ""
        self.user_name = ""
        self.password = ""
        self.certificate = ""
        self.session_id = ""
        self.node_id = ""
        self.module = module
        self.operation_mode = ""
        
#   ***** set method *****

    # set the ip address of ISM
    def setIsmIp(self, ism_ip):
        self.ism_ip = ism_ip

    # set port number of ISM
    def setIsmPortNo(self, ism_port_no):
        self.ism_port_no = ism_port_no

    # set login user name of ISM
    def setIsmUserName(self, user_name):
        self.user_name = user_name

    # set login password of ISM
    def setIsmPassword(self, password):
        self.password = password

    # set certificate of ISM
    def setIsmCertificate(self, certificate):
        self.certificate = certificate

    # set session id
    def setSessionId(self, session_id):
        self.session_id = session_id

    # set node id
    def setNodeId(self, node_id):
        self.node_id = str(node_id)
        
    # set operation mode
    def setOperationMode(self, operation_mode):
        self.operation_mode = operation_mode

#   ***** set method *****



#   ***** get method *****

    # get ip of ISM
    def getIsmIp(self):
        return self.ism_ip

    # get port number of ISM
    def getIsmPortNo(self):
        return self.ism_port_no

    # get login user name of ISM
    def getIsmUserName(self):
        return self.user_name

    # get login password of ISM
    def getIsmPassword(self):
        return self.password

    # get certificate of ISM
    def getIsmCertificate(self):
        return self.certificate

    # get session id
    def getSessionId(self):
        return self.session_id

    # get node id
    def getNodeId(self):
        return self.node_id

    # get operation mode
    def getOperationMode(self):
        return self.operation_mode

    # get rest url
    def getRestUrl(self, rest_url, param = ""):
        if param != "":
            rest_url = "https://" + self.getIsmIp() + ":" + self.getIsmPortNo() + rest_url + str(param)
        else:
            rest_url = "https://" + self.getIsmIp() + ":" + self.getIsmPortNo() + rest_url
        return rest_url
        
#   ***** get method *****

#   ***** is method *****

    # is Essential mode
    def isEssentialMode(self):
        if self.getOperationMode() == self.OPE_MODE_ESSENTIAL:
            return True
        else:
            return False

#   ***** is method *****

#   ***** escape method *****
    # singlequote escape
    def singleEscape(self, str):
        escape_str = str.replace("'","'\\''")
        return escape_str

#   ***** escape method *****


#   *****  unicode method *****
    # run_command_unicode
    def run_command_unicode(self, exec_command, data=None):
        if data:
            (rc, stdout, stderr) = self.module.run_command(exec_command, data=data)
        else:
            (rc, stdout, stderr) = self.module.run_command(exec_command)
        return (rc, unicode(stdout, IsmCommon.UNICODE_STRING), unicode(stderr, IsmCommon.UNICODE_STRING))

    # convert to unicode string
    def covert_unicode(self, str_var):

        # dict
        if isinstance(str_var, dict):
            return str_var
        # list
        if isinstance(str_var, list):
            return str_var
        # int
        if isinstance(str_var, int):
            return str_var

        if str_var is not None:
            convert_str = unicode(str_var, IsmCommon.UNICODE_STRING)
            return convert_str
        else:
            return str_var

    """
    @Description Function to covert unicode hash dict
    @param       class hash_dict
    """
    def covertUnicodeHashDict(self, hash_dict):
        self.module.debug("***** covertUnicodeHashDict Start *****")
        if not isinstance(hash_dict , dict):
            self.errorMessage(IsmCommon.MSG_SUPPORT_PARAMETER_DICT + str(hash_dict))
        
        for key, value in hash_dict.items():
            self.module.debug(" dict key :" + str(key) + " value :" + str(value) )
            if isinstance(value ,str):
                hash_dict[key] = self.covert_unicode(value)
            
            elif isinstance(value ,dict):
                self.covertUnicodeHashDict(value)
            
            else:
                continue
        self.module.debug("***** covertUnicodeHashDict End *****")

    """
    @Description Function to covert unicode hash list
    @param       class hash_list
    """
    def covertUnicodeHashList(self, hash_list):
        self.module.debug("***** covertUnicodeHashList Start *****")
        for hash in hash_list:
            if not isinstance(hash , dict):
                self.errorMessage(IsmCommon.MSG_SUPPORT_PARAMETER_DICT + str(hash_list))
        
            for key , value in hash.items():
                # Assumed data 
                # ex) [{"data1" : "value1"}]
                if isinstance(value ,str):
                    hash[key] = self.covert_unicode(value)
                # Assumed data 
                # ex) [{"data1" : {"data2" : "value2"}}]
                elif isinstance(value ,dict):
                    self.module.debug("dict :" + str(value))
                    self.covertUnicodeHashDict(value)
                else:
                    continue
                    
        self.module.debug("***** covertUnicodeHashList End *****")

    """
    @Description Function to covert unicode hash list
    @param       class common, hash_list
    """
    def covert_unicode_hash_list(self, str_var,required_keys):
        self.module.log("***** covert_unicode_hash_list Start *****")
        for param_hash in str_var:
            for key in required_keys:
                if key not in param_hash:
                    self.module.log("missing required arguments: " + key)
                    self.module.fail_json(msg="missing required arguments: " + key)
                if param_hash[key] is None:
                    self.module.log("no value key: " + key)
                    self.module.fail_json(msg="no value key: " + key)
                param_hash[key] = self.covert_unicode(param_hash[key])

        self.module.log("***** covert_unicode_hash_list End *****")

    # REST-API Specification
    #   The case for null = No , "" = No 
    # The list type is not covert_unicode, covert_unicode inside the loop.
    # First argument  : Target hash list.  type = list
    # Second argument : Required key name. type = list
    def covert_unicode_hash_list_not_none_and_empty(self, target_hash_list,required_keys):
        self.module.log("***** covert_unicode_hash_list_not_none_and_empty Start *****")
        for param_hash in target_hash_list:
            for key in required_keys:
                if key not in param_hash:
                    self.errorMessage(IsmCommon.MSG_MISSING_REQUIRED_ARGUMENTS + str(key))
                if param_hash[key] == "" or param_hash[key] is None:
                    self.errorMessage(IsmCommon.MSG_NO_VALUE_KEY + str(key))
                param_hash[key] = self.covert_unicode(param_hash[key])

        self.module.log("***** covert_unicode_hash_list_not_none_and_empty End *****")
#   ***** unicode method *****
#   ***** param check method *****
 
    """
    @Description required_param_check (whether "" or None)
    @param value check target
    @param key parameter name for error message
    """
    # required_param_check
    def required_param_check(self, value, key):
        if value == "" or value is None:
            self.errorMessage(IsmCommon.MSG_MISSING_REQUIRED_ARGUMENTS + key)

    # param check for firmware_update_list
    def param_check(self, firmware_update_list):
        required_keys = ["firmware_name", "repository_name", "operation_mode"]
        
        # firmware_update_list
        # [
        #    {'repository_name': 'Individual Repository Administrator',
        #     'firmware_version': '8.43F&3.60',
        #     'operation_mode': 'Online',
        #     'firmware_name': 'RX200 S8_iRMC'
        #     },
        #    {'repository_name': 'Individual Repository Administrator',
        #     'firmware_version': 'R1.11.0',
        #     'operation_mode': 'Online',
        #     'firmware_name': 'RX200 S8_BIOS'
        #    }
        # ]
        
        for param_hash in firmware_update_list:
            for key in required_keys:
                if key not in param_hash:
                    self.module.log("missing required arguments: " + key)
                    self.module.fail_json(msg="missing required arguments: " + key)
                if param_hash[key] == "" or param_hash[key] is None:
                    self.module.log("no value key: " + key)
                    self.module.fail_json(msg="no value key: " + key)
                param_hash[key] = self.covert_unicode(param_hash[key])
                
            if "firmware_version" in param_hash:
                param_hash['firmware_version'] = self.covert_unicode(param_hash['firmware_version'])
                
    """
    @Description Convert from null to blank
    @param       dict params
    @return      dict params
    """
    def convertNull(self, params, paramListNotBlank):
        
        for key, value in params.items():
            if key in paramListNotBlank:
                continue
            
            if value is None:
                params[key] = ""
                
        return params
        
#   ***** param check method *****


#   ***** common function *****

    """
    @Description Function pre-process
    @param       dict params
    """
    def preProcess(self, params, NodeCheck=True, paramListNotBlank=[], hostNameCheck=False,
                   licenseCheck=True, usableEssential=False, doIsmLogin=True, noHost=False):
        try :
            # Convert from null to blank
            params = self.convertNull(params, paramListNotBlank)
            
            # Convert from parameters to unicode string
            for key, value in params.items():
                value = self.covert_unicode(value)
            
            # Config file open
            try :
                config_path = path.abspath(params['config'])
                f = open(config_path)
            except Exception as e:
                self.module.log("file open error: " + config_path + ", e=" + str(e))
                self.module.log(traceback.format_exc())
                self.module.fail_json(msg="file open error: " + config_path)
                
            # Config file loads
            try :
                json_data = json.load(f)
                self.ism_config_json = json_data
            except Exception as e:
                f.close()
                self.module.log("Not json format data: " + config_path + ", e=" + str(e))
                self.module.log(traceback.format_exc())
                self.module.fail_json(msg="It is not json format data: " + config_path)
            f.close()
            
            # tha case of hostNameCheck:False
            # If the hostname is ""  , hostname is "0.0.0.0".
            # If the hostname is None, a type error occurs during Ip conversion.
            if noHost == False:
                if hostNameCheck == True :
                    if params['hostname'] == None or params['hostname'] == "":
                        self.errorMessage(IsmCommon.MSG_NO_VALUE_KEY + "hostname")
                
                # Ip transformation
                if params['hostname']!=None:
                    match = re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', params['hostname'])
                    if match is None:
                        try :
                            params['hostname'] = socket.gethostbyname(params['hostname'])
                            self.module.debug("Host name is converted to IP address: " + params['hostname'])
                        except Exception as e:
                            self.module.log("ip transformation error: Hostname=" + params['hostname'] + ", e=" + str(e))
                            self.module.log(traceback.format_exc())
                            self.module.fail_json(msg="Host name could not be converted to IP address: " + params['hostname'])
            # ISM login
            if doIsmLogin:
                self.ismLogin(json_data)
            else:
                # don't check license, node
                return
            
            # ISM licenseCheck
            self.licenseCheck(license_check = licenseCheck, usable_essential = usableEssential)
            
            if NodeCheck:
                # Get node ID of OS
                self.getNodeOS()
                
                # Get node ID of hardware
                if self.getNodeId() == "":
                    self.getNodeHard()
                    
                # Check node ID
                if self.getNodeId() == "":
                    self.module.log("The target host name was not found.: " + params['hostname'])
                    self.module.fail_json(msg="The target host name was not found.: " + params['hostname'])
                
                # Check type and model of node are supporetd on Essential mode
                self.checkNodeSupportedOnEssential()

        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    """
    @Description REST API execution
    @param       string rest_url
    @param       string method (GET, POST, PATCH)
    @param       string response_code
    @param       string body
    @return      dict json_data
    """
    def execRest(self, rest_url, method, response_code, body = "",timeout = "60"):
        try :
            # Adding a response header
            add_header = IsmCommon.ADD_HEADER + self.getSessionId() + "' "
            
            if timeout == "60":
                exec_command = self.COMMAND + rest_url + self.HEADER + add_header + method + body + \
                   self.HTTP_RESPONSE_CODE + self.CERTIFICATE + "'" + self.singleEscape(self.getIsmCertificate()) + "'"
            else:
                exec_command = self.COMMAND_TIMEOUT_FREE + timeout + " " + rest_url + self.HEADER + add_header + method + body + \
                   self.HTTP_RESPONSE_CODE + self.CERTIFICATE + "'" + self.singleEscape(self.getIsmCertificate()) + "'"
            
            # Command execution
            self.module.debug("exec_command = " + exec_command)
            
            # REST execution
            (rc, stdout, stderr) = self.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)
            
            if rc != 0:
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
            
            result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if result.group(2) == response_code:
                    try :
                        json_data = json.loads(result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.log(traceback.format_exc())
                        self.module.fail_json(msg="Not json format data: " + result.group(1))
                else:
                    self.module.log("Response Code=" + result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=result.group(1))
                    
            return json_data
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
        
    """
    @Description Function getQueryParam
    @param       dict dict_param
    @return      string param
    """
    def getQueryParam(self, dict_param):
        try :
            param = ""
            for key, value in dict_param.items():
                if value != "" and param == "":
                    param = "?" + key + "=" + value
                elif value != "" and param != "":
                    param = param + "\&" + key + "=" + value
            return param
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    # ism login
    def ismLogin(self, data):
        try :
            self.module.debug("***** ismLogin Start *****")
            
            # setting up ISM connection infomation
            self.setIsmIp(data["ip"])
            self.setIsmPortNo(data["portNo"])
            self.setIsmUserName(data["credentials"]["userName"])
            self.setIsmPassword(data["credentials"]["password"])
            self.setIsmCertificate(data["certificate"])
            
            # get rest url
            rest_url = self.getRestUrl(IsmCommon.LOGIN_REST_URL)
            
            # execute rest
            param =  " '{\"IsmBody\": {\"UserName\":\"" + self.getIsmUserName() + "\",\"Password\":\"" + self.getIsmPassword() + "\"}}' "
            exec_command = IsmCommon.COMMAND + rest_url + IsmCommon.HEADER + IsmCommon.POST + param + IsmCommon.HTTP_RESPONSE_CODE + IsmCommon.CERTIFICATE + "'" + self.singleEscape(self.getIsmCertificate()) + "'"
            self.module.debug("exec_command = " + exec_command)
            
            (rc, stdout, stderr) = self.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)
            
            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
                
            ism_login_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if ism_login_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if ism_login_result.group(2) == "201":
                    try :
                        json_data = json.loads(ism_login_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.log(traceback.format_exc())
                        self.module.fail_json(msg="Not json format data: " + ism_login_result.group(1))
                    
                    # set session id
                    self.setSessionId(json_data["IsmBody"]["Auth"])
                else:
                    self.module.log("Response Code=" + ism_login_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=ism_login_result.group(1))
                
            self.module.debug("***** ismLogin End *****")
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    # ism logout
    def ismLogout(self):
        try :
            self.module.debug("***** ismLogout Start *****")

            if self.getSessionId() == "":
                return

            # get rest url
            rest_url = self.getRestUrl(IsmCommon.LOGOUT_REST_URL)
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + self.getSessionId() + "' "
            
            # execute rest
            exec_command = IsmCommon.COMMAND + rest_url + IsmCommon.HEADER + add_head + IsmCommon.HTTP_RESPONSE_CODE + IsmCommon.CERTIFICATE + "'" + self.singleEscape(self.getIsmCertificate()) + "'"
            self.module.debug("exec_command = " + exec_command)
            
            (rc, stdout, stderr) = self.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)
            
            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
                
            ism_logout_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if ism_logout_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if ism_logout_result.group(2) != "201":
                    self.module.log("Response Code=" + ism_logout_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=ism_logout_result.group(1))
                
            self.module.debug("***** ismLogout End *****")
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())

    # get node OS
    def getNodeOS(self):
        try :
            self.module.debug("***** getNodeOS Start *****")
            
            # get rest url
            rest_url = self.getRestUrl(IsmCommon.GET_NODE_OS_REST_URL)
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + self.getSessionId() + "' "
            
            # execute rest
            exec_command = IsmCommon.COMMAND + rest_url + IsmCommon.HEADER + add_head + IsmCommon.GET + IsmCommon.HTTP_RESPONSE_CODE + IsmCommon.CERTIFICATE + "'" + self.singleEscape(self.getIsmCertificate()) + "'"
            self.module.debug("exec_command = " + exec_command)
            
            (rc, stdout, stderr) = self.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)
            
            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
                
            get_node_os_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if get_node_os_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if get_node_os_result.group(2) == "200":
                    try :
                        json_data = json.loads(get_node_os_result.group(1))
                    except Exception as e:
                        self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.log(traceback.format_exc())
                        self.module.fail_json(msg="REST result is fault: " + stderr)
                    
                    for list in json_data["IsmBody"]["Hosts"]:
                        if (list["OsIpAddress"] == self.module.params['hostname']):
                            self.setNodeId(list["NodeId"])
                            break
                else:
                    self.module.log("Response Code=" + get_node_os_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=get_node_os_result.group(1))
                
            self.module.debug("***** getNodeOS End *****")
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    # get node Hard
    def getNodeHard(self):
        try :
            self.module.debug("***** getNodeHard Start *****")
            
            # get rest url
            rest_url = self.getRestUrl(IsmCommon.NODE_LIST_REST_URL, "?ipaddress=" + self.module.params['hostname'])
            
            # adding a response header
            add_head = " -H 'X-Ism-Authorization: " + self.getSessionId() + "' "
            
            # execute rest
            exec_command = IsmCommon.COMMAND + rest_url + IsmCommon.HEADER + add_head + IsmCommon.GET + IsmCommon.HTTP_RESPONSE_CODE + IsmCommon.CERTIFICATE + "'" + self.singleEscape(self.getIsmCertificate()) + "'"
            self.module.debug("exec_command = " + exec_command)
            
            (rc, stdout, stderr) = self.run_command_unicode(exec_command)
            self.module.debug("rc = " + str(rc))
            self.module.debug("stdout = " + stdout)
            
            if str(rc) != "0":
                self.module.log("curl communication error: stdout=" + stdout + ". stderr=" + stderr + ". exec_command=" + exec_command)
                self.module.fail_json(msg="curl communication error: " + stderr)
                
            get_node_hard_result = re.search(r'(.+)ISM_HTTP_RESPONSE_CODE=(\d+)', stdout.replace('\n', ''))
            
            if get_node_hard_result is None:
                self.module.log("REST result is fault: stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                self.module.fail_json(msg="REST result is fault: " + stderr)
            else:
                if get_node_hard_result.group(2) == "200":
                    try :
                        json_data = json.loads(get_node_hard_result.group(1))
                    except Exception as e:
                        self.module.log("Not json format data: e=" + str(e) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                        self.module.log(traceback.format_exc())
                        self.module.fail_json(msg="Not json format data: " + get_node_hard_result.group(1))
                    if json_data["IsmBody"]["Nodes"]:
                        self.setNodeId(json_data["IsmBody"]["Nodes"][0]["NodeId"])
                else:
                    self.module.log("Response Code=" + get_node_hard_result.group(2) + ", stdout=" + stdout + ", stderr=" + stderr + ", exec_command=" + exec_command)
                    self.module.fail_json(msg=get_node_hard_result.group(1))
                
            self.module.debug("***** getNodeHard End *****")
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    # License Check
    def licenseCheck(self, license_check = True, usable_essential = False):
        try :
            self.module.debug("***** License Check Start *****")
            
            if license_check == False:
                return
            
            # get rest url
            rest_url = self.getRestUrl(IsmCommon.SYSTEM_URL , "licenses/")
            
            license_data = self.execRest(rest_url, IsmCommon.GET, IsmCommon.RESPONSE_CODE_200)
            
            if "OperationMode" in license_data["IsmBody"].keys():

                # store OperationMode
                self.setOperationMode(license_data["IsmBody"]["OperationMode"])

                # Version of ISM "2.4.0.b" after , Essential mode check
                if license_data["IsmBody"]["OperationMode"] != self.OPE_MODE_ESSENTIAL:
                    # OperationMode is not Essential (=Advanced)
                    return
                    
                elif usable_essential == True:
                    # OperationMode is Essential and usable_essential is True 
                    return
                    
                # OperationMode is Essential and usable_essential is False 
                self.module.log("This module is not supported on Essential mode.")
                self.module.fail_json(msg="This module is not supported on Essential mode.")

            else:
                # Version of ISM "2.4.0.a" before, Server license check
                for license in license_data["IsmBody"]["Licenses"]:
                    if (license["Type"] == "Server"):
                        # Server license found
                        return
                
                # Server license not found
                self.module.log("The server license of FUJITSU Software Infrastructure Manager is necessary to execute this module.")
                self.module.fail_json(msg="The server license of FUJITSU Software Infrastructure Manager is necessary to execute this module.")
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))

        finally:
            self.module.debug("***** License Check End *****")

    """
    @Description Function get node information with self.getNodeId()
    @return      dict node information from node list
    """
    def getNodeInfo(self):
        node_id = self.getNodeId()
        
        try :
            self.module.debug("***** getNodeInfo Start *****")

            # Get REST URL
            rest_url = self.getRestUrl(self.NODES_REST_URL, node_id)
            
            # REST API execution
            node_info = self.execRest(rest_url, self.GET, self.RESPONSE_CODE_200)
            
            return node_info
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))

        finally:
            self.module.debug("***** getNodeInfo End *****")

    """
    @Description Function to check node type and model of node are 
                          supported on Essential mode
                          if not specified arguments, note_type and nome_model are
                          collected in this method and checked
    @param       string node_type
    @param       string node_model
    @error       when node type and model are not supported on Essential mode
    """
    def checkNodeSupportedOnEssential(self, node_type = None, node_model = None):
        self.module.debug("***** checkNodeSupportedOnEssential Start *****")
        
        if not self.isEssentialMode():
            # not Essential mode, do nothing
            return
        
        if not node_type and not node_model:
            node_info = self.getNodeInfo()
            node_type = node_info["IsmBody"]["Node"]["Type"]
            node_model = node_info["IsmBody"]["Node"]["Model"]
        
        self.checkNodeSupportedOnEssentialImpl(node_type, node_model)

        self.module.debug("***** checkNodeSupportedOnEssential End *****")
    
    """
    @Description Function to implement of check type and model of node
                 are supported on Essential mode
    @param       string node_type
    @param       string node_model
    @error       when node type and model are not supported on Essential mode
    """
    def checkNodeSupportedOnEssentialImpl(self, node_type, node_model):

        self.module.debug("***** checkNodeSupportedOnEssentialImpl Start *****")

        not_supported_models = self.getEssentialNotSupportedModelTable()

        for not_supported_def in not_supported_models:
            if not_supported_def["Type"] == node_type and \
               not_supported_def["Model"] == node_model:
                
                # not supported on Essential
                # ex. The node type and model are not supported on Essential mode. Node type: server, model: HPE ProLiant DL series
                msg = self.MSG_NOT_SUPPORTED_TYPE_MODE_ESSENTIAL.format(node_type, node_model)
                
                self.errorMessage(msg)

        self.module.debug("***** checkNodeSupportedOnEssentialImpl End *****")

    """
    @Description Function to filter out not supported values of inventory on Essential mode
    @param       dict inventory info of node
    """
    def filterEssentialModeForInventory(self, result_node):
        if not self.isEssentialMode():
            # not Essential mode, do nothing
            return
        
        self.module.debug("***** filterEssentialModeForInventory Start *****")
        
        node_info = result_node['IsmBody']['Node']
        
        for not_supported_key in self.ESSENTIAL_NOT_SUPPORTED_KEYS_INVENTORY:
            if not_supported_key in node_info:
                node_info.pop(not_supported_key)

        self.module.debug("***** filterEssentialModeForInventory End *****")

    """
    @Description Function to filter out not supported values of
                 inventory array on Essential mode
    @param       dict inventory info of node
    """
    def filterEssentialModeForInventoryArray(self, result_node):
        if not self.isEssentialMode():
            # not Essential mode, do nothing
            return

        self.module.debug("***** filterEssentialModeForInventoryArray Start *****")

        for node_info in result_node['IsmBody']['Nodes']:
            for not_supported_key in self.ESSENTIAL_NOT_SUPPORTED_KEYS_INVENTORY:
                if not_supported_key in node_info:
                    node_info.pop(not_supported_key)

        self.module.debug("***** filterEssentialModeForInventoryArray End *****")

    """
    @Description Function to check parameters supported on Essential mode
    @error       when a parameter not supported on Essential mode exists
    """
    def checkParamsSupportedOnEssentialForNodeList(self):
        if not self.isEssentialMode():
            # not Essential mode, do nothing
            return
        
        self.module.debug("***** checkParamsSupportedOnEssentialForNodeList Start *****")
        
        not_supported_params = [
                                'rack_info',
                                'mount_type'
                               ]

        # check not supported params on Essential mode is not specified
        for not_supported_param in not_supported_params:
            if self.module.params[not_supported_param]:
                # ex. not supported parameter on Essential mode: rack_info
                msg = self.MSG_NOT_SUPPORTED_PARAMETER_ESSENTIAL + not_supported_param
                self.errorMessage(msg)
        
        self.module.debug("***** checkParamsSupportedOnEssentialForNodeList End *****")
        
    """
    @Description Function to filter out not supported values of node list on Essential mode
    @param       dict node info
    """
    def filterEssentialModeForNodeList(self, result_node):
        
        if not self.isEssentialMode():
            # not Essential mode, do nothing
            return
        
        self.module.debug("***** filterEssentialModeForNodeList Start *****")
        
        node_info = result_node['IsmBody']['Node']
        
        for not_supported_key in self.ESSENTIAL_NOT_SUPPORTED_KEYS_NODELIST:
            if not_supported_key in node_info:
                node_info.pop(not_supported_key)
        
        self.module.debug("***** filterEssentialModeForNodeList End *****")

    """
    @Description Function to filter out not supported values of node list arary on Essential mode
    @param       dict node info
    """
    def filterEssentialModeForNodeListArray(self, result_node):

        if not self.isEssentialMode():
            # not Essential mode, do nothing
            return

        self.module.debug("***** filterEssentialModeForNodeListArray Start *****")

        for node_info in result_node['IsmBody']['Nodes']:
            for not_supported_key in self.ESSENTIAL_NOT_SUPPORTED_KEYS_NODELIST:
                if not_supported_key in node_info:
                    node_info.pop(not_supported_key)

        self.module.debug("***** filterEssentialModeForNodeListArray End *****")

    """
    @Description Function to get ISM version information
    @return      string ISM version. ex. "2.4.0.b (S20190305-01)"
    """
    def getIsmVersion(self):
        try :
            self.module.debug("***** getIsmVersion Start *****")

            # Get REST URL
            rest_url = self.getRestUrl(self.ISMVA_SETTINGS_URL)
            
            # REST API execution
            setting_info = self.execRest(rest_url, self.GET, self.RESPONSE_CODE_200)
            
            ism_version = setting_info["IsmBody"]["System"]["ISMVersion"]
            
            self.module.debug("ism_version = " + str(ism_version))
            
            return ism_version
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))

        finally:
            self.module.debug("***** getIsmVersion End *****")

    """
    @Description Function to get model table of not supported on Essential mode
    @return      dict model table of not supported on Essential mode
    """
    def getEssentialNotSupportedModelTable(self):
        self.module.debug("***** getEssentialNotSupportedModelTable Start *****")

        # default (2.4.0.b)
        not_supported_models = IsmEssentialNotSupportedModel.ISM_240B

        ism_version = self.getIsmVersion()
        
        #########################################################################
        # !!! NOTE !!!                                                          #
        # When "not supported models" are changed in the future version of ISM, #
        # implement codes here to select a definition of "not supported models" #
        # corresponding to ISM version.                                         #
        #########################################################################

        if re.match(r'^2\.4\..* ', ism_version):
            # 2.4.xxx
            self.module.debug("essential not supported model 2.4.0.b selected")
            not_supported_models = IsmEssentialNotSupportedModel.ISM_240B
        
        self.module.debug("***** getEssentialNotSupportedModelTable End *****")

        return not_supported_models

    # The type is 'dict' or 'list',
    # Ansible standard parameter check can not be used.
    def choiceCheck(self, value, choice_list , key_name):
        self.module.debug("***** choiceCheck Start *****")
        
        if value not in choice_list:
            msg = ','.join(choice_list) + ','
            self.errorMessage(IsmCommon.MSG_VALUE_OF + key_name + IsmCommon.MSG_MUST_BE_ONE_OF + msg + IsmCommon.MSG_GOT + str(value))
            
        self.module.debug("***** choiceCheck End *****")
    
    # Error message
    def errorMessage(self, message):
        self.module.log(message)
        self.module.fail_json(msg= message )

    # The type is 'dict' or 'list',
    # Ansible standard parameter name check can not be used.
    def checkKeyName(self, param, key_name_list):
        self.module.debug("***** checkKeyName Start *****")
        for key in param.keys():
            if key not in key_name_list:
                self.errorMessage(IsmCommon.MSG_NOT_SUPPORT_PARAMETER + str(key))
        self.module.debug("***** checkKeyName End *****")

    """
    @Description check library version. (support only digit version)
    @param actual actual version string ex: "4.8.0"
    @param expected expected version string ex: "4.7.0"
    @return True: success, False: failed
    """
    def checkLibraryVersion(self, actual, expected):
        if StrictVersion(actual) < StrictVersion(expected):
            return False
        return True

    def decryptIsmPassword(self, password, ism_ip):
        # hostname to ip address
        ism_ip = self.convertHostnameToIP(ism_ip)

        exec_command = self.OPENSSL_DEC + ["pass:" + ism_ip]
        (rc, dec_pass, stderr) = self.run_command_unicode(exec_command, data=password)
        if rc != 0:
            self.module.fail_json(msg="invalid ISM password")
        return dec_pass

    def convertHostnameToIP(self, hostname):
        match = re.match(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', hostname)
        if match is None:
            # FQDN
            try:
                ip = socket.gethostbyname(hostname)
                self.module.debug("Host name is converted to IP address: " + hostname)
                return ip
            except Exception as e:
                self.module.log("ip transformation error: Hostname=" + hostname + ", e=" + str(e))
                self.module.log(traceback.format_exc())
                self.module.fail_json(
                    msg="Host name could not be converted to IP address: " + hostname)
        else:
            # IP
            return hostname

    def mergeDicts(self, dict1, dict2):
        # Recursively merges dict2 into dict1
        if not isinstance(dict1, dict) or not isinstance(dict2, dict):
            return dict2
        for k in dict2:
            if k in dict1:
                dict1[k] = self.mergeDicts(dict1[k], dict2[k])
            else:
                dict1[k] = dict2[k]
        return dict1

#   ***** common function *****
