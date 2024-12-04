import asyncio
import struct
import servers_addr
from time import time
from typing import *


async def recv_and_parse_message(reader: asyncio.StreamReader) -> str:
    # Receive the header (20 bytes)
    header = await reader.readexactly(20)
    # Extract message length from the header
    message_length = struct.unpack('!I', header[:4])[0]  # Big-endian unsigned integer
    
    # Receive the message body based on the length
    message_body = await reader.readexactly(message_length)
    # Decode and return the message body
    return message_body.decode('utf-8')


async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, server_name: str) -> None:
    """
    Handles a single connection to a server. Reads messages based on the protocol.
    """
    try:
        while True:
            message = await recv_and_parse_message(reader)
            print(f"[{server_name}] Received message: {message}")
    except asyncio.IncompleteReadError:
        print(f"[{server_name}] Connection closed by the server.")
        print('Add my connection to reconnection_list and use a task to reconnect')
    except Exception as e:
        print(f"[{server_name}] Error: {e}")


async def connect_to_server(host: str, port: int, server_name: str) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter, str]:
    """
    Establishes a connection to a single server.
    """
    try:
        reader, writer = await asyncio.open_connection(host, port)
        print(f"Connected to {server_name} at {host}:{port}")
        return reader, writer, server_name
    except Exception as e:
        print(f"Failed to connect to {server_name} at {host}:{port}. Error: {e}")
        return None, None, server_name


def create_task(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, server_name: str) -> asyncio.Task:
    """
    Creates a task to handle the connection.
    """
    return asyncio.create_task(handle_connection(reader, writer, server_name))


async def main():
    """
    Connects to multiple servers and handles their connections concurrently.
    """
    # List of server addresses
    servers = servers_addr.SERVERS
    
    # Connect to all servers and create tasks for handling connections
    tasks = []
    for host, port, server_name in servers:
        reader, writer, name = await connect_to_server(host, port, server_name)
        if reader and writer:
            tasks.append(create_task(reader, writer, name))
    
    # Run all connection tasks concurrently
    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("No servers to connect to. Exiting.")


# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
