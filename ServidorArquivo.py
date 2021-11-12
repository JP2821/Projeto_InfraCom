import socket
import time

print("Iniciando Server")
Host = '127.0.0.1'
Port = 5000
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((Host, Port))
servidor.settimeout(10.0)

# 1 Esperando a lista de arquivos do cliente chegar
print("Recebendo arquivos...\n")
arquivos = []
while 1:
    msg, endereco = servidor.recvfrom(512)
    if msg.decode(errors="ignore") == "stop":
        break
    nome_arquivo = msg.decode()
    print(f"[{len(arquivos)} {nome_arquivo}]")
    arquivos.append(nome_arquivo)

# 3 Peruntando ao Cliente qual arquivo ele quer baixar
arquivo_escolhido = int(input("\nQual arquivo sera baixado ?"))
while not (0 <= arquivo_escolhido < len(arquivos)):
    print("Menor aí não dá né")
    arquivo_escolhido = int(input("\nQual arquivo sera baixado ?"))

servidor.sendto(arquivo_escolhido.to_bytes(4, "little"), endereco)

# 7 Recebendo o numero de pacotes que vão chegar
msg = servidor.recv(4)
numero_de_pacotes = int.from_bytes(msg, "little")

# 9 Recebendo os nazarentos
servidor.settimeout(5.0)
arquivo = open(arquivos[arquivo_escolhido], "wb")
pacotes_em_kilobytes = 512
pacotes_em_bytes = pacotes_em_kilobytes * 8
print(f"Recebendo {numero_de_pacotes} pacotes...")
start = time.time()
for i in range(numero_de_pacotes):
    msg = servidor.recv(pacotes_em_bytes)
    arquivo.write(msg)
    porcentagem = f"Baixando... {round((100 * (i+1))/numero_de_pacotes,2)}%"
    print('\r' + porcentagem, end='')
tempo_de_dowload = round(time.time() - start, 2)
print(f"dowload concluido, tempo transcorrido {tempo_de_dowload} sec")

arquivo.close()

arquivo = open(arquivos[arquivo_escolhido], "rb")
#enviando de volta:
print("arquivo:")
for line in arquivo:
    print(line)


#limpando a casa
arquivo.close()
servidor.close()
