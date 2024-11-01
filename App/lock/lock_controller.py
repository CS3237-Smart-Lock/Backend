import requests


class LockController:
    def __init__(self, ip: str):
        self.ip = ip

    def unlock_door(self):
        url = f"{self.ip}/unlock"
        result = requests.get(url)
        return result.status_code

    def lock_door(self):
        url = f"{self.ip}/lock"
        result = requests.get(url)
        return result.status_code
