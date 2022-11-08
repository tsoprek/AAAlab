import paramiko
from paramiko import SSHClient
from time import sleep
from paramiko.ssh_exception import SSHException
from paramiko.ssh_exception import SSHException
from scripts.alab_functions import read_file

usr= "admin"
pswd= "Krakow123"
file= ("device_list")
retaincerts=("n")
chan_data = str("")

def Reset_Cfg_ISE(dev_list):

    for device in dev_list:
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        try:
            client.connect(str(device), username= usr, password= pswd)
        except paramiko.ssh_exception.NoValidConnectionsError:
            print('***** SSH connection issue. *****')
            file_to_wr = open("failed_devices", "a")
            file_to_wr.close()
            break
        except paramiko.ssh_exception.AuthenticationException:
            print ("Authentication faile!  ")
        chan = client.invoke_shell()
        print("**** Connected to " + device + "****")
        sleep(2)
        while True:
            if chan.recv_ready():
                chan_data = chan.recv(1024).decode('utf8')
                print(chan_data)
                sleep(1)
            else:
                continue
            if chan_data.endswith("start a new one:"):
                session = input("Would you like to continue previous session or start new one? ")
                sleep(1)
                chan.send(session + "\n")
            elif ("reset-config is success") in chan_data:
                chan_data = ""
                chan.send("\n")
                chan.close()
                break
            elif ("DATABASE PRIMING FAILED!") in chan_data:
                chan_data = ""
                chan.send("\n")
                chan.close()
                print("############# CONFIG-RESET FAILED! ############# ")
                print("#############    SKIPING DEVICE    ############# ")
                break
            elif chan_data.endswith("(current) UNIX password: "):
                chan.send("Krakow123\n")
                sleep(1)
            elif chan_data.endswith("New password: "):
                chan.send("Warsaw123")
                sleep(1)
            elif chan_data.endswith("Retype new password: "):
                chan.send("Warsaw123\n")
                sleep(3)
                client.connect(str(device), username=usr, password='Warsaw123')
                chan.send("confi t\n")
                sleep(1)
                chan.send("user admin password plain Krakow123 role admin\n")
                chan.send("exit\n")
                sleep(2)
            elif chan_data.endswith("/admin# "):
                chan.send("application reset-config ise \n")
                sleep(1)
            elif chan_data.endswith("factory defaults? (y/n): "):
                chan.send("y\n")
                sleep(1)
            elif chan_data.endswith("factory reset? (y/n): "):
                chan.send("y\n")
                sleep(1)
            elif chan_data.endswith("server certificates? (y/n): "):
                chan.send(retaincerts + "\n")
                sleep(1)
            elif chan_data.endswith("username to create[admin]: "):
                chan.send(usr + "\n")
                sleep(2)
            elif chan_data.endswith("Enter the password for 'admin': "):
                chan.send(pswd + "\n")
                sleep(1)
            elif chan_data.endswith("Re-enter the password for 'admin': "):
                chan.send(pswd + "\n")
                sleep(1)
                chan_data = ""  #Add hash to watch full process
                chan.send("\n") #Add hash to watch full process
                chan.close()    #Add hash to watch full process
                break           #Add hash to watch full process
            elif ("Time out") in chan_data:
                print("Error in connection")
