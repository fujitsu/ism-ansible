#!/usr/bin/python
# coding: UTF-8

#######
# Copyright FUJITSU LIMITED 2020
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
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ism_copy_profile
short_description: Copy profile of Infrastructure Manager.
description:
    - "Provides an interface for copy profile of Infrastructure Manager."
version_added: "2.4"
author: "Munenori Maeda (@XXXXXXXXX)"
options:
    config:
      description:
        - Specifies the full path for the described setting file of the connection
          information of Infrastructure Manager.
      required: true
    ism_source_profile_name:
      description: Specifies the name of the source profile.
      required: true
    ism_profile_name:
      description: Specifies the name of the destination profile.
      required: true
    ism_profile_data:
      description:
        - Specifies the value to change when copying.
          If omitted, no changes are made.
      required: false
      type: dict
requirements:
    - Ansible >= 2.4.0.0
    - python >= 2.6
    - ISM >= 2.2.0
notes:
    - "The setting method of the setting file specified in the config
       parameter is in the following location:
       U(https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)"
'''
EXAMPLES = '''
- name: Copy Profile
  hosts: servers
  gather_facts: no
  connection: local
  vars:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    ism_source_profile_name: "SourceProfile"
    ism_profile_data:
      Server-RX:
        OSInstallation:
          Windows:
            OsIndividualConfig:
              BasicSettings:
                ComputerName: "{{ ism_computer_name }}"
              NetworkInterface:
                IPv4:
                  Address: "{{ ism_os_ip_address }}"
  tasks:
  - name: Copying Profile
    ism_copy_profile:
      config: "{{ config }}"
      ism_source_profile_name: "{{ ism_source_profile_name }}"
      ism_profile_name: "{{ ism_profile_name }}"
      ism_profile_data: "{{ ism_profile_data }}"
    register: ism_copy_profile_result
  - debug: var=ism_copy_profile_result
'''

RETURN = '''
ism_copy_profile:
    description: The execution result of profile copying is returned.
    returned: Always
    type: string
'''

# import
import json
import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon


class IsmCopyProfile():

    CRYPTPASS = "ansible"
    # Receiving args
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(type="str", required=True),
            ism_source_profile_name=dict(type="str", required=True),
            ism_profile_name=dict(typer="str", required=True),
            ism_profile_data=dict(type="dict", required=False)
        )
    )

    def __init__(self):
        self.__present()

    def __present(self):
        # Instance of common class
        self.common = IsmCommon(self.module)

        # check for blank("") and None
        self.common.required_param_check(self.module.params["config"], "config")
        self.common.required_param_check(self.module.params["ism_source_profile_name"],
                                         "ism_source_profile_name")
        self.common.required_param_check(self.module.params["ism_profile_name"],
                                         "ism_profile_name")

        try:

            # Pre-process
            self.common.preProcess(self.module.params, NodeCheck=False, noHost=True)
            self.module.params['config'] = self.common.covert_unicode(self.module.params['config'])
            self.module.params['ism_source_profile_name'] = self.common.covert_unicode(
                self.module.params['ism_source_profile_name'])
            self.module.params['ism_profile_name'] = self.common.covert_unicode(
                self.module.params['ism_profile_name'])

            if self.module.params['ism_profile_data']:
                self.common.covertUnicodeHashDict(self.module.params['ism_profile_data'])

            # Check profile
            check_profile_result = \
                self.__checkProfile(self.module.params['ism_source_profile_name'],
                                    self.module.params['ism_profile_name'])

            # Get profile
            get_profile_result = self.__getProfile(check_profile_result)

            # Copy profile
            self.__copyProfile(get_profile_result)

            self.module.exit_json(changed=True,
                                  ism_copy_profile="Success")

        except Exception as e:
            self.module.log(str(e))
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
        finally:
            self.common.ismLogout()

    def __checkProfile(self, source, dest):
        profile_id = None

        # source and dest profile name are same
        if source == dest:
            msg = "ism_source_profile_name and ism_profile_name have duplicate values: {0}".\
                  format(source)
            self.module.log(msg)
            self.module.fail_json(msg=msg)

        # Get REST URL
        rest_url = self.common.getRestUrl(self.common.PROFILE_LIST_REST_URL)

        # REST API execution
        json_data = self.common.execRest(rest_url, self.common.GET, self.common.RESPONSE_CODE_200)

        for profile in json_data['IsmBody']['ProfileList']:

            if profile['ProfileName'] == dest:
                # already copied
                self.module.exit_json(changed=False, ism_copy_profile="Success")

            elif profile['ProfileName'] == source:
                profile_id = profile['ProfileId']

        # Profile not found
        if not profile_id:
            msg = "profile not found: {0}".format(source)
            self.module.log(msg)
            self.module.fail_json(msg=msg)

        return profile_id

    def __getProfile(self, profile_id):
        # Get REST URL
        rest_url = self.common.getRestUrl(self.common.PROFILE_LIST_REST_URL,
                                          "/" + profile_id + "?passwordkey=" + self.CRYPTPASS)
        # REST API execution
        json_data = self.common.execRest(rest_url, self.common.GET, self.common.RESPONSE_CODE_200)

        source_info = json_data['IsmBody']

        # delete create profile REST-API not supported keys
        not_supported_keys = ['ProfileId',
                              'PathName',
                              'AssignedNodeId',
                              'Status',
                              'InternalStatus',
                              'VerifyStatus',
                              'HistoryList',
                              'VerifyList',
                              'TimeStampInfo']

        for not_supported_key in not_supported_keys:
            if not_supported_key in source_info:
                del source_info[not_supported_key]

        # add information
        if self.module.params['ism_profile_data']:
            dict_data = source_info['ProfileData']
            dict_set = dict(self.module.params['ism_profile_data'])
            source_info['ProfileData'] = self.common.mergeDicts(dict_data, dict_set)

        source_info['ProfileName'] = self.module.params['ism_profile_name']
        source_info['OneTimePasswordKey'] = self.CRYPTPASS

        all_data = {"IsmBody": source_info}
        return all_data

    def __copyProfile(self, body):
        # Get REST URL
        rest_url = self.common.getRestUrl(self.common.PROFILE_LIST_REST_URL)

        # REST API execution
        param_str = "\'" + self.common.singleEscape(json.dumps(body)) + "\'"
        self.common.execRest(rest_url, self.common.POST, self.common.RESPONSE_CODE_201, param_str)


if __name__ == '__main__':
    IsmCopyProfile()