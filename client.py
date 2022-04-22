import asyncio
import websockets
from websockets import WebSocketServerProtocol


async def consumer_handler(ws: WebSocketServerProtocol) -> None:
    async for message in ws:
        print(message)


async def consume(host: str, port: int) -> None:
    url = f'ws://{host}:{port}'
    async with websockets.connect(url) as ws:
        await consumer_handler(ws)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume(host='localhost', port=8000))
    loop.run_forever()