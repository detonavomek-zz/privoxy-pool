import time

from tor_pool import Tor, TorIpUpdateException

from privoxy_pool import PrivoxyPool


privoxies = PrivoxyPool()

print 'START'
privoxies.add(port=8118, tor=Tor(9118, 9119))
privoxies.add(port=8120, tor=Tor(9120, 9121))
privoxies.add(port=8122, tor=Tor(9122, 9123))

print privoxies.instances

print 'RUN 8118'
privoxies.run(8118)

print privoxies.instances

print "FAST UPDATE TOR IP 8118"
try:
	privoxies.update_tor_ip(8118)
	raise Exception('IP Update Error. Need wait 10 seconds')
except TorIpUpdateException as e:
	from ipdb import set_trace; set_trace()

print privoxies.instances

print "NORMAL UPDATE TOR IP 8118"
time.sleep(10)
privoxies.update_tor_ip(8118)

print privoxies.instances

print "RUN ALL"
privoxies.run_all()

print privoxies.instances

print "STOP 8118"
privoxies.stop(8118)

print privoxies.instances

print "STOP ALL"
privoxies.stop_all()

print privoxies.instances
