import asyncio
import websockets
import cv2
import numpy as np
import base64
import time

async def echo(websocket, path):
    async for message in websocket:
        # Decode the base64 message back to image data
        img_data = base64.b64decode(message)
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Display the frame
        if frame is not None:
            cv2.imshow("Received Video", frame)
            # Use waitKey to update the frame; 1ms delay is typical for video
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # Press 'q' to exit the video display

    cv2.destroyAllWindows()  # Close the display window when done

# Set up the WebSocket server
start_server = websockets.serve(echo, "localhost", 12345)

