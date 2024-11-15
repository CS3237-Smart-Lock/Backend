from abc import ABC, abstractmethod
from scipy.spatial.distance import cosine
from deepface import DeepFace

class Encoder(ABC):
    @abstractmethod
    def encode(self) -> list[float]:
        pass

class Facenet512Encoder:
    def encode(self, image) -> list[float]:
        """
        img (str or np.ndarray): The exact path to the image, a numpy array in BGR format, or a base64 encoded image. If the source image contains multiple faces, the result will include information for each detected face.
        """
        return DeepFace.represent(img_path=image, model_name="Facenet512", max_faces=1)[0]["embedding"]

class Recognizer:
    def __init__(self, threshold=0.6, distance_metric=cosine) -> None:
        self.threshold = threshold
        self.distance_metric = distance_metric

    def is_same_person(self, embedding1:list[float], embedding2:list[float]):
        return self.distance_metric(embedding1, embedding2) >= self.threshold
