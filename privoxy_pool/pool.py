from privoxy import Privoxy


class PrivoxyPool(object):

	_instances = None

	def __init__(self):
		self._instances = {}

	@property
	def instances(self):
		res = 'Privoxy instances:\n'
		for port, instance in self._instances.items():
			res += '{port} {tor.port} {status}\n'.format(
				port=instance.port,
				tor=instance.tor,
				status=instance.status)
		return res

	def add(self, port, tor):
		self._instances[port] = Privoxy(port, tor)
		return self._instances[port]

	def remove(self, port):
		del self._instances[port]

	def run(self, port):
		self._instances[port].run()

	def run_all(self):
		for port, instance in self._instances.items():
			instance.run()

	def update_tor_ip(self, port):
		return self._instances[port].tor.update_ip()

	def stop(self, port):
		self._instances[port].stop()

	def stop_all(self):
		for port, instance in self._instances.items():
			instance.stop()
