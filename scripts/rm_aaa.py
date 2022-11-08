import paramiko
from paramiko import SSHClient
from time import sleep

import re
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException
from paramiko.ssh_exception import SSHException

usr= "cisco"
pswd= "cisco"
secret = 'cisco!123'

def rm_AAA(connection):
    connection.enable()
    showipinterface = "show ip interface brie"
    interfaces=connection.send_command_timing(showipinterface)
    showrunaaa='show run aaa'
    cmdshowrunaaa=connection.send_command_timing(showrunaaa)
    removecfg=[]
    for line in cmdshowrunaaa.splitlines():
        if line.startswith('radius '):
            nob=('no '+line)
            removecfg.append(nob)
            continue
        if line.startswith('aaa auth') or line.startswith("aaa ser") or line.startswith("aaa group") or line.startswith("aaa acc") or line.startswith("tacacs"):
            nob=('no '+line)
            removecfg.append(nob)
            continue
    connection.send_config_set(removecfg)
    template = re.compile("(GigabitEthernet[0-9\/]+)\s+(unassigned)\s+([a-zA-Z]+)\s+([a-zA-Z]+)\s+(up|down|administratively down)\s+(up|down)")
    for i in interfaces.splitlines():
        found_if=template.match(i)
        if found_if:
            if found_if[5]=='down' or found_if[5]=='administratively down' and found_if[6]=='down':
                interfacedefault = ['default interface '+found_if[1], 'interface '+found_if[1],'sw mode access']
                connection.send_config_set(interfacedefault)

    #with open('/config_templates/LabSwDefault') as cfg:                   ###Default config
    #    cfglines = cfg.read().splitlines()
    #    print('Following global config will be applied: \n')
    #    print(cfglines)
    #    connection.send_config_set(cfglines)


def ConnectToDevice(device):
        ios_dev = {
            'device_type': 'cisco_ios',
            'host': device,
            'port': '22',
            'username': usr,
            'password': pswd,
            'secret' : secret
        }
        try:
            net_connect = ConnectHandler(**ios_dev)
        except NetMikoAuthenticationException:
            print ('Authentication failed '+ip_address)

        except NetMikoTimeoutException:
            print('Timeout to device. Check connectivity.')
        except EOFError:
            print ('End of file while attempting device. ' + ip_address)
        except SSHException:
            print('SSH issue. Please check if SSH is configured on device. ')
        except Exception as unknow_error:
            print ('There was other error: ' + unknow_error)
        return net_connect

device='10.0.1.20'
con=ConnectToDevice(device)
print (con)
rm=rm_AAA(con)
print(rm)