#!/usr/bin/env python
#coding:utf8

'''
Created on 07/31/2018 by Boris Artemyev
Credit https://github.com/CNSRE/Zabbix-PyZabbix/blob/master/zabbix_host_add.py
'''

import optparse
import sys
import traceback
from getpass import getpass
from pyzabbix import ZabbixAPI

def get_options():
    usage = """usage: %prog [options]
    \t 
    \t %prog [-s|--server http://zabbix_server/zabbix_url] [-u|--username username] [-p|--password password]
    \t [-H|--hostname fqdn_hostname] [-g|--groups list of groups, separeted by a comma] 
    \t [-t|--templates list of templates, separated by a comma]
    \t [-i|--ip IP.v4.Address.Optional] [-n|--name name if different from %hostname] [--proxy default empty]
    \t [--status default 0 monitored]
"""
    OptionParser = optparse.OptionParser
    parser = OptionParser(usage)

    parser.add_option("-s","--server",action="store",type="string",\
        dest="server",help="(REQUIRED)Zabbix Server URL.")
    parser.add_option("-u", "--username", action="store", type="string",\
        dest="username",help="(REQUIRED)Username (Will prompt if not given).")
    parser.add_option("-p", "--password", action="store", type="string",\
        dest="password",help="(REQUIRED)Password (Will prompt if not given).")
    parser.add_option("-H","--hostname",action="store",type="string",\
        dest="hostname",help="(REQUIRED)hostname for hosts.")
    parser.add_option("-g","--groups",action="store",type="string",\
        dest="groups",default="",help="Host groups to add the host to.If you want to use multiple groups,separate them with a ','.")
    parser.add_option("-t","--templates",action="store",type="string",\
	dest="templates",default="0",help="Templates to be linked to the host.If you want to use multiple templates, separate them with a ','. ") 
    parser.add_option("-i","--ip",action="store",type="string",\
	dest="ip",default="",help="IP address for hosts.")
    parser.add_option("-n","--name",action="store",type="string",\
	dest="name",help="Visible name of the host.")
    parser.add_option("--proxy",action="store",type="string",\
	dest="proxy",default="",help="name of the proxy that is used to monitor the host.")
    parser.add_option("--zabbix_type",action="store",type="int",\
        dest="zabbix_type",default="2",help="""Zabbix type of the host. 
Possible values are:
1 - Zabbix agent;
2 - (default) SNMP v1/2c.""")
    parser.add_option("--status",action="store",type="int",\
        dest="status",default="0",help="""Status and function of the host. 
Possible values are:
0 - (default) monitored host;
1 - unmonitored host.""")
    parser.add_option("-f","--file",dest="filename",\
        metavar="FILE",help="Load values from input file. Specify - for standard input Each line of file contains whitespace delimited: <hostname>4space<ip>4space<groups>4space<templates>")

    options,args = parser.parse_args()

    if not options.server:
        options.server = raw_input('server http:')

    if not options.username:
        options.username = raw_input('Username:')

    if not options.password:
        options.password = getpass()

    return options, args

def errmsg(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(-1)

if __name__ == "__main__":
    options, args = get_options()

    zapi = ZabbixAPI(options.server)
    zapi.login(options.username, options.password)
    hostname = options.hostname
    status = options.status
    ip = options.ip
    dns = ""
    name = options.name
    proxy = options.proxy
    zabbix_type = options.zabbix_type
    file = options.filename
    
    if proxy:
	proxy_id = zapi.proxy.get({"output": "proxyid","selectInterface": "extend","filter":{"host":proxy}})[0]['proxyid']
    else:
	proxy_id = ""
    
    if zabbix_type == 1:
        port = "10050"
    else:
        port = "161"
    
    if ip:
        use_ip = "1"
        
    else:
        use_ip = "0"
        dns = hostname

    if file:
        with open(file,"r") as f:
            content = f.readlines()
            for i in content:
                l = i.split("    ")
                hostname = l[0].rstrip()
                ip = l[1].rstrip()
                groups = l[2].rstrip()
                templates = l[3].rstrip()
		groups_id = zapi.hostgroup.get({"output": "groupid","filter": {"name":groups.split(",")}})
		templates_id = zapi.template.get({"output": "templateid","filter": {"host":templates.split(",")}})
                try:
		    print proxy_id
                    if proxy_id:
			print zapi.host.create({"host":hostname,"groups":groups_id,"templates":templates_id,"interfaces":[{"type":zabbix_type,"main":1,"useip":use_ip,"ip":ip,"dns":dns,"port":port}],"proxy_hostid":proxy_id,"status":status})
		    else:
			print zapi.host.create({"host":hostname,"groups":groups_id,"templates":templates_id,"interfaces":[{"type":zabbix_type,"main":1,"useip":use_ip,"ip":ip,"dns":dns,"port":port,"status":status}]})
                except Exception as e:
                    print str(e)
    else:
	groups = options.groups
	templates = options.templates
	groups_id = zapi.hostgroup.get({"output": "groupid","filter": {"name":groups.split(",")}})
	templates_id = zapi.template.get({"output": "templateid","filter": {"host":templates.split(",")}})
        print "The temlate ID %s" % templates_id
	try:
	    if proxy_id:
		print zapi.host.create({"host":hostname,"groups":groups_id,"templates":templates_id,"interfaces":[{"type":zabbix_type,"main":1,"useip":use_ip,"ip":ip,"dns":dns,"port":port}],"proxy_hostid":proxy_id,"status":status})
	    else:
		print zapi.host.create({"host":hostname,"groups":groups_id,"templates":templates_id,"interfaces":[{"type":zabbix_type,"main":"1","useip":use_ip,"ip":ip,"dns":dns,"port":port,"status":status}]})
	except Exception as e:
	    print str(e)
