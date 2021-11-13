import socket
from threading import Thread

print("\t\t\t====>  UDP CHAT APP  <=====")
print("==============================================")
ip, port = "192.168.56.1",50000
server = socket.socket(socket.AF_INET , socket.SOCK_DGRAM )
server.bind((ip, port))

clients = []
client_name = {}



def accept_client(ClientName,ClientAdress):

    ClientName = str(ClientName).split(' ')[2][:-1]
    clients.append(ClientAdress)
    client_name[ClientAdress] = ClientName
    print("client:", ClientName,"connected")
    server.sendto("voce esta conectado".encode(),ClientAdress)



#envia mensagem para todo mundo
def Broadcast(msg,author):
    msg = '\n' + client_name[author] + "\n>>"+ msg 
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
