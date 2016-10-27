import time, urllib2, json

import requests

from privoxy_pool import PrivoxyController


privoxy_controller = PrivoxyController(maximum_instances=3)

def get_ip(port):
	proxies = {"http" : "http://127.0.0.1:"+str(port)}
	content = requests.get('http://api.ipify.org?format=json', proxies=proxies).content
	return json.loads(content)['ip']

print 'RUN'
privoxy_controller.run()

print 'START'
for i in range(10):
	port = privoxy_controller.next()
	print "http://127.0.0.1:{port} --> {ip}".format(port=port, ip=get_ip(port))
	privoxy_controller.set_bad(port)

print 'STOP'
privoxy_controller.stop()