import socket
import sys
import funcoes
import time
import random
from threading import Thread

# 0 - versao do codigo:
while True:
    try:
        user_friendly = int(input("versao:\n0 para normal\n1 para user-friendly"))
        break
    except:
        continue

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

# thread de escuta coloca dados do ack no buffer
buffer = [None]

# escuta so termina quando a main termina
# enquanto isso fica ouvindo a todo tempo
escuta = Thread(target=funcoes.esperar_ack, args= (client,tamanho_do_pacote,buffer))
escuta.daemon = True 
escuta.start()

# numero seq que deve ser enviado
seq = 0

for index,dados in enumerate(array):
    soma = funcoes.checksum(portaorigem, port, comprimento)
    dados = int(dados)  
    if dados == -1: break
    
    if user_friendly:
        escolha = funcoes.menu(array,index)
        # Forçar o erro de bits mudando a soma de verificação
        if escolha == 2: soma += 42
        # Forçando pacotes duplicados
        elif escolha == 3: seq = 1 - seq    
        #Encerrando cliente
        elif escolha == 5:
            sys.exit()

    # cria mensagem e envia
    msg = funcoes.cria_pacote_cliente(portaorigem, port, comprimento, soma, seq, dados) 
    funcoes.enviar_msg(client,msg,host,port)
    
    tcounter = 0 # time counter
    while True:

        time.sleep(0.001) # espera 1 milisec 
        if tcounter == 100: # time out: timer de 100 milisec
            funcoes.enviar_msg(client,msg,host,port)
            tcounter = 0 # reinicia timer

        else: tcounter += 1 # esperar mais

        # mensagem nao chegou ainda
        if buffer[0] is None: continue

        data = buffer[0]

        portaorigemservidor , portadestinoservidor, comprimentoservidor , ackservidor  , seqservidor  , somaservidor  = funcoes.extrair_dados_cliente(data)

        vericar_soma = funcoes.checksum(portadestinoservidor, portadestinoservidor, comprimentoservidor)

        # pacote com erros
        if somaservidor != vericar_soma or (ackservidor == 1-seq and seqservidor == 1-seq):
            tcounter = 0 # reinicia o timer
        
        # pacote chegou sem erros
        else:
            buffer[0] = None # buffer indicando que prox pacote ainda nao chegou
            seq = 1-seq # seq modificado para proximo pacote
            break
  
client.close()
