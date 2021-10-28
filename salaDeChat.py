import socket
import threading
import os

s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM )
s.bind(("127.0.0.1", 5000))
print("\t\t\t====>  UDP CHAT APP  <=====")
print("==============================================")
nm = input("ENTER YOUR NAME : ")
print("\nType 'quit' to exit.")

ip, port = input("Enter IP address and Port number: ").split()

def send():
    while True:
        ms = input(">> ")
        if ms == "quit":
            os.exit(1)
        sm = "{}  : {}".format(nm,ms)
        s.sendto(sm.encode() , (ip,int(port)))

def rec():
    while True:
        msg = s.recvfrom(1024)
        print("\t\t\t\t >> " +  msg[0].decode()  )
        print(">> ")
x1 = threading.Thread( target = send )
x2 = threading.Thread( target = rec )

x1.start()
x2.start()
