from socket import *
import time


host ="localHost"
port = 50000
Socket = socket(AF_INET,SOCK_DGRAM)

addr = (host,port)
tam = 256 #tamanho do bloco de dados

def enviarquivo(nome_arquivo = "enviado.txt",
                Socket = socket(AF_INET,SOCK_DGRAM),
                address = ("localHost",50000),
                tam = 256,
                show=True):
    
    with  open (nome_arquivo, "rb") as file_enviado:

        blocoDados = file_enviado.read(tam)

        count = 0
        while(blocoDados):
            time.sleep(1) # dar tempo do receiver escrever no disco
            Socket.sendto(blocoDados,address)

            count += 1
            print('\nblock:',count)
            if show: print(str(blocoDados,'utf-8'))
            
            blocoDados = file_enviado.read(tam)
            
    Socket.sendto(b'stop',address) #avisa que terminou

    print('\nFIM')
    Socket.close()



if __name__ == '__main__':
    from receiver import recebarquivo

    enviarquivo (nome_arquivo =    "enviado.txt"   , address = addr) #avisa que terminou    
    print("##########Receber de volta##########")
    time.sleep(2)
    recebarquivo(nome_arquivo = "recebidevolta.txt", address = addr)    
    Socket.close()






