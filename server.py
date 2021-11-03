import socket
import time
import threading

def main():
    Host = str(input("Host: "))
    Port = int(input("Port: "))

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print('conectei')

    server.bind((Host, Port))

    clients = []
    usernames = []

    name = server.recvfrom(1024)



    while True:
        client, address = server.recvfrom(1024)
        print(f"conexão estabelecida [IP, Porta]: {address}")
        print("Mensagem recebida de", str(address))
        tempo = time.strftime('%H:%M:%S')
        print(f"{tempo} {name}:", str(client))

        server.sendto(client, address)

        if client == 'bye':
            print("[SERVE CLOSED]")
            server.close()



if __name__ == '__main__':
    main()
