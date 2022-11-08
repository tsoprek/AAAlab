from .alab_functions import connect_to_device, configure_device, read_file, teminate_connection


# Radius configuration files
radius_generic = 'config_templates/radius_generic'
radius_server = 'config_templates/radius_srv_cfg'
radius_group = 'config_templates/radius_gr_srv'
radius_gr_vrf = 'config_templates/radius_gr_vrf'
dot1x_intf = 'config_templates/dot1x_intf_cfg'
var=""


def Radius_Cfg(dev_list, server_list, vrf, source_if, dot1x_if):

    # iterate trough device list
    for device in dev_list:
        # Open connection
        conn = connect_to_device(device)

        # Apply general configuration
        generic_cfg = read_file(radius_generic, var)
        sent_generic= configure_device(conn, generic_cfg)
        print(sent_generic)

        # Configure all servers in list, create group and add servers to group
        for server in server_list:
            if server != '':
                server_cfg = read_file(radius_server, server)
                sent_server= configure_device(conn, server_cfg)
                group_cfg= read_file(radius_group, server)
                sent_group= configure_device(conn, group_cfg)
                print (sent_server, sent_group)
                #return (sent_server, sent_group)
            else:
                continue
        # Configure VRF and radius source interface
        vrf_cfg = read_file(radius_gr_vrf, vrf, source_if)
        sent_vrf= configure_device(conn, vrf_cfg)
        print(sent_vrf)

        # Configure interface for dot1x
        if dot1x_if != 'none' or dot1x_intf!='':
            dot1x_if_cfg= read_file(dot1x_intf, dot1x_if)
            print(dot1x_if_cfg)
            sent_dot1x_if= configure_device(conn, dot1x_if_cfg)

        else:
            continue
        teminate_connection(conn)
        return (sent_generic, sent_server, sent_group, sent_vrf, sent_dot1x_if)
