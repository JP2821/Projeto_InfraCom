import socket
import sys
import funcoes
import os

# Criando as variaveis do cabeçalho

host = 'localhost'
port = 5000
tamanho_do_pacote = 150
comprimento_servidor = 66

################ 66 porquê? #################
#                                           #
# 16 bytes para porta de origem             #
# 16 bytes para porta destino               #
# 16 bytes para comprimento total do pacote #
# 16 bytes para checksum                    #
# 1  byte para o número de sequência        #
# 1  byte para o ack                        #
#                                           #
# 16 + 16 + 16 + 16 + 1 + 1 = 66            #
#############################################

dados_recebidos = []
dados_recebidos_ordem = []
dados_duplicados = []
dados_corrompidos = []
dado = 0
i = 0

#Criando Sockets UDP
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('\nSocket criado com sucesso!')
except socket.error as msg:
    print('\nFalha ao criar o socket. Código do erro: ' + str(msg[0]) + '. Mensagem: ' + msg[1])
    sys.exit()

#Conectando o socket ao localhost e a porta definida
try:
    server.bind((host,port))
except socket.error as msg:
    print('\nBind falhou. Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
    sys.exit()
print('\nBind do Socket completo!')

#Aqui iremos fazer um contador de estados para saber se é a primeira vez que ele entra nesse estado
fist_time = 0

while 1:

    #Estado 0

    #Recebendo dados do cliente (dados, endereço)
    mensagem = server.recvfrom(tamanho_do_pacote)
    data = mensagem[0]
    address = mensagem[1]

    if not data:
        break

    i += 1
    os.system('clear')
    print("\n------------------------------------------")
    print("\tEnvio do", i, "º pacote")
    print("------------------------------------------")

    #Extraindo dados do pacote
    portaorigem = int(data[0:16], 2)
    portadestino = int(data[16:32], 2)
    comprimento = int(data[32:48], 2)
    checksum = int(data[48:64], 2)
    seq = int(data[64:65], 2)
    dadoanterior = dado
    dado = int(data[65:97], 2)

    soma = funcoes.checksum(portaorigem, portadestino, comprimento)

    if seq == 1:
        print("\nPacote [" + str(dadoanterior) + "] duplicado! Descartando e re-solicitando...")
        dados_duplicados.append(dadoanterior)

    if soma != checksum:
        print("\nPacote [" + str(dado) + "] com erro de bits! Descartando e re-solicitando...")
        dados_corrompidos.append(dado)
    while (seq == 1 or soma != checksum):
        if (fist_time == 1):

            msg = funcoes.cria_pacote_servidor(server.getsockname()[1], port, comprimento_servidor, 1, 0)

            try:
                #Enviadando ao cliente a mensagem de pacotes duplicados
                msg = msg.encode()
                server.sendto(msg, address)
            except socket.error as msg:
                print('Código do erro: ' + str(msg[0]) + '.Messagem: ' + msg[1])
                sys.exit()

        # Recebendo dados do cliente (dados, endereço)
        mensagem = server.recvfrom(tamanho_do_pacote)
        data = mensagem[0]
        address = mensagem[1]

        if not data:
            break

        # Extraindo dados do pacote
        portaorigem = int(data[0:16], 2)
        portadestino = int(data[16:32], 2)
        comprimento = int(data[32:48], 2)
        checksum = int(data[48:64], 2)
        seq = int(data[64:65], 2)
        dadoanterior = dado
        dado = int(data[65:97], 2)

        soma = funcoes.checksum(portaorigem, portadestino, comprimento)

    if (seq == 0 and soma == checksum):
        dados_recebidos.append(dado)
        dados_recebidos_ordem.append(dado)
        dados_recebidos_ordem.sort()
        print("\nPacote [" + str(dado) + "] recebido corretamente!")
        print("\nPacotes recebidos até o momento:")
        print(dados_recebidos)
        print("\nPacotes recebidos (em ordem):")
        print(dados_recebidos_ordem)
        print("\nPacotes duplicados:")
        print(dados_duplicados)
        print("\nPacotes corrompidos:")
        print(dados_corrompidos)

        msg = funcoes.cria_pacote_servidor(server.getsockname()[1], port, comprimento_servidor, 1, 0)

        try:
            # Enviando mensagem ao cliente
            msg = msg.encode()
            server.sendto(msg, address)
        except socket.error as msg:
            print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
            sys.exit()
        fist_time = 1

    #Estado 1
    # Recebendo dados do cliente (dados, endereço)
    mensagem = server.recvfrom(tamanho_do_pacote)
    data = mensagem[0]
    data = data.decode()
    address = mensagem[1]

    if not data:
        break

    # Extraindo dados do pacote
    portaorigem = int(data[0:16], 2)
    portadestino = int(data[16:32], 2)
    comprimento = int(data[32:48], 2)
    checksum = int(data[48:64], 2)
    seq = int(data[64:65], 2)
    dadoanterior = dado
    dado = int(data[65:97], 2)

    soma = funcoes.checksum(portaorigem, portadestino, comprimento)

    i += 1
    os.system('clear')
    print("\n------------------------------------------")
    print("\tEnvio do", i, "º pacote")
    print("------------------------------------------")

    if seq == 0:
        print("\nPacote [" + str(dadoanterior) + "] duplicado! Descartando e re-solicitando...")
        dados_duplicados.append(dadoanterior)
    if soma != checksum:
        print("\nPacote [" + str(dado) + "] com erro de bits! Descartando e re-solicitando...")
        dados_corrompidos.append(dado)
    while seq == 0 or soma != checksum:

        msg = funcoes.cria_pacote_servidor(server.getsockname()[1], port, comprimento_servidor, 1, 0)

        try:
            print("PORRAAAAAAAAAAAA!")
            msg = msg.encode()
            server.sendto(msg, address)
        except socket.error as msg:
            print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
            sys.exit()

        print("Cheguei")

        # Recebendo dados do cliente (dados,  endereço)
        mensagem = server.recvfrom(tamanho_do_pacote)
        print("Recebi")
        data = mensagem[0]
        data = data.decode()
        address = mensagem[1]

        if not data:
            break


        #Extraindo dados do pacote
        portaorigem = int(data[0:16], 2)
        portadestino = int(data[16:32], 2)
        comprimento = int(data[32:48], 2)
        checksum = int(data[48:64], 2)
        seq = int(data[64:65], 2)
        dadoanterior = dado
        dado = int(data[65:97], 2)

        soma = funcoes.checksum(portaorigem, portadestino, comprimento)

    if (seq == 0 and soma == checksum):
        dados_recebidos.append(dado)
        dados_recebidos_ordem.append(dado)
        dados_recebidos_ordem.sort()
        print("\nPacote [" + str(dado) + "] recebido corretamente!")
        print("\nPacotes recebidos até o momento:")
        print(dados_recebidos)
        print("\nPacotes recebidos (em ordem):")
        print(dados_recebidos_ordem)
        print("\nPacotes duplicados:")
        print(dados_duplicados)
        print("\nPacotes corrompidos:")
        print(dados_corrompidos)

        #print("sera ?")

        msg = funcoes.cria_pacote_servidor(server.getsockname()[1], port, comprimento_servidor, 1, 0)

        #print("Achei ?")

        try:
            # Enviando mensagem ao cliente
            msg = msg.encode()
            print("Teste")
            server.sendto(msg, address)
        except socket.error as msg:
            print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
            sys.exit()

server.close()