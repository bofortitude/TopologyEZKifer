#!/bin/bash

if [[ $# -lt 3 ]]; then
    echo ""
    echo "./mgmtEZ.sh <external IP> <internal IP> <mgmt interface>"
    echo ""
    exit
fi







iptables -t nat -A PREROUTING -d $1 -j DNAT --to-destination $2
iptables -t nat -A POSTROUTING -s $2 -j SNAT --to $1
ip add add $1/32 dev $3




