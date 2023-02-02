from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.packet.arp import arp
from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.packet_base import packet_base
from pox.lib.packet.packet_utils import *
import pox.lib.packet as pkt
from pox.lib.recoco import Timer
import csv

log = core.getLogger()
netFile = "/home/swk/pox/net.csv"

net = []
ip = [([0] * 20) for j in range(20)]

s1_dpid = 0
s2_dpid = 0
s3_dpid = 0
s4_dpid = 0
s5_dpid = 0

def read_csv_file():
    global net, ip

    with open(netFile, 'r') as rules:
        csvreader = csv.DictReader(rules)
        for line in csvreader:
            netId = int(line['netId'])
            IP = line['IP']
            net.append((netId, IP))
            #print("read file netId:", netId, " host's IP:", IP)

    for (Id1, Ip1) in net:
        netId = Id1
        ip[netId][0] = Ip1
        i = 1
        for (Id2, Ip2) in net:
            if Id1 == Id2 and Ip1 != Ip2:
                ip[netId][1] = Ip2
                i += 1

    for netId in range(20):
        if ip[netId][0] != 0:
            print("netId: ", netId)
            for i in range(20):
                if ip[netId][i] != 0:
                    print("ip:", ip[netId][i])

def _handle_ConnectionUp(event):
    global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid

    print("ConnectionUp: ", dpidToStr(event.connection.dpid))

    for m in event.connection.features.ports:

        if m.name == "s1-eth1":
            s1_dpid = event.connection.dpid
            print("s1_dpid=", s1_dpid)

        elif m.name == "s2-eth1":
            s2_dpid = event.connection.dpid
            print("s2_dpid=", s2_dpid)

        elif m.name == "s3-eth1":
            s3_dpid = event.connection.dpid
            print("s3_dpid=", s3_dpid)

        elif m.name == "s4-eth1":
            s4_dpid = event.connection.dpid
            print("s4_dpid=", s4_dpid)

        elif m.name == "s5-eth1":
            s5_dpid = event.connection.dpid
            print("s5_dpid=", s5_dpid)

def _handle_PacketIn(event):
    global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid, net

    packet = event.parsed

    if event.connection.dpid == s1_dpid:

        table = [0 * 20]
        for netId in range(20):
            if ip[netId][0] != 0:
                for i in range(20):
                    if ip[netId][i] == "10.0.0.2":
                        table = ip[netId]
        print("s1_dpid", table)

        a = packet.find('arp')

        if a and a.protodst == "10.0.0.2" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.3" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.4" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.5" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        for dst in table:
            msg = of.ofp_flow_mod()
            msg.priority = 100
            msg.idle_timeout = 0
            msg.hard_timeout = 0
            msg.match.dl_type = 0x0800
            msg.match.nw_dst = dst
            if dst != "10.0.0.2":
                msg.actions.append(of.ofp_action_output(port=2))
            else:
                msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

    elif event.connection.dpid == s2_dpid:

        table = [0 * 20]
        for netId in range(20):
            if ip[netId][0] != 0:
                for i in range(20):
                    if ip[netId][i] == "10.0.0.3":
                        table = ip[netId]
        print("s2_dpid", table)

        a = packet.find('arp')

        if a and a.protodst == "10.0.0.2" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.3" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.4" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.5" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        for dst in table:
            msg = of.ofp_flow_mod()
            msg.priority = 100
            msg.idle_timeout = 0
            msg.hard_timeout = 0
            msg.match.dl_type = 0x0800
            msg.match.nw_dst = dst
            if dst != "10.0.0.3":
                msg.actions.append(of.ofp_action_output(port=2))
            else:
                msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

    elif event.connection.dpid == s3_dpid:

        table = [0 * 20]
        for netId in range(20):
            if ip[netId][0] != 0:
                for i in range(20):
                    if ip[netId][i] == "10.0.0.4":
                        table = ip[netId]
        print("s3_dpid", table)

        a = packet.find('arp')

        if a and a.protodst == "10.0.0.2" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.3" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.4" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.5" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        for dst in table:
            msg = of.ofp_flow_mod()
            msg.priority = 100
            msg.idle_timeout = 0
            msg.hard_timeout = 0
            msg.match.dl_type = 0x0800
            msg.match.nw_dst = dst
            if dst != "10.0.0.4":
                msg.actions.append(of.ofp_action_output(port=2))
            else:
                msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

    elif event.connection.dpid == s4_dpid:

        table = [0 * 20]
        for netId in range(20):
            if ip[netId][0] != 0:
                for i in range(20):
                    if ip[netId][i] == "10.0.0.5":
                        table = ip[netId]
        print("s4_dpid", table)

        a = packet.find('arp')

        if a and a.protodst == "10.0.0.2" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.3" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.4" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.5" and a.protodst in table:
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

        for dst in table:
            msg = of.ofp_flow_mod()
            msg.priority = 100
            msg.idle_timeout = 0
            msg.hard_timeout = 0
            msg.match.dl_type = 0x0800
            msg.match.nw_dst = dst
            if dst != "10.0.0.5":
                msg.actions.append(of.ofp_action_output(port=2))
            else:
                msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

    elif event.connection.dpid == s5_dpid:
        a = packet.find('arp')

        if a and a.protodst == "10.0.0.2":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.3":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.4":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.5":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.actions.append(of.ofp_action_output(port=4))
            event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)

def launch():
    read_csv_file()
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)