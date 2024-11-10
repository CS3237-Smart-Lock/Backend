import numpy as np
import websockets
import cv2

import base64
import json
import os
import asyncio
from datetime import datetime

from ..db.db import Database
from ..models.face_detector import FaceDetector
from ..models.face_recognition import Recognizer, Facenet512Encoder
from ..tools.embedding import decode_to_vector
from ..tools.arrays import is_subarray

face_detector = FaceDetector()
face_recognizer, encoder = Recognizer(threshold=0.3), Facenet512Encoder()

connected_clients: set[websockets.WebSocketServerProtocol] = set()

db = Database(os.path.join("db", "database"))


class APIState:
    def __init__(self):
        self.attempt_started = False
        self.face_found = False
        self.gesture_record:list = []

    def reset(self) -> None:
        self.attempt_started = False
        self.face_found = False
        self.gesture_record = []

    async def toggle_face_found(self, value, wait=1):
        await asyncio.sleep(wait)
        self.face_found = value


class AuthenticationState:

    def __init__(self):
        self.face:str = "" # stores the id of the user found for logging and other purposes 
        self.gesture = False

    def reset(self) -> None:
        self.face = ""
        self.gesture = False

    def success(self) -> bool:
        return bool(self.face) and self.gesture

    def get_failures(self) -> list[str]:
        res = []
        if not self.face:
            res.append("face")
        if not self.gesture:
            res.append("gesture")
        return res 


async def receive_data(websocket):
    """Receives base64 encoded image data over websocket, decodes, and returns the image."""
    async for message in websocket:
        if not message:
            continue

        try:
            message_json = json.loads(message)
        except json.decoder.JSONDecodeError:
            continue

        data_type = message_json["type"]
        data = base64.b64decode(message_json["data"])

        yield data_type, data


async def broadcast_to_clients(
    message: str, sender: websockets.WebSocketServerProtocol
):
    disconnected_clients = set()
    for client in connected_clients:
        if client == sender:
            continue

        try:
            await client.send(message)
        except websockets.ConnectionClosed:
            disconnected_clients.add(client)

    # Remove disconnected clients
    connected_clients.difference_update(disconnected_clients)


async def broadcast_log(message: str, sender: websockets.WebSocketServerProtocol):
    await broadcast_to_clients(
        json.dumps(
            {
                "type": "log",
                "data": base64.b64encode(
                    f"[{datetime.now().time()}] {message}".encode()
                ).decode("utf-8"),
            }
        ),
        sender=sender,
    )


async def handle_image(
    img_data: bytes, states: APIState, auth_states: AuthenticationState, websocket
):
    # Check if the image data is corrupt
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        await broadcast_log("Corrupt image data received. Cannot process.", sender=websocket)
        return  # Exit the function if the image is corrupt

    faces = face_detector.get_faces(img_data)

    if len(faces) == 0:
        processed_img = img_data
    else:
        if not states.face_found:
            states.face_found = True

            await broadcast_log("Found face, running recognition...", sender=websocket)

            base64_image = (
                f"data:image/jpeg;base64,{base64.b64encode(img_data).decode('utf-8')}"
            )
            embedding = encoder.encode(base64_image)

            users = db.get_all_users()
            for user in users:
                if face_recognizer.is_same_person(
                    embedding, decode_to_vector(user["embedding"])
                ):
                    await broadcast_log(
                        f"User recognized: {user["name"]}", sender=websocket
                    )
                    auth_states.face = user["id"]

            if not auth_states.face:
                await broadcast_log(
                    "No user recognized, will retry in 2 seconds.", sender=websocket
                )
                asyncio.create_task(states.toggle_face_found(False, wait=2))

        processed_img = face_detector.get_image_with_face_circled(img_data)

    np_arr = np.frombuffer(processed_img, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    _, buffer = cv2.imencode(".jpg", img)
    img_as_text = base64.b64encode(buffer).decode("utf-8")
    await broadcast_to_clients(
        json.dumps({"type": "image", "data": img_as_text}), sender=websocket
    )


async def handle_gesture(gesture_data, states: APIState, auth_states: AuthenticationState, websocket):
    states.gesture_record.append(gesture_data)
    
    if not auth_states.face:
        return
    
    user_in_frame = db.get_user(auth_states.face)[0]
    gesture_password = json.loads(user_in_frame["gestures"])

    if is_subarray(states.gesture_record, gesture_password):
        auth_states.gesture = True
        


async def handle_command(command, states: APIState, auth_states:AuthenticationState, websocket):
    command = command.decode("utf-8")
    if command == "start":
        states.reset()

        states.attempt_started = True

        await broadcast_log(
            "Unlock attempt started, capturing enabled.", sender=websocket
        )

    elif command == "end":
        states.reset()

        await broadcast_log("Unlock attempt ended.", sender=websocket)

        await broadcast_to_clients(
            json.dumps(
                {
                    "type": "command",
                    "data": base64.b64encode("end".encode()).decode("utf-8"),
                }
            ),
            sender=websocket,
        )

        if not auth_states.success():
            failure_description = f"Authentication failed due to timeout, the following criterias were unsucessful: {auth_states.get_failures()}"
            # TODO : add a log to db
            await broadcast_log(failure_description, sender=websocket)

async def connect(websocket, path):
    """
    Main handler to receive, process, and broadcast images with face detection.

    It communicates via JSON, with the format below

    ```json
    {
        "type":"image" | "gesture" | "command" | "log"
        "data": base64 encoded data
    }
    ```

    A command is decoded into either "start" or "end", it indicates the start and end of a x seconds communication window from the sensors to the server.
    Images and gestuers and handled by their respective handlers.
    Logs are not used for the server side, but for clients to view.
    """

    connected_clients.add(websocket)

    states = APIState()
    auth_states = AuthenticationState()

    async for data_type, data in receive_data(websocket):
        if data_type not in ["command", "image", "gesture"]:
            continue

        if data_type == "command":
            await handle_command(data, states, auth_states, websocket)

        elif data_type == "image":
            await handle_image(data, states, auth_states, websocket)

        else:
            await handle_gesture(data, states, auth_states, websocket)

        if auth_states.success():
            # TODO: unlock door or whatever
            # TODO: add a log to db
            await broadcast_log("Authentication success, opening lock.", sender=websocket)


# Start the WebSocket server
start_server = websockets.serve(connect, "0.0.0.0", 12345)
