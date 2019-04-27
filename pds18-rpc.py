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
