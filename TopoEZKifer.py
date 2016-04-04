#!/usr/bin/python

import sys
import os
import subprocess

import predefined

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Implement_Topology():
    '''Implement the topology XML'''

    def __init__(self, topology_tree=None, topology_xml=None, work_path=None):
        '''Init the parameters'''

        if topology_tree == None and topology_xml == None:
            print '[Both topolgy_tree and topology_xml are not presented.]'
            raise  RuntimeError, ('Both topolgy_tree and topology_xml are not presented!', 'in TopoEZKifer.py')
        if topology_xml != None:
            if os.path.isfile(topology_xml) == False:
                print '[The topology file "'+topology_xml+'" does not exist!]'
                raise NameError, ('The topology file "'+topology_xml+'" does not exist!', 'in TopoEZKifer.py')

        self.topology_tree = topology_tree
        self.topology_xml = topology_xml
        if work_path == None:
            self.work_path = os.path.split(os.path.realpath(__file__))[0]
        else:
            self.work_path = work_path
        self.pipework_cmd='pipework'

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

        self.node_variable = None
        self.node_container = None
        self.node_connection = None
        self.node_route = None
        self.node_command = None


    def run_shell_cmd(self, command, ok_msg, error_msg, doRaise=True):
        '''Return the status code'''
        print '[Run: '+command+']'
        shell_run = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        status_code = shell_run.wait()
        for line in  shell_run.stdout.readlines():
            print line
        if status_code == 0:
            print ok_msg
        else:
            if doRaise == True:
                print error_msg
                raise RuntimeError (error_msg,'in TopoEZKifer.py')
            else:
                print error_msg

        return status_code

    def read_topology(self):
        '''Read the topology file'''

        if self.topology_xml != None:
            tree = ET.ElementTree(file=self.topology_xml)

        if self.topology_tree != None:
            tree = self.topology_tree

        tree_root = tree.getroot()
        for subtree in tree_root:
            if subtree.tag == self.node_name_variable:
                self.node_variable = subtree
            elif subtree.tag == self.node_name_container:
                self.node_container = subtree
            elif subtree.tag == self.node_name_connection:
                self.node_connection = subtree
            elif subtree.tag == self.node_name_route:
                self.node_route = subtree
            elif subtree.tag == self.node_name_command:
                self.node_command = subtree

        if self.node_container == None or self.node_connection == None:
            print '[Node "'+self.node_name_container+'" and node "'+self.node_name_connection+'" are required in topology file!]'
            raise RuntimeError, ('Node "'+self.node_name_container+'" and node "'+self.node_name_connection+'" are required in topology file!', 'in TopoEZKifer.py')

    def get_final_var(self, replace_var):
        '''Return the variable value or the hard code'''
        if self.node_variable != None:
            if replace_var in self.node_variable.attrib:
                return self.node_variable.attrib[replace_var]
            else:
                return replace_var
        else:
            return replace_var

    def check_validity(self):
        '''Check the container validity'''
        pass

    def build_container(self):
        '''Build all the containers'''

        print '[Start to build containers...]'

        # image is required
        #container_node_label = { 'image':'image', 'cmd':'cmd', 'share_foler':'share_folder' }
        container_node_label = predefined.container_node_label

        for container_run in self.node_container:
            if container_node_label['share_foler'] in container_run.attrib:
                share_foler_run_part = '-v '+self.get_final_var(container_run.attrib[container_node_label['share_foler']])
            else:
                share_foler_run_part = ''

            if container_node_label['cmd'] in container_run.attrib:
                cmd_run_part = self.get_final_var(container_run.attrib[container_node_label['cmd']])
            else:
                cmd_run_part = ''

            if container_node_label['image'] not in container_run.attrib:
                print '[The '+container_node_label['image']+' is required for '+self.node_name_container+' .]'
                raise RuntimeError, ('The '+container_node_label['image']+' is required for '+self.node_name_container+' .', 'in TopoEZKifer.py')

            image_run_part = self.get_final_var(container_run.attrib[container_node_label['image']])

            cmd_to_run = 'docker run -idt --name '+self.get_final_var(container_run.tag)+' --privileged=true --net=none '+share_foler_run_part+' '+image_run_part+' '+cmd_run_part
            self.run_shell_cmd(cmd_to_run, '[The container "'+container_run.tag+'" has been started.]',
                               'Fail: The container "'+container_run.tag+'" can not be started.')


    def build_connection(self):
        '''Build the connections'''

        print '[Start to build connections...]'

        # In connection attrib, format -> 'eth1'='ovs1', both is variable

        # vlan is not required, vlan0=None
        #connection_node_label = { 'ovs':'ovs', 'container_interface':'container_interface',
        #                          'container_ip':'container_ip', 'container':'container',
        #                          'vlan':'vlan'
        #                          }

        connection_node_label = predefined.connection_node_label

        for connection_run in self.node_connection:
            if connection_node_label['vlan'] in connection_run.attrib:
                if self.get_final_var(connection_run.attrib[connection_node_label['vlan']]) == 0:
                    vlan_run_part = ''
                else:
                    vlan_run_part = '@'+self.get_final_var(connection_run.attrib[connection_node_label['vlan']])
            else:
                vlan_run_part = ''

            if connection_node_label['ovs'] not in connection_run.attrib or connection_node_label['container_interface'] not in connection_run.attrib or connection_node_label['container_ip'] not in connection_run.attrib or connection_node_label['container'] not in connection_run.attrib:
                print '[These for connection are required: '+connection_node_label['ovs']+'/'+connection_node_label['container_interface']+'/'+connection_node_label['container_ip']+'/'+connection_node_label['container']+']'
                raise RuntimeError, ('These for connection are required: '+connection_node_label['ovs']+'/'+connection_node_label['container_interface']+'/'+connection_node_label['container_ip']+'/'+connection_node_label['container'], 'in TopoEZKifer.py')

            ovs_run_part = self.get_final_var(connection_run.attrib[connection_node_label['ovs']])
            container_interface_run_part = self.get_final_var(connection_run.attrib[connection_node_label['container_interface']])
            container_ip_run_part = self.get_final_var(connection_run.attrib[connection_node_label['container_ip']])
            container_run_part = self.get_final_var(connection_run.attrib[connection_node_label['container']])

            cmd_to_run = self.pipework_cmd+' '+ovs_run_part+' -i '+container_interface_run_part + ' ' + container_run_part + ' ' + container_ip_run_part + ' ' + vlan_run_part
            self.run_shell_cmd(cmd_to_run, '[The connection "'+connection_run.tag+'" has been created.]',
                               'Fail: The connection "'+connection_run.tag+'" has not been created!')

            for (host_int, current_ovs) in self.node_connection.attrib.items():
                final_host_int = self.get_final_var(host_int)
                final_current_ovs = self.get_final_var(current_ovs)
                shell_run = subprocess.Popen('ip link show '+final_host_int+' |grep master', shell=True, stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT)
                run_result = shell_run.wait()
                if run_result == 0:
                    cmd_to_run = 'ovs-vsctl del-port $(ovs-vsctl port-to-br ' + final_host_int + ') ' + final_host_int
                    self.run_shell_cmd(cmd_to_run, '[The '+final_host_int+' has been removed from other ovs.]',
                                       'Fail: Removing '+final_host_int+' from other ovs fails!')

                cmd_to_run = 'ovs-vsctl add-port '+final_current_ovs+' '+final_host_int
                self.run_shell_cmd(cmd_to_run, '[The '+final_host_int+' has been added to '+final_current_ovs+']',
                                   'Fail: The '+final_host_int+' can not be added to '+final_current_ovs+'!')




    def build_route(self):
        '''Build the route'''
        #route_node_label = { 'container':'container', 'dst_net':'dst_net', 'gw':'gw' }
        route_node_label = predefined.route_node_label

        if self.node_route == None:
            return

        print '[Start to build the route...]'
        for route_run in self.node_route:
            if route_node_label['container'] not in route_run.attrib or route_node_label['dst_net'] not in route_run.attrib or route_node_label['gw'] not in route_run.attrib:
                print '['+route_node_label['container']+'/'+route_node_label['dst_net']+'/'+route_node_label['gw']+' for route are required!]'
                raise  RuntimeError, (route_node_label['container']+'/'+route_node_label['dst_net']+'/'+route_node_label['gw']+' for route are required!','in TopoEZKifer.py')

            final_container = self.get_final_var(route_run.attrib[route_node_label['container']])
            final_dst_net = self.get_final_var(route_run.attrib[route_node_label['dst_net']])
            final_gw = self.get_final_var(route_run.attrib[route_node_label['gw']])

            cmd_to_run = 'docker exec '+final_container+' ip route add '+final_dst_net+' via '+final_gw
            self.run_shell_cmd(cmd_to_run, '["'+final_dst_net+' via '+final_gw+'" in '+final_container+' has been added.]',
                               'Fail: "'+cmd_to_run+'" fails!')


    def build_command(self):
        '''Build the command'''
        #command_node_label = { 'container':'container', 'cmd':'cmd' }
        command_node_label = predefined.command_node_label

        if self.node_command == None:
            return

        print '[Start to build the command...]'
        for command_run in self.node_command:
            if command_node_label['container'] not in command_run.attrib or command_node_label['cmd'] not in command_run.attrib:
                print '["'+command_node_label['container']+'/'+command_node_label['cmd']+'" for command are required!]'
                raise RuntimeError, ('"'+command_node_label['container']+'/'+command_node_label['cmd']+'" for command are required!','in TopoEZKifer.py')

            final_container = self.get_final_var(command_run.attrib[command_node_label['container']])
            final_cmd = self.get_final_var(command_run.attrib[command_node_label['cmd']])

            cmd_to_run = 'docker exec '+final_container+' '+final_cmd
            self.run_shell_cmd(cmd_to_run, '['+final_cmd+' for '+final_container+' run successfully.]',
                               'Fail: '+final_cmd+' for '+final_container+' fails!')


    def add_privilege(self):
        '''Add the runnable privilege for all the shell files'''
        shell_run1 = subprocess.Popen('chmod +x '+self.work_path+'/*.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        run_result1 = shell_run1.wait()

        if run_result1 == 0:
            print '[All shell files in "'+self.work_path+'" have been added runnable privilege.]'
        else:
            print '[Warning: Adding runnable privilege for shell files in "'+self.work_path+'" fails.]'


    def check_shell_file(self):
        '''Check if all the needed shell files are here'''
        if os.path.isfile(self.work_path+'/pipework') == False:
            print '['+self.work_path+'/pipework does not exist!]'
            #raise RuntimeError ('Warning: "pipework" must be in current location!', 'in TopoEZKifer.py')
        else:
            self.pipework_cmd = self.work_path+'/'+self.pipework_cmd



    def build_all(self):
        '''Build all the parts'''
        self.check_shell_file()
        self.add_privilege()
        self.read_topology()
        self.check_validity()
        self.build_container()
        self.build_connection()
        self.build_route()
        self.build_command()




if __name__ == "__main__":


    if len(sys.argv) < 2:
        print "Usage:"
        print ''
        print "./TopoEZKifer <topology XML>"
        print ""
        exit()


    print "[Start to implement the topology...]"

    TopologyXML = sys.argv[1]

    myTOPO = Implement_Topology(topology_xml=TopologyXML)

    myTOPO.build_all()







