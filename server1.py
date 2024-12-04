import asyncio
import struct
import random

serverID = 1
ip = "127.0.0.1"
port = 8081
sleep_time = 2

messages = [
            f"Hello, this is server {serverID}!",
        f"Another message from server {serverID}.",
            f"Goodbye!"
        ]

def create_message_and_pack()->bytes:
    global messages
    msgNum = len(messages)-1
    # Encode the message
    message = messages[random.randint(0,msgNum)]
    body = message.encode('utf-8')
    message_length = len(body)
    # Create the 20-byte header
    # First 4 bytes are the length of the message (big-endian unsigned integer)
    header = struct.pack('!I', message_length) + b'\x00' * 16  # Remaining 16 bytes as padding
    return  header + body


async def mock_server_routine(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        # List of messages to send
        
        while True:
            await asyncio.sleep(1)

            # Send the message body
            writer.write(create_message_and_pack())
            await writer.drain()
            
            # Add a delay between messages
            await asyncio.sleep(sleep_time)
            
    except Exception as e:
        print(f"Server {serverID} error: {e}")
        
    # finally:
    #     writer.close()
    #     await writer.wait_closed()


async def start_mock_server(host, port):
    server = await asyncio.start_server(mock_server_routine, host, port)
    print(f"Mock server running on {host}:{port}")
    async with server:
        await server.serve_forever()

# Run the mock server
if __name__ == "__main__":
    try:
        asyncio.run(start_mock_server(ip, port))
    except Exception as e:
        print(f"something happened: {e}")
    finally:    
        print(f'server {serverID} stopped running')