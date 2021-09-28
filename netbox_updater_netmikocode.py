import re
import os
import argparse
import logging
import concurrent.futures

import pynetbox
from netmiko import (ConnectHandler,
                     NetMikoAuthenticationException,
                     NetMikoTimeoutException)


def read_from_devices(device_platform, device_ip, device_user,
                      device_password):
    # netmiko device_type:

    # Cisco IOS:       'cisco_ios'
    # Cisco Nexus:     'cisco_nxos'
    # Cisco ASA:       'cisco_asa'
    # Aruba OS:        'aruba_os'
    # PaloAlto PAN-OS: 'paloalto_panos'
    # Juniper Junos:   'juniper_junos'
    # Huawei VRP:      'huawei'

    # Cisco IOS
    if device_platform == 'Cisco IOS':
        device = {
            "device_type": "cisco_ios",
            "host": device_ip,
            "username": device_user,
            "password": device_password,
        }

        ''' Exmaple output: Cisco IOS Software, 7200 Software (C7200-ADVENTERPRISEK9-M)
         , Version 15.2(4)S7#, RELEASE SOFTWARE (fc4)'''

        command = "show version | include IOS Software"
        try:
            with ConnectHandler(**device) as net_connect:
                output = str(net_connect.send_command(command))
                version = re.search('Version(.*),', output).group(1)
            return version
        except NetMikoAuthenticationException as e:
            logging.error('%s: %s', e, device_ip)
        except NetMikoTimeoutException as e:
            logging.error('%s: %s', e, device_ip)
        except Exception as e:
            logging.error('%s: %s', e, device_ip)


# Cisco ASA OS
    elif device_platform == 'Cisco ASA':
        device = {
            "device_type": "cisco_asa",
            "host": device_ip,
            "username": device_user,
            "password": device_password,
        }

        '''Example output:..Cisco Adaptive Security Appliance Software Version 8.4(2) n...'''
        command = "show version | include Appliance"
        try:
            with ConnectHandler(**device) as net_connect:
                output = net_connect.send_command(command)
                version = re.search('Version(.*)\n', output).group(1)
                return version
        except NetMikoAuthenticationException as e:
            logging.error('%s: %s', e, device_ip)
        except NetMikoTimeoutException as e:
            logging.error('%s: %s', e, device_ip)
        except Exception as e: 
            logging.error('%s: %s', e, device_ip)   
       
       
# Cisco Nexus OS
    elif device_platform == 'Cisco Nexus':
        device = {
            "device_type": "cisco_nxos",
            "host": device_ip,
            "username": device_user,
            "password": device_password,
        }

        command = "show version"

        try:
            with ConnectHandler(**device) as net_connect:
                output = net_connect.send_command(command)
                version = re.search('Version(.*)', output).group(1)
            return version
        except NetMikoAuthenticationException as e:
            logging.error('%s: %s', e, device_ip)
        except NetMikoTimeoutException as e:
            logging.error('%s: %s', e, device_ip)
        except Exception as e: 
            logging.error('%s: %s', e, device_ip)  

        
# ArubaOS
    elif device_platform == 'Aruba OS':
        device = {
            "device_type": "aruba_os",
            "host": device_ip,
            "username": device_user,
            "password": device_password,
        }

        ''' Example output:... ArubaOS(Model:135), Version 6.3.1.1-4.0.0.0 \n....'''
        command = "show version "
        try:
            with ConnectHandler(**device) as net_connect:
                output = net_connect.send_command(command)
                version = re.search('Version (.*)\n', output).group(1)
                return version               
        except NetMikoAuthenticationException as e:
            logging.error('%s: %s', e, device_ip)
        except NetMikoTimeoutException as e:
            logging.error('%s: %s', e, device_ip)
        except Exception as e: 
            logging.error('%s: %s', e, device_ip) 
        

# PaloAlto PAN-OS
    elif device_platform == 'PaloAlto PAN-OS':
        device = {
            "device_type": "paloalto_panos",
            "host": device_ip,
            "username": device_user,
            "password": device_password,
        }
 
        ''' Example output: ...\n sw_version:8.1.6 \n...'''
        command = "show system info "     
        try:
            with ConnectHandler(**device) as net_connect:
                output = net_connect.send_command(command)
                version = re.search('sw_version:(.*)\n', output).group(1)
            return version        
        except NetMikoAuthenticationException as e:
            logging.error('%s: %s', e, device_ip)
        except NetMikoTimeoutException as e:
            logging.error('%s: %s', e, device_ip)
        except Exception as e: 
            logging.error('%s: %s', e, device_ip) 
        
        
# Juniper Junos
    elif device_platform == 'Juniper Junos':
        device = {
            "device_type": "juniper_junos",
            "host": device_ip,
            "username": device_user,
            "password": device_password,
        }

        # Example: JUNOS Base OS Software Suite [16.1R6.7]
        command = "show version | match Base | match Software"
        try:
            with ConnectHandler(**device) as net_connect:
                output = net_connect.send_command(command)
                version = re.search('\[(.*)]', output).group(1)
                print(version)
            return version
        except NetMikoAuthenticationException as e:
            logging.error('%s: %s', e, device_ip)
        except NetMikoTimeoutException as e:
            logging.error('%s: %s', e, device_ip)
        except Exception as e: 
            logging.error('%s: %s', e, device_ip) 


# Huawei VRP
    elif device_platform == 'Huawei VRP':
        device = {
            "device_type": "huawei",
            "host": device_ip,
            "username": device_user,
            "password": device_password,
        }

        ''' Example:VRP (R) software, Version 5.170 (NE40E&80E V600R009C20SPC600)...'''
        command = "dis version | include software"
        try:
            with ConnectHandler(**device) as net_connect:
                output = net_connect.send_command(command)
                version = re.search('(V\d.*)\)', output).group(1)
                print(version)
            return version
                
        except NetMikoAuthenticationException as e:
            logging.error('%s: %s', e, device_ip)
        except NetMikoTimeoutException as e:
            logging.error('%s: %s', e, device_ip)
        except Exception as e: 
            logging.error('%s: %s', e, device_ip) 

    else:
         
        version='device platform is not defined'
        logging.error('%s is not defined, device ip is %s ', device_platform,device_ip)
        return version        


def update_netbox(device,device_user,device_password):
    
    device_ip = device.primary_ip.address.split('/')[0]
    device_platform = str(device.platform)
    device_version = read_from_devices(
        device_platform, device_ip, device_user, device_password)
    device.custom_fields = {'sw_version': device_version}
    device.save()


def read_from_netbox(url, token):
    nb = pynetbox.api(url=url, token=token)
    devices = nb.dcim.devices.filter(tenant='noc', status='active')
    return devices  


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--netbox-url', required=True)
    parser.add_argument('--netbox-token', required=True)
    parser.add_argument('--device-username', required=True)
    parser.add_argument('--device-password', required=True)
    args = parser.parse_args()

    device_user = args.device_username
    device_password = args.device_password
    devices=read_from_netbox(args.netbox_url, args.netbox_token)
    
    executor = concurrent.futures.ThreadPoolExecutor(5)
    futures = [executor.submit(update_netbox,device,device_user,
    device_password) for device in devices]
    concurrent.futures.wait(futures)
