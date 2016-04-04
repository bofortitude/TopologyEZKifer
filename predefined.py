#!/usr/bin/python

node_name_variable = 'variable'
node_name_container = 'container'
node_name_connection = 'connection'
node_name_route = 'route'
node_name_command = 'command'




container_node_label = { 'image':'image', 'cmd':'cmd', 'share_foler':'share_folder' }
connection_node_label = {'ovs': 'ovs', 'container_interface': 'container_interface',
                         'container_ip': 'container_ip', 'container': 'container',
                         'vlan': 'vlan'
                         }
route_node_label = { 'container':'container', 'dst_net':'dst_net', 'gw':'gw' }
command_node_label = { 'container':'container', 'cmd':'cmd' }









