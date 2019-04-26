###############################################################################
# Project for PDS ( Data Communications, Computer Networks and Protocols )
# @file pds18-rpc.py (3)
# @author Michal Ormos (xormos00)
# @email xormos00@stud.fit.vutbr.cz
# @date April 2019
###############################################################################


import argparse
import socket
import sys
import time
import json

def getNetwork():
	allLines = []
	with open("network.dat","r") as f:
		for line in f:
			allLines.append(line)
		f.close()
	return allLines

def defineStep(args):
	network = getNetwork()
	if args.peer:
		if args.command == "message":
			print("peer message")
		elif args.command == "getlist":
			print("peer getlist")
			ip = False
			port = False
			for line in network:
				jsondata = json.loads(line)
				for item in jsondata:
					if item == "ip":
						ip = jsondata[item]
					if item == "port":
						port = jsondata[item]
					if (port and ip):		
						print("send to")
						print(ip, port)	
						sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
						server_address = (str(ip), int(port))
						message = b'GETLIST'
						try:
							print('sending {!r}'.format(message))
							sent = sock.sendto(message, server_address)
						finally:
							print('closing socket')
							sock.close()
						ip = False
						port = False								
		elif args.command == "peers":
			print("peer peers")            
		elif args.command == "reconnect":
			print("peer reconnect")   
		else:
			print("Unknow command for Peer")         
	elif args.node:
		if args.command == "database":
			print("node database")   
		elif args.command == "neighbors":
			print("node neighbors")                          
		elif args.command == "connect":
			print("node connect")     
		elif args.command == "disconnect":
			print("node disconnect")     
		elif args.command == "sync":
			print("node sync")                                         
		else:
			print("Unknow command for Node")         
	else:
		print("Error, unknow arguments")



parser = argparse.ArgumentParser(description="Hybrid p2p chat application RPC module")
group = parser.add_mutually_exclusive_group()
# command_group = parser.add_mutually_exclusive_group()
group.add_argument("--peer", action='store_true',  help="Command for instance of peer")
group.add_argument("--node", action='store_true', help="Command for instance of server")

parser.add_argument("--command",  help="Command for instance of server")

parser.add_argument("--from", help="Command for instance of server")
parser.add_argument("--to", help="Command for instance of server")
parser.add_argument("--message", help="Command for instance of server")

parser.add_argument("--reg-ipv4", help="Command for instance of server")
parser.add_argument("--reg-port", help="Command for instance of server")
# command_group.add_argument("getlist", help="Command for instance of server")
# command_group.add_argument("peers", help="Command for instance of server")
# command_group.add_argument("reconnect", help="Command for instance of server")
# command_group.add_argument("database", help="Command for instance of server")
# command_group.add_argument("neighbors", help="Command for instance of server")
# command_group.add_argument("connect", help="Command for instance of server")
# command_group.add_argument("discover", help="Command for instance of server")
# command_group.add_argument("sync", help="Command for instance of server")


args = parser.parse_args()
print(args)

defineStep(args)

# --peer --command message --from <username1> --to <username2> --message <zpráva>

"""




# ./pds18-rpc --id <identifikátor> <"--peer"|"--node"> --command <příkaz> --<parametr1> <hodnota_parametru1> ...
# --peer --command message --from <username1> --to <username2> --message <zpráva>, který se pokusí odeslat chat zprávu
# --peer --command getlist, který vynutí aktualizaci seznamu v síti známých peerů, tj. odešle zprávu GETLIST a nechá si ji potvrdit
# --peer --command peers, který zobrazí aktuální seznam peerů v síti, tj. peer si s node vymění zprávy GETLIST a LIST, přičemž obsah zprávy LIST vypíše
# --peer --command reconnect --reg-ipv4 <IP> --reg-port <port>, který se odpojí od současného registračního uzlu (nulové HELLO) a připojí se k uzlu specifikovaném v parametrech

# --node --command database, který zobrazí aktuální databázi peerů a jejich mapování
# --node --command neighbors, který zobrazí seznam aktuálních sousedů registračního uzlu
# --node --command connect --reg-ipv4 <IP> --reg-port <port>, který se pokusí navázat sousedství s novým registračním uzlem
# --node --command disconnect, který zruší sousedství se všemi uzly (stáhne z jejich DB své autoritativní záznamy) a odpojí node od sítě
# --node --command sync, která vynutí synchronizaci DB s uzly, se kterými node aktuálně sousedí



# python3 pds18-node.py --id 1 --reg-ipv4 127.0.0.1 --reg-port 3000

# import socket
# import sys
# import time

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# server_address = ('localhost', 9999)

# message = b'GETLIST'

# try:

#     # Send data
#     print('sending {!r}'.format(message))
#     sent = sock.sendto(message, server_address)

#     # Receive response
#     # print('waiting to receive')
#     # data, server = sock.recvfrom(4096)
#     # print('received {!r}'.format(data))

# finally:
#     print('closing socket')
#     sock.close()


# time.sleep(10)

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# server_address = ('127.0.0.1', 10999)

# message = b'MESSAGE'

# try:

#     # Send data
#     print('sending {!r}'.format(message))
#     sent = sock.sendto(message, server_address)

#     # Receive response
#     # print('waiting to receive')
#     # data, server = sock.recvfrom(4096)
#     # print('received {!r}'.format(data))

# finally:
#     print('closing socket')
#     sock.close()
"""