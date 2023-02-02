from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink

net = Mininet(host=CPULimitedHost, link=TCLink)

c0 = net.addController()
s0 = net.addSwitch('s0')
h0 = net.addHost('h0')
h1 = net.addHost('h1', cpu=0.5)
h2 = net.addHost('h1', cpu=0.5)

net.addLink(h0, s0, bw=10, delay='5ms',
            max_queue_size=1000, loss=10, use_htb=True)
net.addLink(h1, s0)
net.addLink(h2, s0)

net.start()
net.pingAll()
net.stop()