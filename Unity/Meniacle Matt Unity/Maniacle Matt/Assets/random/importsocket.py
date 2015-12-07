import socket
import json
import time

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
	
#i = open('states.json', 'r')

x = 1.

while True:
	x = x+.005
	json_data = '{"players":{"7":{"btmac":"64:BC:0C:F9:0B:5B","tank":{"btmac":"98:D3:31:40:3F:45","health":10,"orientation":{"angular":{"a":1,"i":0,"j":0,"k":0},"linear":['+str(x)+',0,0]},"turret":{"orientation":{"angular":{"a":1,"i":0,"j":0,"k":0},"linear":[0,0,0]},"uuid":2,"weapon":{"ammo":0,"damage":0,"uuid":1,"variant":"DefaultWeapon"}},"uuid":8},"uuid":7}},"uuid":5,"variant":"LobbyState"}'
	send(json_data)
	time.sleep(1/60.0)

#while True:
#	pass