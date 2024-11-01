"""
A testing script to open the laptop's camera and stream it to the websocket server located at uri localhost:12345

This is mainly used for manually testing the websocket server without needing the actual ESP32 camera
"""

import asyncio
import base64
import json
import base64
from datetime import datetime, timedelta

import websockets
import cv2


def is_x_seconds_passed(x, start_time):
    curr_time = datetime.now()
    return (curr_time - start_time) >= timedelta(seconds=x)


async def send_camera_feed():
    # Connect to the WebSocket server
    uri = "ws://localhost:12345"

    async with websockets.connect(uri) as websocket:
        # Open the camera
        cap = cv2.VideoCapture(0)
        await websocket.send(
            json.dumps(
                {
                    "type": "command",
                    "data": base64.b64encode("start".encode()).decode("utf-8"),
                }
            )
        )

        start_time = datetime.now()

        try:
            while cap.isOpened():
                # Read a frame from the camera
                ret, frame = cap.read()

                if is_x_seconds_passed(10, start_time):
                    await websocket.send(
                        json.dumps(
                            {
                                "type": "command",
                                "data": base64.b64encode("end".encode()).decode(
                                    "utf-8"
                                ),
                            }
                        )
                    )
                    break

                # Check if the frame was captured successfully
                if not ret:
                    break

                # Encode the frame as a JPEG image
                _, buffer = cv2.imencode(".jpg", frame)

                # Convert the image to a base64-encoded string
                frame_data = base64.b64encode(buffer).decode("utf-8")

                # Send the frame data over the WebSocket
                await websocket.send(json.dumps({"type": "image", "data": frame_data}))

                # To prevent overloading the server, add a short delay
                await asyncio.sleep(0.05)

        finally:
            # Release the camera resource
            cap.release()


# Start the WebSocket client
asyncio.run(send_camera_feed())
