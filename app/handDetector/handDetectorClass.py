import cv2
import mediapipe as mp

# Importamos las funciones
from .controllers.findHands import findHands
from .controllers.findPosition import findPosition
from .controllers.fingersUp import fingersUp
from .controllers.findDistance import findDistance


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode  # detectar si el número máximo de manos ya ha sido alcanzado
        self.maxHands = maxHands  # máximo de manos a detectar
        self.detectionCon = detectionCon  # confianza para la detección de la mano
        self.trackCon = trackCon  # confianza para el seguimiento de la mano

        # Cargamos la solución de manos de MediaPipe y configuramos con los parámetros definidos
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, int(
            self.detectionCon), int(self.trackCon))

        # Cargamos la utilidad de dibujo de MediaPipe
        self.mpDraw = mp.solutions.drawing_utils
        # Definimos los ids de las puntas de los dedos en el modelo de mano de MediaPipe
        self.tipIds = [4, 8, 12, 16, 20]

    findHands = findHands
    findPosition = findPosition
    fingersUp = fingersUp
    findDistance = findDistance
