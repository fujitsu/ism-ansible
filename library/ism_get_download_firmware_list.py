#!/usr/bin/python
#coding: UTF-8

#######
# Copyleft FUJITSU LIMITED 2018
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
module: ism_get_download_firmware_list
short_description: Get the download firmware infomation of Infrastructure Manager.
description:
    - "Provides an interface for get the download firmware infomation status of Infrastructure Manager."
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
- name: Getting Download Firmware List
  ism_get_download_firmware_list_status:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.22"
    filter:False
  register: ism_get_download_firmware_list_result
- debug: var=ism_get_download_firmware_list_result
'''

RETURN = '''
ism_get_download_firmware_list_status:
    description: The execution result of download firmware information acquisition is returned.
    returned: Always
    type: dict
'''

# import
import traceback
import copy
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon
from ansible.module_utils.ism_user_settings import IsmUserSettingsValue

class IsmGetDownloadFirmwareInfo():
    
    # Receiving args
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(required=True),
            hostname=dict(required=True),
            filter=dict(required=False, choices=['True','False'], default="False"),
        )
    )
    
    def __init__(self):
       self.__present()
       
    def __present(self):
        try :
            self.module.log("argument_spec with config=" + str(self.module.params['config']) + " hostname=" + str(self.module.params['hostname']) + " filter=" + str(self.module.params['filter']))
            
            # Instance of common class
            common = IsmCommon(self.module)

            # Pre-process
            common.preProcess(self.module.params,NodeCheck = False)

            # Get Download Firmware Info execution
            result = self.getDownloadFirmwareInfo(common)

            # ISM logout
            common.ismLogout()
            
            # Return json
            changed_result = False
            self.module.log("ism_get_download_firmware_list successful completion")
            self.module.exit_json(changed=changed_result, ism_get_download_firmware_list=result)
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
            
    """
    @Description Function to output Download Firmware Info
    @param       class common
    @return      dict json_data
    """
    def getDownloadFirmwareInfo(self, common):
        try :
            self.module.debug("***** getDownloadFirmwareInfo Start *****")
            
            # Get REST URL
            rest_url = common.getRestUrl(common.FIRMWARE_URL, "ftsfirmwarelist")
            
            # REST API execution
            json_data = common.execRest(rest_url, common.GET, common.RESPONSE_CODE_200)
            
            # Acquire parameters
            dict_param = dict()
            dict_param['filter'] = self.module.params['filter']
            
            # When the parameter is "True"
            if dict_param['filter'] is "True":
                json_data = self.getNewDownloadFirmwareInfo(common, json_data)
                
            self.module.log("getDownloadFirmwareInfo success")
            self.module.debug("***** getDownloadFirmwareInfo End *****")
            
            return json_data
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
        
    """
    @Description Function to Download Firmware List
    @param       class common
    @return      dict json_data
    """
    def getNewDownloadFirmwareInfo(self, common, new_fw_data):
        try :
            self.module.debug("***** getNewDownloadFirmwareInfo Start *****")

            # Get REST URL
            rest_url = common.getRestUrl(common.FIRMWARE_INVENTORY_REST_URL)

            # REST API execution
            existing_fw_version = common.execRest(rest_url, common.GET, common.RESPONSE_CODE_200)
            
            # new_fw_data copy
            json_copy_data = []
            json_copy_data = copy.deepcopy(new_fw_data)
            
            # new_fw_data["IsmBody"]["FirmwareList"] delete
            del json_copy_data["IsmBody"]["FirmwareList"]
            
            # new_fw_data["IsmBody"]["FirmwareList"] 
            json_copy_data["IsmBody"]["FirmwareList"] = []
            
            for node_level in existing_fw_version["IsmBody"]["Nodes"]:
                for variabledata_level in node_level["VariableData"]:
                    if variabledata_level != "Firmware":
                        continue
                    for firmware_level in node_level["VariableData"]["Firmware"]:
                        if not((firmware_level["Type"] == "iRMC") or (firmware_level["Type"] == "BIOS")) or (firmware_level["Name"] is None) or (firmware_level["FirmwareVersion"] is None) :
                            continue
                        for firmwarelist_level in new_fw_data["IsmBody"]["FirmwareList"]:
                            # Version comparison processing
                            if not(firmwarelist_level["FirmwareName"] ==  firmware_level["Name"]) or (firmwarelist_level["FirmwareName"] == ""):
                                continue
                            self.module.debug("*****  Version comparison processing Start *****")
                            self.module.debug(" Left_info  < Type: " + str(firmwarelist_level["FirmwareType"]) + " Name: " + str(firmwarelist_level["FirmwareName"]) + " Version: " + str(firmwarelist_level["FirmwareVersion"]) + ">")
                            self.module.debug(" Right_info < Type: " + str(firmware_level["Type"]) + " Name: " + str(firmware_level["Name"]) + " Version: " +  str(firmware_level["FirmwareVersion"]) + ">")
                            
                            # "." split
                            left_version = firmwarelist_level["FirmwareVersion"].split(".")
                            right_version = firmware_level["FirmwareVersion"].split(".")
                            
                            #type
                            type = firmware_level["Type"]
                            
                            # Len Comparison
                            len = self.getLenComparison(left_version, right_version)
                            
                            for i in range(len):
                                
                                # Version Comparison
                                result = self.versionComparison(left_version,right_version,type,i)
                                
                                if result  == "SKIP":
                                    continue
                                elif result == "OK":
                                    count = 0
                                    
                                    # Check the latest version
                                    for copy_j in json_copy_data["IsmBody"]["FirmwareList"]:
                                        if (copy_j["FirmwareName"] == firmwarelist_level["FirmwareName"]) :
                                            
                                            # "." split
                                            check_version = copy_j["FirmwareVersion"].split(".")
                                            check_left_version = firmware_level["FirmwareVersion"].split(".")
                                            
                                            # Len Comparison
                                            check_len = self.getLenComparison(check_left_version, check_version)
                                            
                                            for y in range(check_len):
                                            
                                                # Version Comparison
                                                copy_result = self.versionComparison(check_left_version,check_version,type,y)

                                                if copy_result == "NO":
                                                    # json_copy_data pop
                                                    json_copy_data["IsmBody"]["FirmwareList"].pop(count)
                                                    break
                                        count +=1
                                    
                                    self.module.debug("New Download Information :" + str(firmwarelist_level))
                                    self.module.debug("< Type: " + str(firmwarelist_level["FirmwareType"]) + " Name: " + str(firmwarelist_level["FirmwareName"]) + " Version: " + str(firmwarelist_level["FirmwareVersion"]) + ">")
                                    
                                    # Add firmwarelist_level to json_copy_data append
                                    json_copy_data["IsmBody"]["FirmwareList"].append(firmwarelist_level)
                                    break
                                elif result == "NO":
                                    break
                            self.module.debug("*****  Version comparison processing End *****")
            
            # json_copy_data copy
            new_fw_data = copy.deepcopy(json_copy_data)
            
            self.module.log("getNewDownloadFirmwareInfo success")
            self.module.debug("***** getNewDownloadFirmwareInfo End *****")
            return new_fw_data
            
        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
    

    """
    @Description Version Comparison
    @param       Array left_version, right_version, type, i
    @return      str result
    """
    def versionComparison(self,left_version,right_version,type,i):

        result = ""
        if type == "iRMC" and i == 1:
            
            #Charno Comparison
            result = self.charnoComparison(left_version[i], right_version[i])
        elif type == "BIOS" and i == 0:
            right_version[i]  = str(right_version[i])[1:]
            left_version[i] = str(left_version[i])[1:]

        if result == "":
            result = self.noComparison(left_version[i], right_version[i])

        return result

    
    """
    @Description Compare the lengths of the sequences
    @param       Array left_version, right_version
    @return      int len
    """
    def getLenComparison(self, left_version, right_version):

        left_len = len(left_version)
        right_len = len(right_version)
        
        if (left_len > right_len):
            return right_len
        elif (left_len < right_len):
            return left_len
        else:
            return left_len

    """
    @Description Number Version Comparison
    @param       str left, right
    @return      str "OK" or "NO" or "SKIP"
    """
    def noComparison(self, left, right):
    
        left_no = int(left)
        right_no = int(right)
        
        self.module.debug("left_Comparison : " + str(left_no))
        self.module.debug("right_Comparison: " + str(right_no))
        if (left_no > right_no):
            self.module.debug("return OK")
            return "OK"
        elif (left_no < right_no):
            self.module.debug("return NO")
            return "NO"
        else:
            self.module.debug("return SKIP")
            return "SKIP"
            
    """
    @Description Character Version Comparison
    @param       str left, right
    @return      str "OK" or "NO" or "SKIP"
    """
    def charnoComparison(self, left, right):

        left_array = self.getArrayProcessing(left)
        right_array = self.getArrayProcessing(right)
        
        len = self.getLenComparison(left_array, right_array)
        for i in range(len):
            result = self.noComparison(left_array[i],right_array[i])
            
            if result == "OK":
                self.module.debug("return OK")
                return "OK"
            elif result == "NO":
                self.module.debug("return NO")
                return "NO"
        self.module.debug("return SKIP")
        return "SKIP"

    """
    @Description Array Processing
    @param       str character
    @return      array array
    """
    def getArrayProcessing(self,character):
        array = ["",""]
        index = 0
        
        for chara in character:
            if chara.isdigit() == True:
                 array[index] += str(chara)
            else:
                index = 1
        
        for index,item in enumerate(array):
            if item == "":
                array.pop(index)
        
        self.module.debug("return " + str(array))
        return array
        
IsmGetDownloadFirmwareInfo()
