###############################################################################
# Project for PDS ( Data Communications, Computer Networks and Protocols )
# @file pds18-peer.py (3)
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
# working with json
import json
import os
# @TODO bencoding not allow
import yabencode

import select

class Client:
		# method which is able to send message to the server
		def sendMsg(self, sock):
			# running in the background
			helloTime = time.time()
			listTime = time.time()
			while True:
				# threading.Timer(10.0, self.sendMsg(sock)).start()
				if (time.time() - helloTime) > 10:
					myID = str(id)
					data = {
						"type": "hello",
						"txid": int(ID),
						"username": str(USERNAME),
						"ipv4": str(CHAT_IPV4),
						"port": int(CHAT_PORT)
					}	
					bencoded = yabencode.encode(data)
					sock.send(bencoded)
					helloTime = time.time()
				elif (time.time() - listTime) > 30:
					listTime = time.time()
					sock.send(bytes("GETLIST", 'utf-8'))
				# data = self.sendHello()
				# print("sendMsg")
				# if data:
				# 	sock.send(bytes("hello", 'utf-8'))
				# if (input("")):
				# 	sock.send(bytes(input(""), 'utf-8'))
				# sock.send(bytes("a", 'utf-8'))


		def __init__(self, address):
			# Establish connection with server
			print("Client running ...")
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			#connect to socket
			sock.connect((REG_IPV4, int(REG_PORT)))                  
			# we can receive and send in same time so threads
			iThread = threading.Thread(target=self.sendMsg, args=(sock,))
			iThread.daemon = True
			iThread.start()
		
			iThread2 = threading.Thread(target=self.listener, args=())
			iThread2.daemon = True
			iThread2.start()
		
			# # Wait for other client trying to connect with me
			# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			# # ip , port
			# sock.bind((CHAT_IPV4, int(CHAT_PORT)))
			# # how many connections are allowed to listen
			# sock.listen(1)
			# print("Cliest is listenning ...")					

			# while True:
			# 	# c - connection which socket return
			# 	# a - connectio naddress which socket return
			# 	c, a = sock.accept()
			# 	print("log1")
			# 	# self.checkPeerHelloInterval()
			# 	print(a)
			# 	# on every connection make unique thread so we can server multiply users
			# 	cThread = threading.Thread(target=self.handler, args=(c,a))
			# 	# we are able to close problem even threads are ongoing
			# 	cThread.daemon = True
			# 	cThread.start()
			# 	# self.connections.append(c)
			# 	# add peer to peers list when someone connects
			# 	# self.peers.append(a[1])
			# 	# print who was connected
			# 	print(str(a[0]) + ':' + str(a[1]), "connected")		
			# 	# self.sendPeers()

			#sending messages
			while True:
				data = sock.recv(1024)
				if not data:
					# print("[LOG] If 1")
					break
				#if first byte of the data then we receive list of peers
				# if data[0:1] == b'\x11':
				# 	# print("[LOG] If 2")
				# 	# update th peers list minus first byte
				# 	self.updatePeers(data[1:])
				# 	# print("got peers")
				else:
					# print("[LOG] If 3")
					print(str(data, 'utf-8'))
					# print("======")

		# def handler(self, c, a):
		# 	while True:
		# 		# we receiving data by connection and maximum data is
		# 		data = c.recv(1024)
		# 		print(data)

		# def updatePeers(self, peerData):
		# 	# go from the start of the list to the second last item
		# 	p2p.peers = str(peerData, "utf-8").split(",")[:-1]

		# def getPeersList(self, peerData):
			# print(peerData)

		# def sendHello(self):
		# 	threading.Timer(10.0, self.sendHello).start()
		# 	data = {
		# 		"type": "hello",
		# 		"txid": "10",
		# 		"username": "ormi",
		# 		"ipv4": "127.0.0.1",
		# 		"port": "3010",
		# 	}
		# 	return data

		def sendGetList(self):
			# threading.Timer(10.0, self.sendHello).start()
			data = {
				"type": "getlist",
				"txid": "10",
			}
			self.sendMsg(data)		

		def listener(self):
			# Wait for other client trying to connect with me
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			# ip , port
			sock.bind((CHAT_IPV4, int(CHAT_PORT)))
			# how many connections are allowed to listen
			sock.listen(1)
			print("Cliest is listenning ...")					

			while True:
				# c - connection which socket return
				# a - connectio naddress which socket return
				c, a = sock.accept()
				print("log1")
				# self.checkPeerHelloInterval()
				print(a)
				# on every connection make unique thread so we can server multiply users
				cThread = threading.Thread(target=self.handler, args=(c,a))
				# we are able to close problem even threads are ongoing
				cThread.daemon = True
				cThread.start()
				# self.connections.append(c)
				# add peer to peers list when someone connects
				# self.peers.append(a[1])
				# print who was connected
				print(str(a[0]) + ':' + str(a[1]), "connected")		
				# self.sendPeers()

		def handler(self, c, a):
			while True:
				# we receiving data by connection and maximum data is
				data = c.recv(1024)
				print(data)
				if not data:
					c.close
					break				

# class p2p:
# 	peers = ['127.0.0.1']

while True:
	parser = argparse.ArgumentParser(description="Hybrid p2p chat application PEER module")
	parser.add_argument("--id", type=int, required=True, help="--id us unique identifier of peer instance for cases, where it is needed to differ between peer in case of oe host (OS), on which they are running")
	parser.add_argument("--username", required=True, help="Unique username identifing this peer within the chat")
	parser.add_argument("--chat-ipv4", required=True, help="IP address on which peer listening and receiving messages from other peers or nodes")
	parser.add_argument("--chat-port", required=True, help="Port on which peer listening and receiving messages from other peers or nodes")
	parser.add_argument("--reg-ipv4", required=True, help="IP address of egistration node, on which peer send messages HELLO and GETLIST")        
	parser.add_argument("--reg-port", required=True, help="Port of egistration node, on which peer send messages HELLO and GETLIST")
	args = parser.parse_args()
	ID = str(args.id)
	USERNAME = str(args.username)
	CHAT_IPV4 = str(args.chat_ipv4)
	CHAT_PORT = str(args.chat_port)
	REG_IPV4 = str(args.reg_ipv4)
	REG_PORT = str(args.reg_port)
	try:
		print("Trying to connect ...")
		# between 1 to 5 seconds
		# time.sleep(randint(1,5))
		# for peer in p2p.peers:
		try:
			client = Client(REG_IPV4)
			# clientPeer = clientPeer(peer)
		except KeyboardInterrupt:
			sys.exit(0)
		except:
			pass				
	except KeyboardInterrupt:
		sys.exit(0)    


    # ./pds18-peer --id <identifikátor> --username <user> --chat-ipv4 <IP> --chat-port <port> --reg-ipv4 <IP> --reg-port <port>

# python3 pds18-peer.py --id 10 --username user1 --chat-ipv4 127.0.0.10 --chat-port 3010 --reg-ipv4 127.0.0.1 --reg-port 3000
