import asyncio
import websockets
from collections import defaultdict
import os
from dotenv import load_dotenv
import json

load_dotenv()
rooms = defaultdict(set)

async def handler(websocket):
    websocket.max_size = 100 * 1024 * 1024 * 100
    try:
        await websocket.send("Please enter your room:")
        room_name = await websocket.recv()
        rooms[room_name].add(websocket)
        print(f"Client joined room: {room_name}")
        await websocket.send("System")

        async for message in websocket:
            print(f"Received message in room '{room_name}': {message}")
            if message == "exit":
                print(f"Exit signal received from room '{room_name}'. Closing connection.")
                break
            if message in ["System", "Network", "Logs", "Software"]:
                for client in rooms[room_name]:
                    if client != websocket:

                        await client.send(message)
            else:
                try:
                    data = json.loads(message)
                    for client in rooms[room_name]:
                        if client != websocket:
                            await client.send(json.dumps(data))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON message: {str(e)}")
                except Exception as e:
                    print(f"Error processing message: {str(e)}")
    except websockets.exceptions.ConnectionClosedError:
        print(f"Client disconnected from room: {room_name}")
    finally:
        if room_name in rooms:
            rooms[room_name].remove(websocket)
            if not rooms[room_name]:
                del rooms[room_name]
        await websocket.close()

async def main():
    server_url = os.getenv('SERVER_URL')
    port = int(os.getenv('PORT'))
    if server_url is None:
        raise ValueError("SERVER_URL environment variable is not set.")
    async with websockets.serve(handler, server_url, port, max_size=100*1024*1024*100):
        print(f"WebSocket server is running on ws://{server_url}:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")