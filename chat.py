
# Wanna comunicate over internet? Use socket.
import socket
import threading

# Accessing socket library in socket method
# @param - we are going to use IP version 4
# @param - we have a TCP connection (udp = SOCK_DGRAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ip , port
sock.bind(('0.0.0.0', 10000))

# how many connections are allowed to listen
sock.listen(1)

connections = []

def handler(c,a):
	global connections
	while True:
		# we receiving data by connection and maximum data is
		data = c.recv(1024)
		# send to every client
		for connection in connections:
			connection.send(bytes(data))
		# way to quit loop
		if not data:
			connections.remove(c)
			c.close
			break

while True:
	# c - connection which socket return
	# a - connectio naddress which socket return
	c, a = sock.accept()
	# on every connection make unique thread so we can server multiply users
	cThread = threading.Thread(target=handler, args=(c,a))
	# we are able to close problem even threads are ongoing
	cThread.daemon = True
	cThread.start()
	connections.append(c)
	print(connections)