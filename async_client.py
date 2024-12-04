import asyncio
import struct
import servers_addr
from time import time
from typing import *


async def recv_and_parse_message(reader: asyncio.StreamReader)->asyncio.coroutines:
        # Receive the header (20 bytes)
    header = await reader.readexactly(20)
    # Extract message length from the header
    message_length = struct.unpack('!I', header[:4])[0]  # Big-endian unsigned integer
    
    # Receive the message body based on the length
    message_body = await reader.readexactly(message_length)
    # Decode and print the message body
    result = message_body.decode('utf-8')
    return result


async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, server_name: str)->asyncio.coroutines:
    """
    Handles a single connection to a server. Reads messages based on the protocol.
    """
    try:
        while True:
            message = await recv_and_parse_message(reader)
            print(f"[{server_name}] Received message: {message}")
            
            
    except asyncio.IncompleteReadError:
        print(f"[{server_name}] Connection closed by the server.")
        # add to reconnection_list
        print('add my connection to reconnection_list and use a task to reconnect')
    except Exception as e:
        print(f"[{server_name}] Error: {e}")
    # finally:
    #     writer.close()
    #     await writer.wait_closed()


async def main():
    """
    Connects to multiple servers and handles their connections concurrently.
    """
    # List of server addresses
    servers = servers_addr.SERVERS
    
    # Create connections for all servers
    tasks = []
    for host, port, server_name in servers:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            print(f"Connected to {server_name} at {host}:{port}")
            tasks.append(handle_connection(reader, writer, server_name))
        except Exception as e:
            print(f"Failed to connect to {server_name} at {host}:{port}. Error: {e}")
    
    # Run all connections concurrently
    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("No servers to connect to. Exiting.")


# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
