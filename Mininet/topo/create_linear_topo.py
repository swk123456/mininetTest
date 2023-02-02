from mininet.net import Mininet
from mininet.topo import LinearTopo

linear = LinearTopo(k=6)
net = Mininet(topo=linear)
net.start()
net.pingAll()
net.stop()