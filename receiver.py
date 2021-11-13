from socket import *
import time

host="localHost"
port = 50000
Socket = socket(AF_INET,SOCK_DGRAM)

addr = (host,port)

def recebarquivo(nome_arquivo = "recebido.txt",
                Socket = socket(AF_INET,SOCK_DGRAM), 
                address = ("0.0.0.0",50000),
                tam = 256,
                show = True):
    
    while True:
        try:
            Socket.bind(address)
            break
        except:
            continue

    with open(nome_arquivo,'wb') as file_recebido:
        blocoDados,addr = Socket.recvfrom(tam)

        count = 0
        while(blocoDados):
            count += 1
            print('\nblock:',count) #bloco de 256 bytes
            file_recebido.write(blocoDados) #escreve no arquivo
            if show: print(str(blocoDados,'utf-8'))
            
            Socket.settimeout(2)  #terminar a conexao

            blocoDados,addr = Socket.recvfrom(tam)

            if(blocoDados == b'stop'):
                print(
                "\n\n####################### STOP recebido #######################\n"
                )
                break

    print('terminou de receber')
    Socket.close()

    



if __name__ == '__main__':
    from sender import enviarquivo

    recebarquivo(nome_arquivo =    "recebido.txt"  , address = addr)    
    print("##########Reenviando##########")
    time.sleep(2)
    enviarquivo( nome_arquivo = "recebido.txt", address = addr)    #reenviar
    Socket.close()