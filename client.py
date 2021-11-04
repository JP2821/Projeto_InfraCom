import socket
import threading

def Client():
    serverIP = input("Server IP: ")
    Port = int(input("Port: "))

    server = (serverIP, Port)

    conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conexao.connect((serverIP, Port))

    nick_name = str(input("Qual seu nickname: "))

    conexao.sendto(nick_name.encode(), server)

    while True:
        msg = input("-> ")
        if msg == 'bye':
            conexao.sendto(msg.encode(), server)
            client, endereco = conexao.recvfrom(1024)
            print("Recebida ->", str(client))
            conexao.close()
        else:
            conexao.sendto(msg.encode(), server)
            servidor, endereco = conexao.recvfrom(1024)
            print("Recebida ->", str(servidor))


if __name__ == '__main__':
    Client()