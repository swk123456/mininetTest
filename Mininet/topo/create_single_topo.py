from mininet.net import Mininet
from mininet.topo import SingleSwitchTopo

single = SingleSwitchTopo(k=3)
net = Mininet(topo=single)
net.start()
net.pingAll()
net.stop()