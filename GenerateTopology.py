#!/usr/bin/python

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

try:
    from xml.etree.cElementTree import Element, SubElement, ElementTree
except ImportError:
    from xml.etree.ElementTree import Element, SubElement, ElementTree

from xml.dom import minidom
import sys
import predefined

class GenerateTopology():
    '''Generate topology XML'''
    def __init__(self):

        #self.node_name_variable = 'variable'
        #self.node_name_container = 'container'
        #self.node_name_connection = 'connection'
        #self.node_name_route = 'route'
        #self.node_name_command = 'command'

        self.node_name_variable = predefined.node_name_variable
        self.node_name_container = predefined.node_name_container
        self.node_name_connection = predefined.node_name_connection
        self.node_name_route = predefined.node_name_route
        self.node_name_command = predefined.node_name_command

        self.root = Element('Topology')
        self.node_variable = SubElement(self.root, self.node_name_variable)
        self.node_container = SubElement(self.root, self.node_name_container)
        self.node_connection = SubElement(self.root, self.node_name_connection)
        self.node_route = SubElement(self.root, self.node_name_route)
        self.node_command = SubElement(self.root, self.node_name_command)
        self.tree = ElementTree(self.root)


    def write(self, file_name):
        xml_string = ET.tostring(self.root)
        mytree = minidom.parseString(xml_string)
        to_write = mytree.toprettyxml(encoding='utf-8')
        #xml_string = mytree.toxml('utf-8')
        output = open(file_name, 'w')
        output.write(to_write)
        output.close()

    def add_node_item(self, node, item, item_attrib):
        # node -> object | item(name) -> string | item_attrib -> dict
        sub_element = SubElement(node, item)
        sub_element.attrib = item_attrib


    def add_node_attrib(self, node, attrib_key, attrib_value):
        # node -> object | attrib_key -> string | attrib_value -> string
        node.attrib[attrib_key] = attrib_value

    def del_node_item(self, node, item):
        # node -> object | item(name) -> string
        for i in node.findall(item):
            node.remove(i)

    def del_node_attrib(self, node, key):
        # node -> object | key -> string
        if key in node.attrib:
            del node.attrib[key]

    def add_variable_attrib(self, key, value):
        self.del_node_attrib(self.node_variable, key)
        self.add_node_attrib(self.node_variable, key, value)

    def del_variable_attrib(self, key):
        self.del_node_attrib(self.node_variable, key)

    def add_container(self, container_name, image, cmd = None, share_folder = None):
        #container_node_label = {'image': 'image', 'cmd': 'cmd', 'share_foler': 'share_folder'}
        container_node_label = predefined.container_node_label
        self.del_node_item(self.node_container, container_name)
        container_attrib = {container_node_label['image']:image}
        if cmd != None:
            container_attrib[container_node_label['cmd']:cmd]
        if share_folder != None:
            container_attrib[container_node_label['share_foler']:share_folder]
        self.add_node_item(self.node_container, container_name, container_attrib)

    def del_container(self, container_name):
        self.del_node_item(self.node_container, container_name)

    def add_connection_attrib(self, key, value):
        self.del_node_attrib(self.node_connection, key)
        self.add_node_attrib(self.node_connection, key, value)

    def del_connection_attrib(self, key):
        self.del_node_attrib(self.node_connection, key)

    def add_connection(self, connection_name, ovs, container_interface, container_ip, container, vlan='0'):
        #connection_node_label = {'ovs': 'ovs', 'container_interface': 'container_interface',
        #                         'container_ip': 'container_ip', 'container': 'container',
        #                         'vlan': 'vlan'
        #                         }
        connection_node_label = predefined.connection_node_label
        self.del_node_item(self.node_connection, connection_name)
        connection_attrib = {
            connection_node_label['ovs']:ovs,
            connection_node_label['container_interface']:container_interface,
            connection_node_label['container_ip']:container_ip,
            connection_node_label['container']:container,
            connection_node_label['vlan']:vlan
        }
        self.add_node_item(self.node_connection, connection_name, connection_attrib)

    def del_connection(self, connection_name):
        self.del_node_item(self.node_connection, connection_name)

    def add_route(self, route_name, container, dst_net, gw ):
        #route_node_label = {'container': 'container', 'dst_net': 'dst_net', 'gw': 'gw'}
        route_node_label = predefined.route_node_label
        self.del_node_item(self.node_route, route_name)
        route_attrib = {
            route_node_label['container']:container,
            route_node_label['dst_net']:dst_net,
            route_node_label['gw']:gw
        }
        self.add_node_item(self.node_route, route_name, route_attrib)


    def del_route(self, route_name):
        self.del_node_item(self.node_route, route_name)

    def add_command(self, command_name, container, cmd):
        #command_node_label = {'container': 'container', 'cmd': 'cmd'}
        command_node_label = predefined.command_node_label
        self.del_node_item(self.node_command, command_name)
        command_attrib = {
            command_node_label['container']:container,
            command_node_label['cmd']:cmd
        }
        self.add_node_item(self.node_command, command_name, command_attrib)

    def del_command(self, command_name):
        self.del_node_item(self.node_command, command_name)



if __name__ == "__main__":
    myTOPO = GenerateTopology()

    file_name = 'example_Topology.xml'
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]


    myTOPO.add_variable_attrib('server_image', 'ubuntu:apache2')
    myTOPO.add_variable_attrib('ovs_name', 'ovs1')
    myTOPO.add_container('server1', 'server_image')
    myTOPO.add_connection_attrib('eth1', 'ovs_name')
    myTOPO.add_connection('link1', 'ovs_name', 'eth1', '10.76.1.1/16', 'server1', vlan='1101')
    myTOPO.add_route('route1', 'server1', '100.1.1.0/24', '10.76.1.101')
    myTOPO.add_command('command1', 'server1', 'ip add add 200.1.1.1/24 dev lo')
    myTOPO.write(file_name)



