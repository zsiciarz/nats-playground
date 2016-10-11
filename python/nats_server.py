import logging
import socketserver


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] %(name)s %(levelname)s: %(message)s'))
logger.addHandler(handler)


class NatsHandler(socketserver.StreamRequestHandler):
    def handle(self):
        logger.info('Client connection created: {}'.format(self.client_address))
        self.info()
        while True:
            data = self.rfile.readline().strip()
            if not data:
                break
            logger.info(data)
            if data.startswith(b'PING'):
                self.pong()
        logger.info('Client connection closed')

    def info(self):
        self.wfile.write(b'INFO {"max_payload": 1024}\r\n')

    def pong(self):
        self.wfile.write(b'PONG\r\n')


if __name__ == '__main__':
    server = socketserver.TCPServer(('localhost', 4222), NatsHandler, bind_and_activate=False)
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    logger.info('Starting server...')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server shutting down...')
        server.shutdown()
