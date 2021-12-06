import socket
import sys
import os
from threading import Thread
import time

def menu(array,index = 0):
    os.system('clear')
    print("\n----------------------------------------------")
    print("Lista de pacotes a serem enviados: ")
    print(array[index:len(array) - 1])
    print("\nOpções:")
    print("\n1 - Enviar próximo pacote")
    print("2 - Corromper envio do próximo pacote")
    print("3 - Duplicar envio do próximo pacote")
    
    print("5 - Sair\n")
    escolha = 0
    while (escolha < 1 or escolha > 5):
        escolha = int(input("Opção escolhida: "))
    return escolha

# Calculando o complemento de 1
def complemento_de_1(n, size):
    comp = n ^ ((1 << size) - 1)
    return '0b{0:0{1}b}'.format(comp, size)

# Soma de verificação
def checksum(porta_origem, porta_destino, comprimento):
    primera_soma = bin(porta_origem + porta_destino)[2:].zfill(16) # uso a função zfill para preencher com 0 a esquerda qual quer espaço que ficar sobrando
    if len(primera_soma) > 16:
        primera_soma = primera_soma[1:17]
        primera_soma = bin(int(primera_soma, 2) + 1)[2:].zfill(16)
    segunda_soma = bin(int(primera_soma, 2) + comprimento)[2:].zfill(16)
    if len(segunda_soma) > 16:
        segunda_soma = segunda_soma[1:17]
        segunda_soma = bin(int(segunda_soma, 2) + 1)[2:].zfill(16)
    checksum = complemento_de_1(int(segunda_soma, 2), 16)[2:]
    return int(checksum, 2)

# Função para criar o pacote do cliente
def cria_pacote_cliente(porta_origem, porta_destino, comprimento, soma, seq, dados):
    pacote = bin(porta_origem)[2:].zfill(16) + bin(porta_destino)[2:].zfill(16) + bin(comprimento)[2:].zfill(16) + bin(soma)[2:].zfill(16) + bin(seq)[2:].zfill(1) + bin(dados)[2:].zfill(32)
    return pacote

def cria_pacote_servidor(porta_origem, porta_destino, comprimento, ack, seq):
    soma = checksum(porta_origem, porta_destino, comprimento)
    pacote = bin(porta_origem)[2:].zfill(16) + bin(porta_destino)[2:].zfill(16) + bin(comprimento)[2:].zfill(16) + bin(ack)[2:].zfill(1) + bin(seq)[2:].zfill(1) + bin(soma)[2:].zfill(16)
    
    return pacote



# serve para servidor extrair dados enviados pelo cliente
def extrair_dados_servidor(data):
    portaorigem  = int(data[0:16], 2)
    portadestino = int(data[16:32], 2)
    comprimento  = int(data[32:48], 2)
    checksum     = int(data[48:64], 2)
    seq          = int(data[64:65], 2)
    dado         = int(data[65:97], 2)

    return portaorigem , portadestino, comprimento , checksum,   seq   , dado        

def extrair_dados_cliente(data):
    
    portaorigemservidor  = int(data[0:16], 2)
    portadestinoservidor = int(data[16:32], 2)
    comprimentoservidor  = int(data[32:48], 2)
    ackservidor          = int(data[48:49], 2)
    seqservidor          = int(data[49:50], 2)
    somaservidor         = int(data[50:66], 2)

    return portaorigemservidor , portadestinoservidor, comprimentoservidor , ackservidor  , seqservidor  , somaservidor  

def print_info_servidor(dado,dados_recebidos,dados_duplicados,dados_corrompidos):
    print("\nPacote [" + str(dado) + "] recebido corretamente!")
    print("\nPacotes recebidos até o momento:")
    print(dados_recebidos)
    print("\nPacotes duplicados:")
    print(dados_duplicados)
    print("\nPacotes corrompidos:")
    print(dados_corrompidos)     

# rotina de thread para enviar mensagem e
# poder ser terminada pela main
# ao ocorrer timeout do timer
def enviar_msg(client,msg,host,port): 

    while True:
        try: #Enviando o datagrama para o servidor
            msg = msg.encode()
            client.sendto(msg, (host, port))
            break
        except socket.error as msg:
            print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
            print("tentando novamente...")

#daemon thread para ouvir mensagens
def esperar_ack(*args):
    while True:
        client,tamanho_do_pacote,buffer = args
        # Recebendo a mensagem do servidor
        buffer[0],address = client.recvfrom(tamanho_do_pacote)

