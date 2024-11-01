"""
Start both the HTTP server and the websocket server in parallel.
"""

import asyncio
import threading

from .rest_api import app as flask_app
from .websocket_api import start_server as websocket_server


def start_websocket_server(server):
    asyncio.get_event_loop().run_until_complete(server)
    print("WebSocket server running on ws://localhost:12345")
    asyncio.get_event_loop().run_forever()


def run_flask_app(port=8080):
    flask_app.run(port=port)


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    start_websocket_server(websocket_server)
