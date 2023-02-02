from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel,info

tree = TreeTopo(depth=2, fanout=2)
net = Mininet(topo=tree)
net.start()

h1 = net.hosts[0]
h4 = net.hosts[3]
net.iperf((h1, h4))

setLogLevel('info')
info("***Running test\n")
h1.cmdPrint('ping -c 1 %s' % h4.IP())
info('\n')

net.stop()