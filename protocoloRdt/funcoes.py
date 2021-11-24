import socket
import sys
import os

def menu(array):
    os.system('clear')
    print("\n----------------------------------------------")
    print("Lista de pacotes a serem enviados: ")
    print(array[0:len(array) - 1])
    print("\nOpções:")
    print("\n1 - Enviar próximo pacote")
    print("2 - Corromper envio do próximo pacote")
    print("3 - Duplicar envio do próximo pacote")
    print("4 - Embaralhar pacotes")
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