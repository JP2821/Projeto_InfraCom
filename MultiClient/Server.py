import socket
from threading import Thread

print("\t\t\t====>  UDP CHAT APP  <=====")
print("==============================================")
ip, port = "192.168.56.1",80
server = socket.socket(socket.AF_INET , socket.SOCK_DGRAM )
server.bind((ip, port))

clients = []




def accept_client(ClientName,ClientAdress):

    clients.append(ClientAdress)
    
    print("client:", ClientName,"connected")
    server.sendto("voce esta conectado".encode(),ClientAdress)



#envia mensagem para todo mundo
def Broadcast(msg,author):
    msg = ">>" + msg 
    print(msg)
    for ClientAdress in clients:
        if ClientAdress == author: continue
        server.sendto((msg).encode(),ClientAdress)


def Server():
    while True:
        mensagem,ClientAdress = server.recvfrom(1024)
        
        if "connection request" in mensagem.decode():
            accept_client(mensagem,ClientAdress)

        else:
            
            Broadcast(mensagem.decode(),ClientAdress)


    
    print("SERVER OFF")

if __name__ == "__main__":
    Server()
