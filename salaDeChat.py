import socket
import time
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
        tempo = time.strftime('%H:%M:%S')
        ms = input(">> ")
        if ms == "bye":
            sm = "{} {}  : {}".format(tempo, nm, ms)
            s.sendto(sm.encode(), (ip, int(port)))
            fechar_conexao()
        sm = "{} {}  : {}".format(tempo,nm,ms)
        s.sendto(sm.encode(), (ip, int(port)))

def rec():
    while True:
        msg = s.recvfrom(1024)
        print("\t\t\t\t >> " +  msg[0].decode()  )
        print(">> ")
x1 = threading.Thread( target = send )
x2 = threading.Thread( target = rec )

def fechar_conexao():
    s.close()

x1.start()
x2.start()
