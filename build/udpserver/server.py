"""
Lab - IP Spoof Attack

Minimal UDP Echo Server with amplification for IP spoofing examples

Each packet of data is multiplied by `AMPLIFICATION` and sent back

This is intentional insecure code! Do NOT use for production!

(CC BY-SA 4.0) github.com/moospit
"""

import asyncio

# Set the amount of amplification the server uses
# in each response
AMPLIFICATION = 10

SERVER_ADDR = '0.0.0.0'
SERVER_PORT = 9999


class EchoServerProtocol(asyncio.DatagramProtocol):
    """ Minimal UDP echo server implementation
        see: https://docs.python.org/3/library/asyncio-protocol.html
    """

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        """ Set a transport """
        self.transport = transport  # pylint: disable=attribute-defined-outside-init

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        """ Handle incoming data """
        print(f'received {len(data)} bytes from {addr}')
        print(f'send {len(data)*AMPLIFICATION} to {addr}')
        self.transport.sendto(data*AMPLIFICATION, addr)  # type: ignore


async def main() -> None:
    """ Start the server """
    print('starting UDP server')
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),  # pylint: disable=unnecessary-lambda
        local_addr=(SERVER_ADDR, SERVER_PORT))
    _ = protocol

    print(f'running on {SERVER_ADDR}:{SERVER_PORT}')

    try:
        while loop.is_running():  # run forever
            await asyncio.sleep(10)
        # await asyncio.sleep(3600)  # serve for 1 hour.
    except KeyboardInterrupt:
        print('user requested exit')
    finally:
        print('cleaning up')
        transport.close()


asyncio.run(main())
