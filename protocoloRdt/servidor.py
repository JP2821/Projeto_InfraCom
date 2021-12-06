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

dados_duplicados = []
dados_corrompidos = []
dado = 0
i = 0

# Criando Sockets UDP
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('\nSocket criado com sucesso!')
except socket.error as msg:
    print('\nFalha ao criar o socket. Código do erro: ' + str(msg[0]) + '. Mensagem: ' + msg[1])
    sys.exit()

# Conectando o socket ao localhost e a porta definida
try:
    server.bind((host, port))
except socket.error as msg:
    print('\nBind falhou. Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
    sys.exit()
print('\nBind do Socket completo!')

# Aqui iremos fazer um contador de estados
# para saber se é a primeira vez que ele entra nesse estado
fist_time = 0

while 1:

    # Estado 0

    # Recebendo dados do cliente (dados, endereço)
    data, address = server.recvfrom(tamanho_do_pacote)

    if not data:
        break

    i += 1
    os.system('clear')
    print("\n------------------------------------------")
    print("\tEnvio do", i, "º pacote")
    print("------------------------------------------")

    dadoanterior = dado
    portaorigem, portadestino, comprimento, checksum, seq, dado = funcoes.extrair_dados_servidor(data)

    soma = funcoes.checksum(portaorigem, portadestino, comprimento)

    if seq == 1:
        print("\nPacote [" + str(dadoanterior) + "] duplicado! Descartando e re-solicitando...")
        dados_duplicados.append(dadoanterior)

    if soma != checksum:
        print("\nPacote [" + str(dado) + "] com erro de bits! Descartando e re-solicitando...")
        dados_corrompidos.append(dado)

    while (seq == 1 or soma != checksum):
        if (fist_time == 1):

            msg = funcoes.cria_pacote_servidor(server.getsockname()[1], port, comprimento_servidor, 1, 1)

            try:
                funcoes.print_info_servidor(dado, dados_recebidos, dados_duplicados, dados_corrompidos)
                # Enviando ao cliente a mensagem de pacotes duplicados
                server.sendto(msg, address)
                print('cheguei bb')
            except socket.error as msg:
                print('Código do erro: ' + str(msg[0]) + '.Messagem: ' + msg[1])
                sys.exit()

        # Recebendo dados do cliente (dados, endereço)
        data, address = server.recvfrom(tamanho_do_pacote)

        if not data:
            break

        # Extraindo dados do pacote
        dadoanterior = dado
        portaorigem, portadestino, comprimento, checksum, seq, dado = funcoes.extrair_dados_servidor(data)

        soma = funcoes.checksum(portaorigem, portadestino, comprimento)

    if (seq == 0 and soma == checksum):
        dados_recebidos.append(dado)

        funcoes.print_info_servidor(dado, dados_recebidos, dados_duplicados, dados_corrompidos)

        msg = funcoes.cria_pacote_servidor(server.getsockname()[1], port, comprimento_servidor, 1, 0)

        try:
            # Enviando mensagem ao cliente
            server.sendto(msg, address)
        except socket.error as msg:
            print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
            sys.exit()
        fist_time = 1

    # Estado 1
    # Recebendo dados do cliente (dados, endereço)
    data, address = server.recvfrom(tamanho_do_pacote)
    data = data.decode()

    if not data:
        break

    # Extraindo dados do pacote
    dadoanterior = dado
    portaorigem, portadestino, comprimento, checksum, seq, dado = funcoes.extrair_dados_servidor(data)

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
            server.sendto(msg, address)
        except socket.error as msg:
            print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
            sys.exit()

        # Recebendo dados do cliente (dados,  endereço)
        data, address = server.recvfrom(tamanho_do_pacote)

        if not data:
            break

        # Extraindo dados do pacote
        dadoanterior = dado
        portaorigem, portadestino, comprimento, checksum, seq, dado = funcoes.extrair_dados_servidor(data)
        soma = funcoes.checksum(portaorigem, portadestino, comprimento)

    if (seq == 1 and soma == checksum):
        dados_recebidos.append(dado)

        funcoes.print_info_servidor(dado, dados_recebidos, dados_duplicados, dados_corrompidos)

        msg = funcoes.cria_pacote_servidor(server.getsockname()[1], port, comprimento_servidor, 1, 1)

        try:
            # Enviando mensagem ao cliente
            server.sendto(msg, address)
        except socket.error as msg:
            print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
            sys.exit()

server.close()
