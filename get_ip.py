import socket

def check_for_internet_conection():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 0))
        return s.getsockname()[0]
    except OSError:
        return None

print(check_for_internet_conection())