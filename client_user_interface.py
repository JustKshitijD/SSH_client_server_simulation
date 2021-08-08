# Import socket module
import socket

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 12360

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# receive data from the server
while True:
    val = input()
    #print(val)
    val2=val.encode()
    s.send(val2)
    y=s.recv(1024)
    y=y.decode()
    print(y)                             # y="DONE"
    #print (s.recv(1024) )
# close the connection
s.close()
