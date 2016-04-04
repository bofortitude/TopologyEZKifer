#!/bin/bash


if [[ $# -lt 2 ]]; then
    echo "./int2OVSEZ.sh <host interface> <ovs name>"
    exit
fi

host_interface=$1
ovs_name=$2


ip link show $host_interface|grep master >/dev/null
if [[ $? == 0 ]]; then
    duplicate_ovs=$(ovs-vsctl port-to-br $host_interface)
    ovs-vsctl del-port $duplicate_ovs $host_interface
    echo "[The \"$host_interface\" has been removed from \"$duplicate_ovs\".]"
fi


ovs-vsctl add-port $ovs_name $host_interface
echo "[The \"$host_interface\" has been added to \"$ovs_name\".]"



