import socket
import sys
import argparse
import time
import json
import yabencode
import threading

class Client:

    def RPCHandler(self):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the port
        server_address = ('localhost', 9999)
        print('Client listening for RPC {} port {}'.format(*server_address))
        sock.bind(server_address)        
        while True:
            # we receiving data by connection and maximum data is
            data, address = sock.recvfrom(4096)
            print(data)
            if data == b'SEND':
                print("call send")
                self.sendMsg()            

    def sendMsg(self):
        # Create a UDP socket
        print("eh")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        server_address = (REG_IPV4, int(REG_PORT))

        data = {
            "type": "hello",
            "txid": int(ID),
            "username": str(USERNAME),
            "ipv4": str(CHAT_IPV4),
            "port": int(CHAT_PORT)
        }	        
        bencoded = yabencode.encode(data)
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

    def __init__(self):

        # FOR RPC
        cThread = threading.Thread(target=self.RPCHandler, args=())
        # we are able to close problem even threads are ongoing
        cThread.daemon = True
        cThread.start()

        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the port
        server_address = (CHAT_IPV4, int(CHAT_PORT))
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)

        helloTime = time.time()
        firstsHello = False
        self.sendMsg()

        while True:       
            print('\nwaiting to receive message')
            data, address = sock.recvfrom(4096)
            print('received {} bytes from {}'.format(
                len(data), address))
            print(data)
            # if data:
            #     sent = sock.sendto(data, address)
            #     print('sent {} bytes back to {}'.format(
            #         sent, address))


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
			client = Client()
			# clientPeer = clientPeer(peer)
		except KeyboardInterrupt:
			sys.exit(0)
		except:
			pass				
	except KeyboardInterrupt:
		sys.exit(0)        