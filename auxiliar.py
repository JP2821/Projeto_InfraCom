import socket

def get_local_id():
    return socket.gethostbyname(socket.gethostname())
