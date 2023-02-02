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
import time

log = core.getLogger()

s1_dpid = 0
s2_dpid = 0
s3_dpid = 0
s4_dpid = 0
s5_dpid = 0

turn = 0

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
    global s1_dpid, s2_dpid, s3_dpid, s4_dpid, s5_dpid

    packet = event.parsed

    if event.connection.dpid == s1_dpid:

        a = packet.find('arp')

        if a and a.protodst == "10.0.0.1":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.2":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.3":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.4":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=4))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.5":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=5))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.6":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=6))
            event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=6))
        event.connection.send(msg)

    elif event.connection.dpid == s2_dpid:

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.in_port = 1
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.in_port = 2
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

    elif event.connection.dpid == s3_dpid:

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.in_port = 1
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.in_port = 2
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

    elif event.connection.dpid == s4_dpid:

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.in_port = 1
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.in_port = 2
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

    elif event.connection.dpid == s5_dpid:

        a = packet.find('arp')

        if a and a.protodst == "10.0.0.1":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.2":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.3":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.4":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=4))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.5":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=5))
            event.connection.send(msg)

        if a and a.protodst == "10.0.0.6":
            msg = of.ofp_packet_out(data=event.ofp)
            msg.priority = 100
            msg.actions.append(of.ofp_action_output(port=6))
            event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.1"
        msg.actions.append(of.ofp_action_output(port=1))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.2"
        msg.actions.append(of.ofp_action_output(port=2))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.3"
        msg.actions.append(of.ofp_action_output(port=3))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.4"
        msg.actions.append(of.ofp_action_output(port=4))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.5"
        msg.actions.append(of.ofp_action_output(port=5))
        event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        msg.priority = 0
        msg.match.dl_type = 0x0800
        msg.match.nw_dst = "10.0.0.6"
        msg.actions.append(of.ofp_action_output(port=6))
        event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)