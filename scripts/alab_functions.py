#!/usr/bin/env python3
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException
from paramiko.ssh_exception import SSHException

username = 'cisco'
passwd = 'cisco'
#file='devices_list'
intf = 'gig0/0'
var = 0
# Open file and return list
def read_file(file, *args):
    with open(file) as f:
        output = f.read().format(*args).splitlines()
        f.close()
        #print (output)
        return output

# Open connection to device and return device session
def connect_to_device(device):

    print('Connecting to ' + device)
    ios_dev = {
        'device_type': 'cisco_ios',
        'host': device,
        'port': '22',
        'username': username,
        'password': passwd,
        'secret' : 'cisco!123'
    }
    try:
        connection = ConnectHandler(**ios_dev)
    except NetMikoAuthenticationException:
        print('Authentication failed '+device)
        exit()
    except NetMikoTimeoutException:
        print ('Timeout connecting to device. Check connectivity.')
        exit()
    except EOFError:
        print ('End of file while attempting device. ' + device)
        exit()
    except SSHException:
        print ('SSH issue. Please make sure SSH is configured on device.')
        exit()
    except Exception as unknow_error:
        print('There was other error: ' + unknow_error)
        exit()
    return connection

# Configure device and close session
def configure_device(connection, configuration):
    connection.enable()
    output = connection.send_config_set(configuration)
    return output

    # SGT credentials is global command so handled by this section, before going to config mode

    #if selection == 2:
    #    CTScred = 'cts credentials id cisco password cisco\n'
    #    output2 = connection.send_command_timing(CTScred)
    #    print(output2)

    # Apply selected configuration

def teminate_connection(connection):
    connection.disconnect()

### Main program - RUN
#configuration = read_file(file)
#device_list = read_file('devices_list.txt')
#for device in device_list:
#    conn = connect_to_device(device)
#    configure_device(conn, configuration)
