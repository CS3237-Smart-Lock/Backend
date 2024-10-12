import cv2
import numpy as np

class FaceDetector: 
    def __init__(self):
        ...

    def get_image_with_face_circled(self, image_blob):
        nparr = np.frombuffer(image_blob, np.uint8)

        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        success, encoded_image = cv2.imencode('.png', image)
        
        if success:
            image_blob = encoded_image.tobytes()
            return image_blob
        else:
            raise Exception("Image encoding failed")

    def get_faces(self, image_blob:bytes):
        print("getting faces")
        nparr = np.frombuffer(image_blob, np.uint8)

        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print("decoded image")

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=5, minSize=(30, 30))
        print(faces)

        return faces


# cv2.imshow('Faces found', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
