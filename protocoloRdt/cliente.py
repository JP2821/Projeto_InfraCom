import socket
import sys
import funcoes
import time
import random

# 1 - Declarando as variaveis de cabeçalho
host = 'localhost'
port = 5000
tamanho_do_pacote = 150
comprimento = 97

################ 97 porquê? #################
#                                           #
# 16 bytes para porta de origem             #
# 16 bytes para porta destino               #
# 16 bytes para comprimento total do pacote #
# 16 bytes para checksum                    #
# 1 byte para o número de sequência         #
# 32 bytes para o payload(carga)            #
#                                           #
# 16 + 16 + 16 + 16 + 32 + 1 = 97           #
#############################################

# 2 - Criando socket UDP
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Datagrama não criado")
    sys.exit()

portClient = 0 # Estou passando a porta como 0,pois o S.O. por sí só dá uma porta livre
client.bind(('', portClient))
portaorigem = client.getsockname()[1] #usamos o metodo getsockname para acessar a porta forncida pelo S.O

file = open(sys.argv[1], 'r')
array = file.read().splitlines()

while len(array) > 1:
    escolha = funcoes.menu(array)
    while (escolha == 4):
        toshuffle = array[0:len(array) - 1]
        random.shuffle(toshuffle)
        toshuffle.append('-1')
        array = toshuffle
        escolha = funcoes.menu(array)


    #Estado 0

    dados = int(array.pop(0))
    if dados == -1:
        break

    # Forçar o erro de bits mudando a soma de verificação
    if escolha == 2:
        soma = 0
    else:
        soma = funcoes.checksum(portaorigem, port, comprimento)

    #Forçando pacotes duplicados
    if escolha == 3:
        seq = 1
    else:
        seq = 0

    #Encerrando cliente
    if escolha == 5:
        sys.exit()

    msg = funcoes.cria_pacote_cliente(portaorigem, port, comprimento, soma, seq, dados)

    try: #Enviando o datagrama para o servidor
        msg = msg.encode()
        client.sendto(msg, (host, port))
    except socket.error as msg:
        print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
        sys.exit()

    # Estado 1
    # Recebendo mensagem do servidor
    data, address = client.recvfrom(tamanho_do_pacote)

    if not data:
        break

    portaorigemservidor , portadestinoservidor, comprimentoservidor , ackservidor  , seqservidor  , somaservidor  = funcoes.extrair_dados_cliente(data)

    vericar_soma = funcoes.checksum(portadestinoservidor, portadestinoservidor, comprimentoservidor)

    while (somaservidor != vericar_soma or (ackservidor == 1 and seqservidor == 1)):

        soma = funcoes.checksum(portaorigem, port, comprimento)
        seq = 0
        msg = funcoes.cria_pacote_cliente(portaorigem, port, comprimento, soma, seq, dados)
        msg = msg.encode()
        client.sendto(msg, (host, port))

        # Colocar thread para fazer isso.
        # cronometrar o tempo ate chegar, 
        # quando a mensagem chegar
        # a thread que instanciamos 
        # faz a atual parar de esperar

        # Recebendo a mensagem do servidor
        data,address = client.recvfrom(tamanho_do_pacote)
      
        portaorigemservidor , portadestinoservidor, comprimentoservidor , ackservidor  , seqservidor  , somaservidor = funcoes.extrair_dados_cliente(data)

        vericar_soma = funcoes.checksum(portaorigemservidor, portadestinoservidor, comprimentoservidor)

        if not data: #fim da comunicacao
            break

    #Estado 2

    escolha = funcoes.menu(array)
    while (escolha == 4):
        toshuffle = array[0:len(array) - 1]
        random.shuffle(toshuffle)
        toshuffle.append('-1')
        array = toshuffle
        escolha = funcoes.menu(array)

    dado = int(array.pop(0))
    if dado == -1:
        break

    # Forçar o erro de bits mudando a sma de verificação
    if escolha == 2:
        soma = 0
    else:
        soma = funcoes.checksum(portaorigem, port, comprimento)

    #Forçando pacotes duplicados
    if escolha == 3:
        seq = 1
    else:
        seq = 0

    #Encerrando cliente
    if escolha == 5:
        sys.exit()

    msg = funcoes.cria_pacote_cliente(portaorigem, port, comprimento, soma, seq, dados)

    try:
        #Enviando datagrama ao servidor
        msg = msg.encode()
        client.sendto(msg, (host, port))
    except socket.error as msg:
        print('Código do erro: ' + str(msg[0]) + '. Messagem: ' + msg[1])
        sys.exit()

    #Estado 3
    # Recebendo mensagem do servidor

    data, address = client.recvfrom(tamanho_do_pacote)

    if not data:
        break

    portaorigemservidor , portadestinoservidor, comprimentoservidor , ackservidor  , seqservidor  , somaservidor = funcoes.extrair_dados_cliente(data)

    vericar_soma = funcoes.checksum(portadestinoservidor, portadestinoservidor, comprimentoservidor)

    while (somaservidor != vericar_soma or (ackservidor == 1 and seqservidor == 0)):

        soma = funcoes.checksum(portaorigem, port, comprimento)
        seq = 1
        msg = funcoes.cria_pacote_cliente(portaorigem, port, comprimento, soma, seq, dado)
        msg = msg.encode()
        client.sendto(msg, (host, port))

        #Recebendo a mensagem do servidor
        data, address = client.recvfrom(tamanho_do_pacote)
        
        if not data:
            break

        portaorigemservidor , portadestinoservidor, comprimentoservidor , ackservidor  , seqservidor  , somaservidor = funcoes.extrair_dados_cliente(data)

        vericar_soma = funcoes.checksum(portadestinoservidor, portadestinoservidor, comprimentoservidor)



client.close()
