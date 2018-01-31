#!/usr/bin/sh
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

set -eu
trap "" ERR

echo "Please enter IP address or FQDN:"
read ip
if [ "${ip}" = "" ]; then
    echo "IP address or FQDN is not entered"
    exit 1
fi

regex_ip='^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'
passphrase=""

# FQDN -> IP
get_ipaddr() {
     printf '%s' "$1" | python -c 'import socket,sys; print(socket.gethostbyname(sys.stdin.read()))'
}

# set passphrase
if [[ ${ip} =~ ${regex_ip} ]]; then
    passphrase=${ip}
else
    # FQDN -> IP
    passphrase=`get_ipaddr ${ip}`
fi

echo "Please enter port number:"
read portNo
if [ "${portNo}" = "" ]; then
    echo "Port number is not entered"
   exit 1
fi

echo "Please enter user name:"
read userName
if [ "${userName}" = "" ]; then
    echo "User name is not entered"
    exit 1
fi

echo "Please enter password:"
read password
if [ "${password}" = "" ]; then
    echo "Password is not entered"
    exit 1
else
    # Password encryption
    password=`echo -n "${password}" | openssl enc -aes-256-cbc -e -base64 -pass pass:"${passphrase}"`
fi

echo "Please enter full path of certificate file:"
read certificate
if [ "${certificate}" = "" ]; then
    echo "full path of certificate file is not entered"
    exit 1
fi

json_escape () {
     printf '%s' "$1" | python -c 'import json,sys; print(json.dumps(sys.stdin.read()))';
}

# Value escape
ip=`json_escape ${ip}`
portNo=`json_escape ${portNo}`
userName=`json_escape ${userName}`
password=`json_escape ${password}`
certificate=`json_escape ${certificate}`

echo \{\"ip\":${ip},\"portNo\":${portNo},\"credentials\":\{\"userName\":${userName},\"password\":${password}\},\"certificate\":${certificate}\} > ism_config.json

echo completed
exit 0
