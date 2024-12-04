import asyncio
import struct
import servers_addr
from time import time
from typing import *


# Global lists for tracking connected and disconnected servers
reconnect_delay = 10
connected_servers = []
disconnected_servers = []


async def recv_and_parse_message(reader: asyncio.StreamReader) -> str:
    # Receive the header (20 bytes)
    header = await reader.readexactly(20)
    # Extract message length from the header
    message_length = struct.unpack('!I', header[:4])[0]  # Big-endian unsigned integer
    
    # Receive the message body based on the length
    message_body = await reader.readexactly(message_length)
    # Decode and return the message body
    return message_body.decode('utf-8')


async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, server_info: Tuple[str, int, str]) -> None:
    """
    Handles a single connection to a server. Reads messages based on the protocol.
    """
    host, port, server_name = server_info
    try:
        while True:
            message = await recv_and_parse_message(reader)
            print(f"[{server_name}] Received message: {message}")
    except asyncio.IncompleteReadError:
        print(f"[{server_name}] Connection closed by the server.")
    except Exception as e:
        print(f"[{server_name}] Error: {e}")
    finally:
        # Move server from connected to disconnected
        if server_info in connected_servers:
            connected_servers.remove(server_info)
        if server_info not in disconnected_servers:
            disconnected_servers.append(server_info)
        writer.close()
        await writer.wait_closed()


async def connect_to_server(host: str, port: int, server_name: str) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter, str]:
    """
    Establishes a connection to a single server.
    """
    try:
        reader, writer = await asyncio.open_connection(host, port)
        print(f"Connected to {server_name} at {host}:{port}")
        server_info = (host, port, server_name)
        
        if server_info not in connected_servers:
            connected_servers.append(server_info)
        if server_info in disconnected_servers:
            disconnected_servers.remove(server_info)
        return reader, writer, server_name
    
    except Exception as e:
        print(f"Failed to connect to {server_name} at {host}:{port}. Error: {e}")
        server_info = (host, port, server_name)
        if server_info not in disconnected_servers:
            disconnected_servers.append(server_info)
        return None, None, server_name


async def reconnect():
    """
    Reconnects to all servers in the disconnected list.
    """
    while True:
        for server_info in disconnected_servers.copy():
            host, port, server_name = server_info
            reader, writer, name = await connect_to_server(host, port, server_name)
            if reader and writer:
                asyncio.create_task(handle_connection(reader, writer, server_info))
        await asyncio.sleep(reconnect_delay)  # Wait before retrying


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
            server_info = (host, port, server_name)
            tasks.append(asyncio.create_task(handle_connection(reader, writer, server_info)))

    # Start a task to handle reconnections
    tasks.append(asyncio.create_task(reconnect()))

    # Run all connection tasks concurrently
    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("No servers to connect to.")


# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
