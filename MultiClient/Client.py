import socket
from threading import Thread


def writeMSG(server, conexao):
    while True:
        msg = input() 
        
        if msg == 'bye': return
           
        conexao.sendto(msg.encode(), server)
    

def receiveMSG(server,conexao):
    while True:
        msg, endereco = conexao.recvfrom(1024)
        msg= msg.decode('utf8')

        if msg == 'bye':
            conexao.sendto("closing connections".encode(), server)
            conexao.close()
        else:
            print(msg)


def Client():
   #serverIP = input("Server IP: ")
   #Port = int(input("Port: "))
    
    serverIP,Port = '192.168.56.1',50000

    server = (serverIP, Port)

    conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conexao.connect((serverIP, Port))

    nick_name = str(input("Qual seu nickname: "))
    connection_request = "connection request " + nick_name 
    
    print("enviando pedido de conexao:",connection_request)
    conexao.sendto(connection_request.encode(), server)
    print("status:",conexao.recvfrom(1024)[0].decode('utf8'))
    
    
    escrever = Thread(target=writeMSG,args = (server,conexao))
    
    ouvir = Thread(target = receiveMSG,args = (server,conexao))

    ouvir.start()
    escrever.start()

    escrever.join()
    conexao.close()


if __name__ ==  '__main__':
    Client()