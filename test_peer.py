import socket
import sys
import argparse
import time
import json
import yabencode
import threading
import os

TXID = 1
TXID_LOCK = threading.Lock()
def next_id():
	global TXID
	with TXID_LOCK:
		result = TXID
		TXID += 1
	return result

class Client:
		
	def RPCHandler(self):
		RPCid = self.findRPCPort()
		# Create a UDP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Bind the socket to the port
		server_address = (CHAT_IPV4, int(RPCid))
		print('Client listening for RPC {} port {}'.format(*server_address))
		sock.bind(server_address)        
		while True:
			print("listening")
			# we receiving data by connection and maximum data is
			data, address = sock.recvfrom(4096)
			print(data)
			if data == b'MESSAGE':
				print("call message")
				# self.sendMessage("a")  
			elif data == b'GETLIST':
				print("call getlist")
				self.sendGetList()
			elif data == b'PEERS':
				print("call peers")
			elif data == b'RECONNECT':  
				print("call reconnect")

	def prepareData(self):
		next_id()
		data = {
			"type": "hello",
			"txid": TXID,
			"username": (USERNAME),
			"ipv4": str(CHAT_IPV4),
			"port": int(CHAT_PORT)
		}
		return data

	def sendHello(self):
		helloTime = time.time()
					
		firstHello = True
		while True:
			if (time.time() - helloTime) > 10 or firstHello:
				# Create a UDP socket
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

				server_address = (REG_IPV4, int(REG_PORT))      

				firstHello = False
				data = self.prepareData()
				bencoded = yabencode.encode(data)
				print(bencoded)
				try:

					# Send data
					print('sending {!r}'.format(bencoded))
					sent = sock.sendto(bencoded, server_address)
					# Receive response
					# print('waiting to receive')
					# data, server = sock.recvfrom(4096)
					# print('received {!r}'.format(data))

				finally:
					print('closing socket')
					sock.close()
				helloTime = time.time() 

	def sendMessage(self, toUser):
		# Create a UDP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		server_address = (REG_IPV4, int(REG_PORT))

		data = {
			"type":"message",
			"txid": TXID,
			"from": str(USERNAME),
			"to":"<string>",
			"message":"<string>"
		}
			   
		while True:
			bencoded = yabencode.encode(data)
			try:
				# Send data
				print('sending {!r}'.format(bencoded))
				sent = sock.sendto(bencoded, server_address)

				# Receive response
				print('waiting to receive')
				data, server = sock.recvfrom(4096)
				print('received {!r}'.format(data))

			finally:
				print('closing socket')
				sock.close()

	def sendGetList(self):
		# Create a UDP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		server_address = (REG_IPV4, int(REG_PORT))

		data = {
			"type":"getlist", 
			"txid": TXID
		}
			   
		while True:
			bencoded = yabencode.encode(data)
			try:
				# Send data
				print('sending {!r}'.format(bencoded))
				sent = sock.sendto(bencoded, server_address)

				# Receive response
				print('waiting to receive')
				data, server = sock.recvfrom(4096)
				print('received {!r}'.format(data))

			finally:
				print('closing socket')
				sock.close()
			return

	"""
	Port for communication with RPC is generated as id with 9's until length is 5
	"""
	def findRPCPort(self):
		if(len(str(ID)) == 1):
			RPCid = ID + "999"
		if(len(str(ID)) == 2):
			RPCid = ID + "999"
		if(len(str(ID)) == 3):
			RPCid = ID + "99"
		if(len(str(ID)) == 4):
			RPCid = ID + "9"                                           
		return RPCid

	def __init__(self):

		# Start RPC daemon for listening to his messages
		RPCThread = threading.Thread(target=self.RPCHandler, args=())
		RPCThread.daemon = True
		RPCThread.start()

		helloThread = threading.Thread(target=self.sendHello, args=())
		helloThread.daemon = True
		helloThread.start()        

		# Create a UDP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Bind the socket to the port
		server_address = (CHAT_IPV4, int(CHAT_PORT))
		print('starting up on {} port {}'.format(*server_address))
		sock.bind(server_address)

		# Get some time variable out of while loop
		helloTime = time.time()

		while True:       
			print('\nwaiting to receive message')
			data, address = sock.recvfrom(4096)
			print('received {} bytes from {}'.format(
				len(data), address))
			print(data)
			print("aaaa")

			# if data == :
			#     sent = sock.sendto(data, address)
			#     print('sent {} bytes back to {}'.format(
			#         sent, address))

def checkwhoIAm(action, data):
	print("[INFO] checkwhoIam")
	weGotUserName = False
	weGotId = False
	allLines = []
	lineToRemove = ""
	if os.path.exists("network.dat"):
		with open("network.dat","r") as f:
			for line in f:
				allLines.append(line)
				print(line)
				jsondata = json.loads(line)
				for item in jsondata:
					if item == "username":
						if jsondata[item] == USERNAME:
							weGotUserName = True
							lineToRemove = line
					if item == "id":
						print(jsondata[item])
						print(ID)
						if jsondata[item] == int(ID):
							weGotId = True
		f.close()
		if(action == "add"):
			with open("network.dat","a") as f:
				if (weGotUserName == False and weGotId == False):
					f.write(json.dumps(data))
					f.write("\n")
			f.close()
		elif(action == "remove"):
			with open("network.dat","w") as f:
				counter = 1
				print(len(allLines))
				for line in allLines:
					if line != lineToRemove:
						f.write(line)
						print(counter)
						if (counter != len(allLines)-1):
							f.write("\n")
							counter += 1
			f.close()	
	else:
		with open("network.dat","w") as f:
			f.write(json.dumps(data))
			f.write("\n")
			f.close()			



def findRPCPort():
	if(len(str(ID)) == 1):
		RPCid = ID + "999"
	if(len(str(ID)) == 2):
		RPCid = ID + "999"
	if(len(str(ID)) == 3):
		RPCid = ID + "99"
	if(len(str(ID)) == 4):
		RPCid = ID + "9"                                           
	return RPCid
# while True:
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
whoIAm = {
	"type": "peer",	
	"username": str(USERNAME),
	"id": int(ID),
	"ip": str(CHAT_IPV4),
	"port": int(findRPCPort())
}	
checkwhoIAm("add", whoIAm)
try:
	print("Trying to connect ...")
	# between 1 to 5 seconds
	# time.sleep(randint(1,5))
	# for peer in p2p.peers:
	try:
		client = Client()
		# clientPeer = clientPeer(peer)
	except KeyboardInterrupt:
		checkwhoIAm("remove", whoIAm)
		sys.exit(0)
	except:
		pass				
except KeyboardInterrupt:
	checkwhoIAm("remove", whoIAm)
	sys.exit(0)        