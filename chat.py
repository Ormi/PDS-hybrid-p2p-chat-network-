
# Wanna comunicate over internet? Use socket.
import socket
import threading
import sys

class Server:
	# Accessing socket library in socket method
	# @param - we are going to use IP version 4
	# @param - we have a TCP connection (udp = SOCK_DGRAM)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	#create constructor
	def __init__(self):
		# ip , port
		self.sock.bind(('0.0.0.0', 10000))
		# how many connections are allowed to listen
		self.sock.listen(1)

	def handler(self, c, a):
		global connections
		while True:
			# we receiving data by connection and maximum data is
			data = c.recv(1024)
			# send to every client
			for connection in self.connections:
				# connection.send(bytes(data))
				connection.send(data)
			# way to quit loop
			if not data:
				print(str(a[0]) + ':' + str(a[1]), "disconnected")
				self.connections.remove(c)
				c.close
				break
	def run(self):
		while True:
			# c - connection which socket return
			# a - connectio naddress which socket return
			c, a = self.sock.accept()
			# on every connection make unique thread so we can server multiply users
			cThread = threading.Thread(target=self.handler, args=(c,a))
			# we are able to close problem even threads are ongoing
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			# print who was connected
			print(str(a[0]) + ':' + str(a[1]), "connected")

class Client:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# method which is able to send message to the server
		def sendMsg(self):
			# running in the background
			while True:
				self.sock.send(bytes(input(""), 'utf-8'))
		def __init__(self, address):
			#connect to socket
			self.sock.connect((address, 10000))

			# we can receive and send in same time so threads
			iThread = threading.Thread(target=self.sendMsg)
			iThread.daemon = True
			iThread.start()

			#sending messages
			while True:
				data = self.sock.recv(1024)
				if not data:
					break
				print(str(data, 'utf-8'))

# instance server
# first argument name of file second is IP address
if (len(sys.argv) > 1):
	client = Client(sys.argv[1])
else:
	server = Server()
	server.run()