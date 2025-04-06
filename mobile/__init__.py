import asyncio
import json
import datetime
import dotenv
import websockets

dotenv()

latest_data_timestamp: None | datetime.datetime = None

async def gps_receiver(websocket):
    global latest_data_timestamp
    # 10 Seconds every data
    async for message in websocket:
        try:
            data = json.loads(message)
            
            if "latitude" not in data or "longitude" not in data or "accuracy" not in data:
                if DEBUG_DATA:
                    print("Received invalid GPS data.")
                continue

            curr = datetime.datetime.now()
            with storage_lock:
                if latest_data_timestamp is not None:
                    diff = (curr - latest_data_timestamp).total_seconds()
                    if diff < MIN_TIMESTAMP_DIFF:
                        if data["latitude"] == tmp_storage[-1]["latitude"] and data["longitude"] == tmp_storage[-1]["longitude"]:
                            if DEBUG_DATA:
                                print("Received data too fast. Skip adding to storage.")
                            continue

                latest_data_timestamp = curr
                data["timestamp"] = latest_data_timestamp.isoformat()
                print(f"Received GPS Data: {data}")

                # float
                # Sample data: `{"latitude": 00000, "longitude": 0000, "timestamp": "HH:MM:SS.sssZ"}`
                # Save data to temp storage
                # TODO: Implement a new function to save this to database or smth???
                if len(tmp_storage) >= STORAGE_LIMIT:
                    tmp_storage.pop(0)
                    if DEBUG_DATA:
                        print("Removed oldest data from storage.")
                tmp_storage.append(data)
                if DEBUG_DATA:
                    print("Data added to storage.")
        except json.JSONDecodeError:
            print("Received invalid JSON data.")
        except Exception as e:
            print(f"An error occurred: {e}")

async def start_server():
    async with websockets.serve(gps_receiver, HOSTNAME, PORT_WS):
        print(f"GPS Server started at ws://{HOSTNAME}:{PORT_WS}")
        await asyncio.Future()
