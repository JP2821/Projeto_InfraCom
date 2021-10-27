import socket
import threading

serverIP= input("Server IP: ")
Port = int(input("Port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client.connect((serverIP, Port))
except:
    print(f"Reveja os seus dados: {serverIP}:{Port}")
