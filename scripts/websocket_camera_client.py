"""
A testing script to open the laptop's camera and stream it to the websocket server located at uri localhost:12345

This is mainly used for manually testing the websocket server without needing the actual ESP32 camera
"""

import cv2
import asyncio
import websockets
import base64

async def send_camera_feed():
    # Connect to the WebSocket server
    uri = "ws://localhost:12345"
    async with websockets.connect(uri) as websocket:
        # Open the camera
        cap = cv2.VideoCapture(0)
        
        try:
            while cap.isOpened():
                # Read a frame from the camera
                ret, frame = cap.read()
                
                # Check if the frame was captured successfully
                if not ret:
                    break

                # Encode the frame as a JPEG image
                _, buffer = cv2.imencode('.jpg', frame)
                
                # Convert the image to a base64-encoded string
                frame_data = base64.b64encode(buffer).decode('utf-8')
                
                # Send the frame data over the WebSocket
                await websocket.send(frame_data)

                # To prevent overloading the server, add a short delay
                await asyncio.sleep(0.02)

        finally:
            # Release the camera resource
            cap.release()

# Start the WebSocket client
asyncio.run(send_camera_feed())
