
# Wanna comunicate over internet? Use socket.
import socket
import threading
import sys
import time
# library for parsing arguments
import argparse
from random import randint

class Client:
		# method which is able to send message to the server
		def sendMsg(self, sock):
			# running in the background
			while True:
				sock.send(bytes(input(""), 'utf-8'))

		def __init__(self, address):
			print("Client running ...")
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

		def getPeersList(self, peerData):
			print(peerData)

class p2p:
	peers = ['127.0.0.1']

# while True:
parser = argparse.ArgumentParser(description="Hybrid p2p chat application PEER module")
parser.add_argument("--id", type=int, required=True, help="--id us unique identifier of peer instance for cases, where it is needed to differ between peer in case of oe host (OS), on which they are running")
parser.add_argument("--username", required=True, help="Unique username identifing this peer within the chat")
parser.add_argument("--chat-ipv4", required=True, help="IP address on which peer listening and receiving messages from other peers or nodes")
parser.add_argument("--chat-port", required=True, help="Port on which peer listening and receiving messages from other peers or nodes")
parser.add_argument("--reg-ipv4", required=True, help="IP address of egistration node, on which peer send messages HELLO and GETLIST")        
parser.add_argument("--reg-port", required=True, help="Port of egistration node, on which peer send messages HELLO and GETLIST")
args = parser.parse_args()
print(args)
	# try:
	# 	print("Trying to connect ...")
	# 	# between 1 to 5 seconds
	# 	time.sleep(randint(1,5))
	# 	for peer in p2p.peers:
	# 		try:
	# 			client = Client(peer)
	# 		except KeyboardInterrupt:
	# 			sys.exit(0)
	# 		except:
	# 			pass
	# except KeyboardInterrupt:
	# 	sys.exit(0)    


    # ./pds18-peer --id <identifikátor> --username <user> --chat-ipv4 <IP> --chat-port <port> --reg-ipv4 <IP> --reg-port <port>
