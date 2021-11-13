# Projeto_InfraCom
Criação de serviço de chat de sala única

## files/folders:
### para_envio/para_recepcao
arquivos para receber e enviar (testar a aplicação)

### receiver/sender
Receiver e sender implementam respectivamente as funções de enviar e receber arquivos.

Na main do receiver importamos a função do sender, o mesmo para main do sender.

O receiver recebe o arquivo do sender, e depois reenvia para o sender.

### receber/transmitir
Transmitir envia .png para receber


### MultiClient
Client envia mensagem para Server,
Server repassa as mensagens para os outros clients. 

Client possui uma thread para escrever e enviar mensagem
e outra para escutar o as mensagens que são transmitadas pelo server
