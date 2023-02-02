from mininet.net import Mininet

net = Mininet()

c0 = net.addController()
s0 = net.addSwitch('s0')
h0 = net.addHost('h0')
h1 = net.addHost('h1')

net.addLink(h0, s0)
net.addLink(h1, s0)

h0.setIP('192.168.1.2', 24)
h1.setIP('192.168.1.3', 24)

net.start()
net.pingAll()
net.stop()