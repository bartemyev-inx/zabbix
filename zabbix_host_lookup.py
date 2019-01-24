"""
Looks up a host based on its name, and then adds an item to it
"""

from pyzabbix import ZabbixAPI, ZabbixAPIException
import sys

# The hostname at which the Zabbix web interface is available
#ZABBIX_SERVER = 'http://zabbix.303net.pvt/zabbix'

#zapi = ZabbixAPI(ZABBIX_SERVER)
zapi = ZabbixAPI("http://zabbix.303net.pvt/zabbix")
zapi.login("bartemyev", "{M@tr1x7997}")
print("Connected to Zabbix API Version %s" % zapi.api_version())

# Login to the Zabbix API
#zapi.login("bartemyev", "{M@tr1x7997}")

host_name = 'pdu3a.dal.303net.pvt'

hosts = zapi.host.get(filter={"host": host_name}, selectInterfaces=["type","main","useip","dns","port"], selectGroup=["groupid"],selectTemplates=["templateid"])
if hosts:
    host_id = hosts[0]["hostid"]
    print "unformatted host ID %s" % host_id
    print("Found host id {0}".format(host_id))
    print hosts
else:
    print("Host not found")
group_name = "PDUs"
groups = zapi.hostgroup.get(filter={"name": group_name})#, selectInterfaces=["interfaceid"])
if groups:
    group_id = groups[0]["groupid"]
    print "Hostgroup ID for",  group_name, group_id
else:
    print("group not found")
template_name = "Template SNMP APC PDU"
templates = zapi.template.get(filter={"host": template_name})
if templates:
    template_id = templates[0]["templateid"]
    print "Temlate ID for", template_name, template_id
else:
    print ("template not found")
