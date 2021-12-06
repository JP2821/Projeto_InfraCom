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

while True:
    # Criando Sockets UDP
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('\nSocket criado com sucesso!')
        break
    except socket.error as msg:
        print('\nFalha ao criar o socket. Código do erro: ' + str(msg[0]) + '. Mensagem: ' + msg[1])

while True:
    # Conectando o socket ao localhost e a porta definida
    try:
        server.bind((host, port))
        print('\nBind do Socket completo!')
        break
    except socket.error as msg:
        print('\nBind falhou. Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])

# Aqui iremos fazer um contador de estados
# para saber se é a primeira vez que ele entra nesse estado
fist_time = 0
seq_esperado = 0
server_on = True
while server_on:

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

    # tratarmante de erros e checagens:

    if seq != seq_esperado:
        print("\nPacote [" + str(dadoanterior) + "] duplicado! Descartando e re-solicitando...")
        dados_duplicados.append(dadoanterior)

    if soma != checksum:
        print("\nPacote [" + str(dado) + "] com erro de bits! Descartando e re-solicitando...")
        dados_corrompidos.append(dado)

    # erro no pacote recebido
    while (seq != seq_esperado or soma != checksum):

        # envia pacote com ack errado para avisar o erro
        msg = funcoes.cria_pacote_servidor(server.getsockname()[1], port, comprimento_servidor, 1 - seq_esperado,
                                           1 - seq_esperado)

        try:
            funcoes.print_info_servidor(dado, dados_recebidos, dados_duplicados, dados_corrompidos)
            # Enviando ao cliente a mensagem de pacotes duplicados
            server.sendto(msg, address)

        except socket.error as msg:
            print('Código do erro: ' + str(msg[0]) + '.Messagem: ' + msg[1])
            continue  # try again

        # Recebendo dados do cliente (dados, endereço)
        data, address = server.recvfrom(tamanho_do_pacote)

        if not data:  # erro, tenta novamente
            continue

        # Extraindo dados do pacote
        dadoanterior = dado
        portaorigem, portadestino, comprimento, checksum, seq, dado = funcoes.extrair_dados_servidor(data)

        soma = funcoes.checksum(portaorigem, portadestino, comprimento)

    if server_on == False: break

    # caso pacote nao tenha problemas:
    dados_recebidos.append(dado)

    # enviar ack correto:

    while True:
        i += 1
        os.system('clear')
        print("\n------------------------------------------")
        print("\tEnvio do", i, "º pacote")
        print("------------------------------------------")

        funcoes.print_info_servidor(dado, dados_recebidos, dados_duplicados, dados_corrompidos)
        msg = funcoes.cria_pacote_servidor(server.getsockname()[1], port, comprimento_servidor, seq_esperado,
                                           0)  # ack =0

        try:
            # Enviando mensagem ao cliente
            server.sendto(msg, address)
            break
        except socket.error as msg:
            print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
            continue

    seq_esperado = 1 - seq_esperado

server.close()
