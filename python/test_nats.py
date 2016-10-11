import asyncio
from datetime import datetime

from nats.aio.client import Client
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


async def on_response(msg):
    print('[{dt}] [{subject}]: {response} (data={data})'.format(
        dt=datetime.now(),
        subject=msg.subject,
        response=msg.reply,
        data=msg.data.decode('utf-8'),
    ))


async def test_nats(loop):
    client = Client()
    await client.connect(io_loop=loop)
    await client.subscribe('test_subject', cb=on_response)
    while True:
        await client.publish('test_subject', 'Test NATS ąółęśń'.encode('utf-8'))
        await asyncio.sleep(1, loop=loop)
    await client.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_nats(loop))
    loop.close()
