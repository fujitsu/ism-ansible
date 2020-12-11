#!/usr/bin/python
# coding: UTF-8

#######
# Copyright FUJITSU LIMITED 2019-2020
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
module: ism_backup
short_description: Backup Infrastructure Manager.
description:
    - "Provides an interface for backup Infrastructure Manager."
version_added: "2.4"
author: "Munenori Maeda (@XXXXXXXXX)"
options:
    config:
      description:
        - Specify the full path for the described setting file
          of the connection information of Infrastructure Manager.
      required: true
    hostname:
      description:
        - Specify the host name (FQDN) for the IP address of Infrastructure Manager.
          IPv6 is not supported. Specify a host name that can be resolved by IPv4 or IPv4.
      required: true
    dest_dir:
      description:
        - "Specify the output directory for the backup file as full path.
          The backup file is named with the following format automatically.
          Format: ism<ISM version>-backup-<Date of backup>.tar.gz
          Example: ism2.5.0.030-backup-20191219041611.tar.gz"
      required: true
    timeout:
      description:
        - Specify the timeout for waiting completion of the backup as integer.
          The unit is a second. When specifying 0 or less or omitted, the time-out
          is not done.
      required: false
      default: 0
requirements:
    - "python >= 2.7"
    - "pexpect >= 4.7"
    - "ISM >= 2.2.0.c"
