import cv2
import numpy as np


class FaceDetector:
    def __init__(self, scale_factor=1.1):
        self.scale_facor = scale_factor

    def get_image_with_face_circled(self, image_blob: bytes):
        if not image_blob:
            return None

        nparr = np.frombuffer(image_blob, np.uint8)

        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=self.scale_facor, minNeighbors=10, minSize=(150, 150)
        )

        for x, y, w, h in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        success, encoded_image = cv2.imencode(".jpg", image)

        if success:
            image_blob = encoded_image.tobytes()
            return image_blob
        else:
            raise Exception("Image encoding failed")

    def get_faces(self, image_blob: bytes):
        if not image_blob:
            return []

        nparr = np.frombuffer(image_blob, np.uint8)

        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=self.scale_facor, minNeighbors=10, minSize=(150, 150)
        )

        return faces
