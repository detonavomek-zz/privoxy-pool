import time

from privoxy_pool import PrivoxyController


privoxy_controller = PrivoxyController(maximum_instances=3)

print 'RUN'
privoxy_controller.run()

print 'START'
for i in range(10):
	port = privoxy_controller.next()
	print port
	privoxy_controller.set_bad(port)

print 'STOP'
privoxy_controller.stop()