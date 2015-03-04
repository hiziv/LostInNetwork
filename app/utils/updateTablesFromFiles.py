#!/usr/bin/python3
# Version 1.0
# Author hiziv
from app import app
from app import db
from app.models.device import Device
from app.models.configuration import Configuration
import re

def main():

#    conf_file='/home/tor/LostInNetwork/data/rtr1-run.txt'
    for device in Device.query.all():
        run_file="data/" + device.name + "-run.txt"
        route_file="data/" + device.name + "-route.txt"
        run_configuration=Configuration(path=run_file)
        route_configuration=Configuration(path=route_file)
        run_configuration.save()
        route_configuration.save()
        device.configuration_id.append(run_configuration)
    #    device.configuration.append(route_configuration)
        device.save()
        #print (conf_file)
#        #print (device.configuration_id)
#
#        for lines in open(conf_file):
#            lines=lines.strip()
#
#            version_Search=re.search('(?i)version\s(.*)',lines)
#            if version_Search:
#                version=version_Search.group(1)
#                print ("version :"+ version)
#            interface_Search=re.search('(?i)interface\s(.*)',lines)
#            if interface_Search:
#                interface=interface_Search.group(1)
#                print ("interface : "+ interface)
#
if __name__ == '__main__':
                    main()

