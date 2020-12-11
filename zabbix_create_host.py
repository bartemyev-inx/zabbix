#!/usr/bin/env python

from pyzabbix import ZabbixAPI, ZabbixAPIException
import sys, getpass
try:
    password = getpass.getpass()
except Exception as error:
    print('ERROR', error)

host_group_id = "56"
template_id = "15590"
host_name = "pdu1a.sje.303net.pvt"
zabbix_server = "http://zabbix.303net.pvt/zabbix"
zapi = ZabbixAPI(zabbix_server)
zapi.login("bartemyev", password)
print("Connected to Zabbix API Version %s" % zapi.api_version())
print ("")
print zapi.host.create({"host": host_name, "groups":host_group_id, "templates":template_id, "interfaces": [{"main": "1","type": "2", "useip": "0", "dns": host_name, "port": "161"}]})
