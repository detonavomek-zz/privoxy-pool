from datetime import datetime
import subprocess
import time
import os

from jinja2 import Template


TEMPLATE_CONFIG = """
forward-socks5t / 127.0.0.1:{{ tor_port }} .
listen-address    :{{ port }}

"""

class Privoxy(object):

	CONFIG_PATH = '/tmp/privoxy.config.{}'
	PRIVOXY_PATH = '/usr/local/sbin/privoxy'

	STATUSES = {
		1: 'STOP',
		2: 'RUN'
	}

	port = None
	tor = None
	_status = None
	

	@property
	def status(self):
		return Privoxy.STATUSES[self._status]

	def __init__(self, port, tor):

		self.CONFIG_PATH = Privoxy.CONFIG_PATH.format(port)
		
		self.port = port
		self.tor = tor
		self._status = 1
		
		self._create()

	def _create(self):
		template = Template(TEMPLATE_CONFIG)
		config = template.render(port=self.port, tor_port=self.tor.port)
		with open(self.CONFIG_PATH, 'w') as config_file:
			config_file.write(config)

	def run(self):
		if self._status == 1:
			self.stop()
			self.tor.run()
			cmd = '{privoxy} {config}'.format(privoxy=Privoxy.PRIVOXY_PATH, config=self.CONFIG_PATH)
			os.system(cmd)
			self._status = 2

	def stop(self):
		cmd = "kill $(ps -ax | grep privoxy | grep " + str(self.port) + " | awk '{print $1}')"
		os.system(cmd)
		self.tor.stop()
		self._status = 1
