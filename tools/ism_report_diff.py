#!/usr/bin/python
# coding: UTF-8

#######
# Copyright FUJITSU LIMITED 2019
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

import sys
import json
import copy

STATUS = ["Error", "Warning", "Unknown", "Updating", "Normal"]
ALARM_STATUS = ["Error", "Warning", "Info", "Normal"]
INDENT = "    "


def parser():
    try:
        usage = 'Usage: ism_report_diff.py <FILE1> [<FILE2>]'
        arguments = sys.argv
        if not (1 < len(arguments) < 4):
            raise ValueError(usage)
        arguments.pop(0)
        result = arguments
        return result
    except ValueError as e:
        print("Argument is incorrect.")
        print(e)
        sys.exit(1)


def json_load(data):
    try:
        with open(data, 'r') as f:
            json_data = json.load(f)
        return json_data
    except Exception as e:
        print("File open error.")
        print(e)
        sys.exit(1)


def get_node_info(node_infos, node_inventory_infos, ism_firmware_infos, old_node_id):
    firmware_infos = []
    added_node = []
    for node_info in node_infos:
        firmware = {"Name": node_info["Name"]}
        firmware["Type"] = node_info["Type"]
        firmware["Model"] = node_info["Model"]
        firmware["IP"] = node_info["IpAddress"]
        if not node_info["NodeId"] in old_node_id:
            add_node = copy.deepcopy(firmware)
            added_node.append(add_node)
        firmware["node firmware"] = get_firmware_info(node_inventory_infos,
                                                      node_info["NodeId"])
        firmware["updatable firmware"] = get_updatable_firmware_info(ism_firmware_infos,
                                                                     node_info["NodeId"])
        firmware_infos.append(firmware)
    return firmware_infos, added_node


def get_firmware_info(node_inventory_infos, node_id):
    node_firmware_infos = []
    for node_inventory in node_inventory_infos:
        if "Firmware" not in node_inventory["VariableData"]:
            continue
        if node_inventory["NodeId"] == node_id:
            for firmware in node_inventory["VariableData"]["Firmware"]:
                firmware_info = {"Name": firmware["Name"]}
                firmware_info["Type"] = firmware["Type"]
                firmware_info["Version"] = firmware["FirmwareVersion"]
                node_firmware_infos.append(firmware_info)
    return node_firmware_infos


def get_updatable_firmware_info(firmware_infos, node_id):
    updatable_firmware_infos = []
    for firmware in firmware_infos:
        if firmware["NodeId"] == node_id:
            updatable_firmware_info = {"Name": firmware["FirmwareName"]}
            updatable_firmware_info["Type"] = firmware["FirmwareType"]
            updatable_firmware_info["Version"] = firmware["FirmwareVersion"]
            updatable_firmware_info["RepositoryName"] = firmware["RepositoryName"]
            updatable_firmware_info["OperationMode"] = firmware["OperationMode"]
            updatable_firmware_infos.append(updatable_firmware_info)
    return updatable_firmware_infos


def get_node_id(node_infos):
    ids = []
    for node_info in node_infos:
        ids.append(node_info["NodeId"])
    return ids


def get_node_diff(now_node_id, old_node_id):
    add_node = len(set(now_node_id) - set(old_node_id))
    delete_node = len(set(old_node_id) - set(now_node_id))
    diff = "+" + str(add_node) + ", " + "-" + str(delete_node)
    return diff


def output_status(status_infos, status_keys, status_name):
    print(status_name)
    for status_key in status_keys:
        print(INDENT + status_key + ": " + convert_str(status_infos[status_key]))


def output_addednode(added_infos):
    nodenumber = 0
    print("Added node:")
    for added_info in added_infos:
        nodenumber += 1
        print(INDENT + "Node " + convert_str(nodenumber) + ":")
        output_node(added_info)


