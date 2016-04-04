#!/bin/bash


currentContainers=`docker ps -q`
if [[ $currentContainers != "" ]]; then
    echo "[Killing the alive containers...]"
    docker kill $currentContainers
    echo "[All the alive containers have been killed.]"
fi


deadContainer=`docker ps -aq`

if [[ $deadContainer != "" ]]; then
    echo "[Removing the stopped containers...]"
    docker rm $deadContainer
    echo "[All the stopped containers have been removed.]"
fi

sleep 0.5

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


