import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1" ,33333))



def send(msg):
	MSGLEN = len(msg)
	totalsent = 0
	while totalsent < MSGLEN:
		sent = s.send(msg[totalsent:])
		if sent == 0:
			raise RuntimeError("socket connection broken")
		totalsent = totalsent + sent
	
while True:
	i = raw_input()
	send(i)

