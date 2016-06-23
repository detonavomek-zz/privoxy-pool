import time

from tor_pool import Tor, TorIpUpdateException

from pool import PrivoxyPool


class PrivoxyController(object):
	_pool = None
	_instances = None
	_start_ip = 8118
	
	def __init__(self, maximum_instances):
		self.maximum_instances = maximum_instances
		self._instances = {}
		self._create()

	def _create(self):
		self._pool = PrivoxyPool()
		for i in range(self.maximum_instances):
			privoxy_port = self._start_ip + i*2
			tor_port = privoxy_port + 1000
			tor_control_port = tor_port + 1
			self._pool.add(port=privoxy_port, tor=Tor(tor_port, tor_control_port))
			self._instances[privoxy_port] = True

	def run(self):
		self._pool.run_all()

	def stop(self):
		self._pool.stop_all()

	def _get_next(self):
		for port, good_ip in self._instances.items():
			if good_ip:
				return port

	def _update_instance(self):
		min_seconds = None
		for port in self._instances.keys():
			try:

				self._pool.update_tor_ip(port)
				self._instances[port] = True
				return
			except TorIpUpdateException as e:
				if not min_seconds:
					min_seconds = 10
				min_seconds = min(min_seconds, e.args[1])

		if min_seconds:
			time.sleep(min_seconds)
			self._update_instance()

	def next(self):
		port = self._get_next()
		
		if not port:
			self._update_instance()
			port = self._get_next()

		return port

	def set_bad(self, port):
		self._instances[port] = False