def output_node(node_info):
    print(INDENT + INDENT + "Name: " + convert_str(node_info["Name"]))
    print(INDENT + INDENT + "Type: " + convert_str(node_info["Type"]))
    print(INDENT + INDENT + "Model: " + convert_str(node_info["Model"]))
    print(INDENT + INDENT + "IP: " + convert_str(node_info["IP"]))


def output_firmware(firmware_infos):
    print("Firmware:")
    nodenumber = 0
    for firmware_info in firmware_infos:
        if firmware_info["updatable firmware"] == []:
            # No updatable firmware
            continue
        nodenumber += 1
        print(INDENT + "Node " + convert_str(nodenumber) + ":")
        output_node(firmware_info)
        output_node_firmware(firmware_info["node firmware"])
        output_updatable_firmware(firmware_info["updatable firmware"])


def output_node_firmware(node_firmware_info):
    number = 0
    for node_firmware in node_firmware_info:
        number += 1
        print(INDENT + INDENT + "Firmware " + convert_str(number))
        print(INDENT + INDENT + INDENT + "Name: " + convert_str(node_firmware["Name"]))
        print(INDENT + INDENT + INDENT + "Type: " + convert_str(node_firmware["Type"]))
        print(INDENT + INDENT + INDENT + "Version: " + convert_str(node_firmware["Version"]))


def output_updatable_firmware(updatable_firmware_info):
    number = 0
    for updatable_firmware in updatable_firmware_info:
        number = number + 1
        print(INDENT + INDENT + "Updatable firmware " + convert_str(number))
        print(INDENT + INDENT + INDENT + "Name: " + convert_str(updatable_firmware["Name"]))
        print(INDENT + INDENT + INDENT + "Type: " + convert_str(updatable_firmware["Type"]))
        print(INDENT + INDENT + INDENT + "Version: " + convert_str(updatable_firmware["Version"]))
        print(INDENT + INDENT + INDENT + "RepositoryName: "
              + convert_str(updatable_firmware["RepositoryName"]))
        print(INDENT + INDENT + INDENT + "OperationMode: "
              + convert_str(updatable_firmware["OperationMode"]))


def convert_str(target):
    if target is None:
        return str(target)
    else:
        if isinstance(target, unicode):
            return target.encode('utf-8')
        else:
            return str(target)


if __name__ == '__main__':
    jsonfiles = parser()
    if len(jsonfiles) == 1:
        now_data = json_load(jsonfiles[0])
        now_node_id_list = get_node_id(now_data["ism_node_info"]["IsmBody"]["Nodes"])
        old_node_id_list = []
    else:
        now_data = json_load(jsonfiles[1])
        now_node_id_list = get_node_id(now_data["ism_node_info"]["IsmBody"]["Nodes"])
        old_data = json_load(jsonfiles[0])
        old_node_id_list = get_node_id(old_data["ism_node_info"]["IsmBody"]["Nodes"])
    analysis_data = {"Status": now_data["ism_status_count"]}
    analysis_data["Alarm status"] = now_data["ism_alarm_status_count"]
    analysis_data["Total"] = now_data["ism_node_count"]
    analysis_data["Firmware"], analysis_data["Added node"] = get_node_info(
        now_data["ism_node_info"]["IsmBody"]["Nodes"],
        now_data["ism_inventory_info"]["IsmBody"]["Nodes"],
        now_data["ism_firmware_info"]["IsmBody"]["FirmwareList"],
        old_node_id_list)
    analysis_data["Diff"] = get_node_diff(now_node_id_list, old_node_id_list)
    # Total
    print("Total: " + convert_str(analysis_data["Total"]))
    # Diff
    if len(jsonfiles) == 2:
        print("Diff: " + analysis_data["Diff"])
    # Status
    output_status(analysis_data["Status"], STATUS, "Status")
    # Alarm Status
    output_status(analysis_data["Alarm status"], ALARM_STATUS, "Alarm status")
    # Added node
    if len(jsonfiles) == 2:
        output_addednode(analysis_data["Added node"])
    # firmware
    output_firmware(analysis_data["Firmware"])
    sys.exit(0)
