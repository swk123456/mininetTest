from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv

log = core.getLogger()
policyIpFile = "/home/swk/pox/firewall-policies-ip.csv"
policyMacFile = "/home/swk/pox/firewall-policies-mac.csv"

disabled_IP_pair = []
disabled_MAC_pair = []

dpid = []
have_firewall_dpid = []

def read_csv_file():
    global disabled_IP_pair, disabled_MAC_pair

    with open(policyIpFile, 'r') as rules:
        csvreader = csv.DictReader(rules)
        for line in csvreader:
            ip_0 = line['ip_0']
            ip_1 = line['ip_1']
            disabled_IP_pair.append((ip_0, ip_1))
            print("read file disabled IP pair ip0:", ip_0, " ip1:", ip_1)

    with open(policyMacFile, 'r') as rules:
        csvreader = csv.DictReader(rules)
        for line in csvreader:
            mac_0 = EthAddr(line['mac_0'])
            mac_1 = EthAddr(line['mac_1'])
            disabled_MAC_pair.append((mac_0, mac_1))
            print("read file disabled MAC pair mac0:", mac_0, " mac1:", mac_1)

def _handle_ConnectionUp (event):
    global dpid

    print("ConnectionUp: ", dpidToStr(event.connection.dpid))

    for m in event.connection.features.ports:
        if "eth1" in m.name:
            dpid.append(dpidToStr(event.connection.dpid))
            print("dpid=", event.connection.dpid)


def _handle_PacketIn(event):

    global disabled_IP_pair, dpid, have_firewall_dpid

    if (dpidToStr(event.connection.dpid) in dpid) and \
            (dpidToStr(event.connection.dpid) not in have_firewall_dpid):

        have_firewall_dpid.append(event.connection.dpid)

        for (source_ip, destination_ip) in disabled_IP_pair:

            message = of.ofp_flow_mod()
            message.command = of.OFPFC_MODIFY_STRICT
            message.idle_timeout = 0
            message.hard_timeout = 0
            message.priority = 65535
            message.match.dl_type = 0x0800
            message.match.nw_src = source_ip
            message.match.nw_dst = destination_ip
            message.actions.append(of.ofp_action_output(port=0))
            event.connection.send(message)

        for (source_mac, destination_mac) in disabled_MAC_pair:

            message = of.ofp_flow_mod()
            message.command = of.OFPFC_MODIFY_STRICT
            message.idle_timeout = 0
            message.hard_timeout = 0
            message.priority = 65535
            message.match.dl_src = source_mac
            message.match.dl_dst = destination_mac
            message.actions.append(of.ofp_action_output(port=0))
            event.connection.send(message)


def launch():
    read_csv_file()
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
