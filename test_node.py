import socket
import sys
import argparse

class Server:

    def __init__(self):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the port
        server_address = (REG_IPV4, int(REG_PORT))
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)

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
