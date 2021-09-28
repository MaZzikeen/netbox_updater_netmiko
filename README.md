# netbox_updater_netmiko

netbox_updater_netmiko is written in Python3.

## Setup

Clone the project:
```
git clone https://github.com/MaZzikeen/netbox_updater_netmiko
and then go to ./netbox_updater_netmiko directory
```

Create a virtual environment to run the script(optional):
```

python3 -m venv venv
source venv/bin/activate
```

Install required libraries:
```
pip3 install -r requirements.txt 
```

Run the script in below format:
```
python netbox_updater_netmiko.py  --netbox-url NETBOXURL  --netbox-token TOKEN --device-username USERNAME --device-password PASSWORD 
## if password includes special characters put it in the " ".
```


## Architecture
The script aim is to get OS Version from Network devices and Update the custom_field {sw_version} part in the Netbox.

The script includes 3 functions:

1.read_from_netbox(url, token)

2.read_from_devices(device_platform, device_ip, device_user,device_password)

3.update_netbox(device,device_user,device_passwordr)

#### read_from_netbox(url, token):

Gets devices from netbox . In this script filter is used to only get devices with status: “active" and tenant:"noc".
pynetbox library is used to interact with Netbox.


#### read_from_devices(device_platform, device_ip, device_user, device_password)

netmiko library uses different device_type for connecting to different platforms.
in the script device_typle is specified based on device_platform.
```
## NOTE: in this script device_platforms defined as below:
device_platform 

    'Cisco IOS': 'cisco_ios',
    'Cisco Nexus': 'cisco_nxos',
    'Cisco ASA': 'cisco_asa',
    'Aruba OS': 'aruba_os',
    'PaloAlto PAN-OS': 'paloalto_panos',
    'Juniper Junos': 'juniper_junos',
    'Arista EOS': 'eos',
    'Huawei VRP': 'huawei'

If these platforms are defined diffently on your netbox
You should change the device_platform keys in the script based what you defined on
Netbox.
```
netmiko ConnectHandeler uses device_type,device IP,device username,device password to connect to devices.
for each platform related command is used to get the os_version.
 
#### update_netbox(device,device_user,device_password)

Get the OS Version from read_from_devices function and updates the custom_field {sw_version} part in the Netbox.

#### For Multi-Threading concurrent.futures is used.
