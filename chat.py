
# Wanna comunicate over internet? Use socket.
import socket
import threading
import sys
import time
from random import randint

class Server:
	connections = []
	peers = []
	#create constructor
	def __init__(self):
		# Accessing socket library in socket method
		# @param - we are going to use IP version 4
		# @param - we have a TCP connection (udp = SOCK_DGRAM)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# ip , port
		sock.bind(('0.0.0.0', 10000))
		# how many connections are allowed to listen
		sock.listen(1)
		print("Server running ...")

		while True:
			# c - connection which socket return
			# a - connectio naddress which socket return
			c, a = sock.accept()
			# on every connection make unique thread so we can server multiply users
			cThread = threading.Thread(target=self.handler, args=(c,a))
			# we are able to close problem even threads are ongoing
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			# add peer to peers list when someone connects
			self.peers.append(a[0])
			# print who was connected
			print(str(a[0]) + ':' + str(a[1]), "connected")		
			self.sendPeers()

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
				# remove peer from peers list when someone disconnects
				self.peers.remove(a[0])
				c.close
				# when someone disconnect update the list of connected peers
				self.sendPeers()
				break

	def sendPeers(self):
		p = ""
		for peer in self.peers:
			p = p + peer + ","

			for connection in self.connections:
				connection.send(b'\x11' + bytes(p, "utf-8"))

class Client:
		# method which is able to send message to the server
		def sendMsg(self, sock):
			# running in the background
			while True:
				sock.send(bytes(input(""), 'utf-8'))

		def __init__(self, address):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			#connect to socket
			sock.connect((address, 10000))

			# we can receive and send in same time so threads
			iThread = threading.Thread(target=self.sendMsg, args=(sock,))
			iThread.daemon = True
			iThread.start()

			#sending messages
			while True:
				data = sock.recv(1024)
				if not data:
					break
				#if first byte of the data then we receive list of peers
				if data[0:1] == b'\x11':
					# update th peers list minus first byte
					self.updatePeers(data[1:])
					print("got peers")
				else:
					print(str(data, 'utf-8'))

		def updatePeers(self, peerData):
			# go from the start of the list to the second last item
			p2p.peers = str(peerData, "utf-8").split(",")[:-1]

class p2p:
	peers = ['127.0.0.1']

# instance server
# first argument name of file second is IP address
# if (len(sys.argv) > 1):
# 	client = Client(sys.argv[1])
# else:
# 	server = Server()

while True:
	try:
		print("Trying to connect ...")
		# between 1 to 5 seconds
		time.sleep(randint(1,5))
		for peer in p2p.peers:
			try:
				client = Client(peer)
			except KeyboardInterrupt:
				sys.exit(0)
			except:
				pass
			# Problem of every client to become server
			# 1 to 20 chance that client will become a server
			# if randint(1, 20) == 1: 
			try:
				server = Server()
			except KeyboardInterrupt:
				sys.exit(0)
			except Exception as e:
				print(e)
	except KeyboardInterrupt:
		sys.exit(0)