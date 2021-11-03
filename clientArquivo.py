import socket
import os
import time

print("Iniciando o Client")
Host = '127.0.0.1'
Port = 5000
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.connect((Host, Port))
cliente.settimeout(10.0)

# 2 Enviando os arquivos para o servidor
lista_de_arquivos = os.listdir()
print("Enviando nomes dos arquivos...")
for arquivo in lista_de_arquivos:
    cliente.sendall(arquivo.encode())

cliente.sendall("stop".encode())

# 4 Esperando o servidor Responder
msg = cliente.recv(4)
indece = int.from_bytes(msg, "little")

# 5 abrindo o arquivo para mandar o nazarento
arquivo = open(lista_de_arquivos[indece], 'rb')
tamanho_arquivo = os.path.getsize((lista_de_arquivos[indece])) #tamanho do arquivo em bits
pacotes_em_kilobytes = 512
pacotes_em_bytes = pacotes_em_kilobytes * 8

# 6 Enviando o numero de pacotes para o servidor
numero_de_pacotes  = (tamanho_arquivo // pacotes_em_bytes) + 1
cliente.sendall(numero_de_pacotes.to_bytes(4, 'little'))

# 8 Enviando os nazarentos
delay = 0.004
tempo_estimado = numero_de_pacotes * (delay * 1.2)

print(f"Enviando {numero_de_pacotes} pacotes ao servior")
print(f"Tempo estimado: {round(tempo_estimado)} sec")

for i in range(numero_de_pacotes):
    pacote = arquivo.read(pacotes_em_bytes)
    cliente.sendall(pacote)
    enviando_o_nazarento = f"{int((i+1)*pacotes_em_kilobytes)} / {int(pacotes_em_kilobytes*numero_de_pacotes)}Kb"
    print('\r' + enviando_o_nazarento, end = '')
    time.sleep(delay)

# Limpando tudo
cliente.close()
arquivo.close()
