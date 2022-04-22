import asyncio
import websockets
from websockets import WebSocketServerProtocol


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        print(f'{ws.remote_address} connect')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        print(f'{ws.remote_address} disconnect')

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send_to_clients(message)

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketServerProtocol, url: str) -> None:
        await self.register(ws)
        try:
            await  self.distribute(ws)
        finally:
            await  self.unregister(ws)


server = Server()
start_server = websockets.serve(server.ws_handler, 'localhost', 8000)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
