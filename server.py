import socket
import threading

Host = input("Host: ")
Port = int(input("Port: "))

print('conectei')

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #que é a conexão que aceita UDP
server.bind((Host, Port)) #será a parte que executa a ligação entre o client e o server

clients = []
nomeDosUsuarios = []

def globalMessage(message):
    # utilizamos esse for para apartir da nossa lista de clients mandar a mensagem para todos os
    # clients conectados ao nosso servidor
    for client in clients:
        client.send(message)

def handleMessages(client):
    while True:
        try:
            mensagemRecebidaDoClient = client.recv(2048).decode('ascii')
            globalMessage(f'{nomeDosUsuarios[clients.index(client)]} -> {mensagemRecebidaDoClient}'.encode('ascii'))
        except:
            client_saiu = nomeDosUsuarios.index(client)
            client.close()
            clients.remove(client_saiu)
            nome_do_client_exit = nomeDosUsuarios[client_saiu]
            nomeDosUsuarios.remove(nome_do_client_exit)


def initconection():
    while True:
        client, address = server.recvfrom()
        print(f'Nova conexão: {address}')


initconection()

