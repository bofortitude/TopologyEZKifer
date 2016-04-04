#!/bin/bash


current_brs=$(ovs-vsctl list-br)

for i in $current_brs
do
    all_ports=$(ovs-vsctl list-ports $i)
    for j in $all_ports
    do
        ip link show $j >/dev/null 2>/dev/null
        if [[ $? == 1 ]]; then
            ovs-vsctl del-port $i $j
            echo "[The \"$j\" has been removed from \"$i\".]"
        fi
    done
done






