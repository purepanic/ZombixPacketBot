from websocket import create_connection
import socket
import sys
import time
import json
#The game uses websockets, so I used a packet sniffer to find the address of the game websocket
#This code tricks the server into thinking I am logging into the app and loading my character and stuff
print("Login to app")
#When the app is opened it connects to this to fetch what the player looks like and stuff for the home page
ws = create_connection("ws://212.109.222.20:3003/socket.io/?EIO=4&transport=websocket")
print(ws.recv())
#Checks for updates (We dont use this but we need to send it to mock the app)
ws.send('42["checkUpdates",{"v":29}]')
print(ws.recv())
#Gets available servers that I can join
ws.send('42["getRatings",{"id":3}]')
print(ws.recv())
#Tells the server to log us into the homepage
ws.send('42["login",{"token":"AC924A667F51916616DAA43D27911712"}]')
print(ws.recv())
#This lets the game know that I am connecting to the US game servers
ws.send('42["connectToTheServer",{"id":3,"r":"US"}]')
print(ws.recv())
print(ws.recv())
print(ws.recv())
#print(ws.recv())
ws.send('41')
ws.send('1')
ws.close()
#Since we told the game we will be connecting to us servers, we go to their "redirect" server. It basically gives us the server that our player was last in / or we can query to travel to a new world. Its like a phone book but for server ips. or maybe google maps is a good metaphor
#Logging in here to ask to be authed for a certain area of the game
print("logging into base server")
ws = create_connection("ws://213.159.211.66:3006/socket.io/?EIO=4&transport=websocket")
ws.send('42["newPlayer",{"token":"AC924A667F51916616DAA43D27911712","lang":"EN","region":"US"}]')
ws.send('2')
ws.send('42["t",{"t":"gd"}]')
ws.send('42["sector",{"id":3,"region":"US"}]')
#ID corresponds to area I want to visit, will authenticate a connection to that port with my player token
while True:
	#Keep asking until we get a valid server address to connect to
	ws.send('42["t",{"t":"gd"}]')
    #Queries for the pvp world
	ws.send('42["sector",{"id":3,"region":"US"}]')
	info = ws.recv()
	print(info)
	region = "loc"
	if region in str(info):
		print("we got the server IP")
		break
ws.send('41')
ws.send('1')		
ws.close()
#I have been authed, now I am logged into the area
print("logging into area")
ws = create_connection("ws://5.34.178.94:3011/socket.io/?EIO=4&transport=websocket")
#This officially logs us into a region
ws.send('42["newPlayer",{"token":"AC924A667F51916616DAA43D27911712","lang":"EN","region":"US"}]')
#while True:
ws.send('42["t",{"t":"gd"}]')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(5.0)
addr = ("5.34.178.94", 3021)

#Open session to walking port
message = b'{"token":"AC924A667F51916616DAA43D27911712"}'
client_socket.sendto(message, addr)
message = b'{"token":"AC924A667F51916616DAA43D27911712"}'
client_socket.sendto(message, addr)
#message = b'948.18;945;1'
while True:
  #I don't know what this means, but when its sent it keeps the player logged in
  ws.send('42["t",{"t":"gd"}]')
  #log player data
  #print(ws.recv())
  try:
    #data = None
    data, server = client_socket.recvfrom(1024)
    #data = None
    #Log walking data
    #data = data[2:]
    #data = f'{data}'
    #data = str(data)
    data = data.decode("utf-8") 
    print(data)
    #datainfo = json.loads(data)
    #datainfo = datainfo["title"]
    #print(datainfo)
    data = None
  except socket.timeout:
    print('REQUEST TIMED OUT')
#Close the session (log off)    
ws.send('41')
ws.send('1')
ws.close()





print("Program finished.")


#Random crap:
#Send walk packet (super buggy)
  #message = b'948.18;945;1'
  #client_socket.sendto(message, addr)
  #time.sleep(3)
  #message = b'957.44;947.55;0'
  #client_socket.sendto(message, addr)
  #try:
    #data, server = client_socket.recvfrom(1024)
    #Log walking data
    #print(f'{data}')
  #except socket.timeout:
    #print('REQUEST TIMED OUT')
  
  #Drop a pistol
  #ws.send('42["t",{"t":"getInventory"}]')
  #ws.send('42["drop",{"s":100}]')