notes:
    - "The setting method of the setting file specified in the config parameter is in the following
      location:
      U(https://github.com/fujitsu/ism-ansible/blob/master/Readme.md)"
'''

EXAMPLES = '''
- name: Execution of ism_backup
  ism_backup:
    config: "/etc/ansible/ism-ansible/ism_config.json"
    hostname: "192.168.1.10"
    des_dir: "/tmp"
  register: ism_backup_result
- debug: var=ism_backup_result
'''

RETURN = '''
ism_backup_file:
    description: The full path of the backup file.
    returned: Always
    type: string
'''

# import
import traceback
import sys
import re
import os
from ftplib import FTP

try:
    import pexpect
    from pexpect import pxssh
    HAS_PEXPECT = True
except ImportError:
    HAS_PEXPECT = False

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ism_common import IsmCommon


class IsmBackup():
    PEXPECT_VERSION = "4.7.0"
    PEXPECT_VERSION_MSG = 'The pexpect >= 4.7.0 python module is required'
    PXSSH_DEBUG = False
    PXSSH_CONNECT_TIMEOUT = 60
    PXSSH_MSG_HEADER = "SSH connection error: {0}"
    PXSSH_OPTION = {
        "ConnectTimeout": PXSSH_CONNECT_TIMEOUT,
        "StrictHostKeyChecking": "no",
        "UserKnownHostsFile": "/dev/null"
    }

    PORT_SSH = 22

    FTP_CONNECT_TIMEOUT = 60
    FTP_MSG_CONNECT_HEADER = "FTP connection error: {0}"
    FTP_MSG_OPERATION_HEADER = "FTP operation error: {0}"

    RE_CONNECT_ERROR = re.compile(r'^could not set shell prompt')
    RE_START_BACKUP = re.compile(r'^Start backup process\? \[y/n\]: ', re.MULTILINE)
    RE_ERROR = re.compile(r'^(ERROR:\d+:.+)$', re.MULTILINE)
    RE_OUTPUT_FILE = re.compile(r'^Output file: (ism.+\.gz)', re.MULTILINE)

    FTP_DIR = "/Administrator/ftp/"

    module = AnsibleModule(
        argument_spec=dict(
            config=dict(type="str", required=True),
            hostname=dict(type="str", required=True),
            dest_dir=dict(type="str", required=True),
            timeout=dict(type="int", default=0, required=False)
        )
    )

    def __init__(self):
        self.__present()

    def __present(self):
        self.common = IsmCommon(self.module)

        # check for blank("") and None
        self.common.required_param_check(self.module.params["config"], "config")
        self.common.required_param_check(self.module.params["hostname"], "hostname")
        self.common.required_param_check(self.module.params["dest_dir"], "dest_dir")

        # check pexpect installed and its version
        if not HAS_PEXPECT:
            self.module.fail_json(msg=self.PEXPECT_VERSION_MSG)
        if not self.common.checkLibraryVersion(pexpect.__version__, "4.7.0"):
            self.module.fail_json(msg=self.PEXPECT_VERSION_MSG)

        try:
            self.common.preProcess(self.module.params,
                                   usableEssential=True,
                                   NodeCheck=False,
                                   paramListNotBlank=["timeout"],  # don't convert None to blank("")
                                   doIsmLogin=False)
            # convert to unicode
            self.module.params['config'] = self.common.covert_unicode(
                self.module.params['config'])
            self.module.params['hostname'] = self.common.covert_unicode(
                self.module.params['hostname'])
            self.module.params['dest_dir'] = self.common.covert_unicode(
                self.module.params['dest_dir'])

            self.dest_dir = self.module.params["dest_dir"]

            self.timeout = self.module.params["timeout"]
            if not(self.timeout) or self.timeout <= 0:  # less than or equal 0
                self.timeout = None  # no timeout

            config_json = self.common.ism_config_json

            self.ism_ip = config_json["ip"]
            self.ism_user_name = config_json["credentials"]["userName"]
            self.ism_password = config_json["credentials"]["password"]

            self.ism_password = self.common.decryptIsmPassword(self.ism_password, self.ism_ip)

            filename = self.__backup()
            dest_file = os.path.join(self.dest_dir, filename)

            self.__download(dest_file, filename)

            self.module.exit_json(changed=True,
                                  ism_backup_file=dest_file)

        except Exception as e:
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))

    def __backup(self):
        ssh = None

        try:
            ssh = pxssh.pxssh(options=self.PXSSH_OPTION)

            if self.PXSSH_DEBUG:
                # pxssh stdout for debug
                ssh.logfile = sys.stdout

            try:
                ssh.login(self.ism_ip,
                          username=self.ism_user_name,
                          password=self.ism_password,
                          login_timeout=self.PXSSH_CONNECT_TIMEOUT,
                          port=self.PORT_SSH)
            except pexpect.ExceptionPexpect as e:
                msg = str(e)
                if self.RE_CONNECT_ERROR.match(msg):
                    # connection error
                    msg = self.PXSSH_MSG_HEADER.format("Failed to connect host")
                else:
                    msg = self.PXSSH_MSG_HEADER.format(msg)
                self.module.log(msg)
                self.module.log(traceback.format_exc())
                self.module.fail_json(msg=msg)

            ssh.sendline("ismadm system backup")

            # waiting backup size estimation
            index = ssh.expect([self.RE_START_BACKUP, self.RE_ERROR, ssh.PROMPT],
                               timeout=self.timeout)

            if index == 1:
                # error message
                msg = ssh.match.group(1).rstrip()
                self.module.log(msg)
                self.module.fail_json(msg=msg)
            elif index == 2:
                # not ISM server
                msg = "backup failed: not ISM server"
                self.module.log(msg)
                self.module.log("output={0}".format(ssh.before))
                self.module.fail_json(msg=msg)

            # start backup
            ssh.sendline("y")

            # waiting backup complete
            ssh.expect(ssh.PROMPT, timeout=self.timeout)

            output = ssh.before

            match = self.RE_ERROR.search(output)
            if match:
                # error message
                msg = match.group(1).rstrip()
                self.module.log(msg)
                self.module.fail_json(msg=msg)

            match = self.RE_OUTPUT_FILE.search(output)
            if not match:
                # Output file not found
                msg = "missing backup file info"
                self.module.log(msg)
                self.module.log("output={0}".format(output))
                self.module.fail_json(msg=msg)

            filename = match.group(1)

            return filename

        except pexpect.TIMEOUT:
            msg = "waiting for backup timeout: {0}s".format(self.timeout)
            self.module.log(msg)
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=msg)
        finally:
            # close
            if ssh:
                try:
                    ssh.close()
                except Exception:
                    # ignore error
                    self.module.log(traceback.format_exc())

    def __download(self, dest_file, ftp_file):
        ftp = None
        file_deleted = False
        try:
            try:
                ftp = FTP(self.ism_ip, self.ism_user_name, self.ism_password,
                          self.FTP_CONNECT_TIMEOUT)
            except Exception as e:
                msg = self.FTP_MSG_CONNECT_HEADER.format(e)
                self.module.log(msg)
                self.module.log(traceback.format_exc())
                self.module.fail_json(msg=msg)

            with open(dest_file, 'wb') as f:
                try:
                    ftp.retrbinary('RETR ' + self.FTP_DIR + ftp_file, f.write)
                    ftp.delete(self.FTP_DIR + ftp_file)
                    file_deleted = True
                except Exception as e:
                    msg = self.FTP_MSG_OPERATION_HEADER.format(e)
                    self.module.log(msg)
                    self.module.log(traceback.format_exc())
                    self.module.fail_json(msg=msg)

        except Exception as e:
            self.module.log(traceback.format_exc())
            self.module.fail_json(msg=str(e))
        finally:
            # FTP logout
            if ftp:
                try:
                    if not file_deleted:
                        # delete file
                        ftp.delete(self.FTP_DIR + ftp_file)
                    ftp.quit()
                except Exception:
                    # ignore error
                    self.module.log(traceback.format_exc())


if __name__ == '__main__':
    IsmBackup()
