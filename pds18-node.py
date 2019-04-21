###############################################################################
# Project for PDS ( Data Communications, Computer Networks and Protocols )
# @file pds18-node.py (3)
# @author Michal Ormos (xormos00)
# @email xormos00@stud.fit.vutbr.cz
# @date April 2019
###############################################################################

# Compatible with PDS Virtual machine
# Socket for easy establishing communication between two points
import socket
# Threading for making more instancies easilt
import threading
# System calls
import sys
# Getting time
import time
# Parsing arguments
import argparse
# Creating random stream of numbers
from random import randint
import json

# @TODO bencoding not allow
import yabencode

class Server:
	connections = []
	peers = []
	db = []
	#create constructor
	def __init__(self):
		# Accessing socket library in socket method
		# @param - we are going to use IP version 4
		# @param - we have a TCP connection (udp = SOCK_DGRAM)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# ip , port
		sock.bind((REG_IPV4, int(REG_PORT)))
		# how many connections are allowed to listen
		sock.listen(1)
		print("Server running ...")

		while True:
			# c - connection which socket return
			# a - connectio naddress which socket return
			c, a = sock.accept()
			print("log1")
			print(a)
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
			print("============= CONNECTIONS ==============")
			print(self.connections)
			print("============= PEERS ==============")
			print(self.peers)
			print("============= DB ==============")
			print(self.db)
			print("=================================================")
			if data == b'GETLIST':
				print(str(a[0]) + ':' + str(a[1]))
				print("Is asking List of peers")
			else:
				bdeccoded = yabencode.decode(data)
				for key in bdeccoded:
					if key == "type":
						if bdeccoded[key].decode("utf-8") == "hello":
							self.checkPeer(bdeccoded)
							break
			# send to every client
			for connection in self.connections:
				connection.send(bytes(data))
				# if data == b'GETLIST':
				# 	connection.send(self.peers.encode)
				# else:
				# 	connection.send(data)
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
			# if data:
			# 	if data == b'GETLIST':
			# 		self.sendListToPeer()

	def checkPeer(self, data):
		timestamp = time.time()
		dbCopy = self.db
		data.update({"time": timestamp})
		peerID = 0
		found = False
		for key in data:
			if key == "txid":
				peerID = data[key]
				break
		# First entry to database
		if not dbCopy:
			found = True
			dbCopy.append(data)
		# Check if entry is not already in database
		# if so just rewrite timestamp
		# if not add to db
		else:
			for peer in dbCopy:
				line = peer
				for entry in line:
					if entry == 'txid':
						if line[entry] == peerID:
						# self.db.append(data)
							found = True
							break
		if found == False:
			dbCopy.append(data)							
		self.db = dbCopy


	def sendPeers(self):
		p = ""
		for peer in self.peers:
			p = p + peer + ","

			for connection in self.connections:
				connection.send(b'\x11' + bytes(p, "utf-8"))

	# def sendListToPeer(self):


	def printit(self):
		# threading.Timer(5.0, self.printit).start()
		print("List of peers connected: ")
		print(self.peers)

class p2p:
	peers = ['127.0.0.1']

while True:
	parser = argparse.ArgumentParser(description="Hybrid p2p chat application NODE module")
	parser.add_argument("--id", type=int, required=True, help="--id us unique identifier of node instance for cases, where it is needed to differ between peer in case of oe host (OS), on which they are running")
	parser.add_argument("--reg-ipv4", required=True, help="IP address on which node listening and receiving messages from other peers or nodes")
	parser.add_argument("--reg-port", required=True, help="Port on which node listening and receiving messages from other peers or nodes")
	args = parser.parse_args()
	ID = str(args.id)
	REG_IPV4 = str(args.reg_ipv4)
	REG_PORT = str(args.reg_port)
	try:
		print("Trying to connect ...")
		# between 1 to 5 seconds
		# time.sleep(randint(1,5))
		# for peer in p2p.peers:
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

    # ./pds18-node --id <identifikátor> --reg-ipv4 <IP> --reg-port <port>
