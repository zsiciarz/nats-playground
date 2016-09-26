import json
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 4222))
try:
    while True:
        msg = sock.recv(1024)
        if not msg:
            break
        if msg.startswith(b'INFO'):
            print(json.loads(msg[5:].decode('utf-8')))
        elif msg.startswith(b'PING'):
            sock.send(b'PONG\r\n')
        else:
            print('unknown message: %s' % msg.decode('utf-8'))
except Exception as e:
    print(e)
finally:
    sock.close()
