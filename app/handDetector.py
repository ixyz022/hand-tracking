# Importamos las librerías necesarias
import cv2
import mediapipe as mp
import time
import math


# Creamos la clase handDetector
class handDetector():
    # Inicializamos la clase con los parámetros deseados
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # mode: en este modo, si el número máximo de manos ya ha sido alcanzado, simplemente detecta la presencia de manos adicionales, pero no rastrea su movimiento.
        self.mode = mode
        # maxHands: número máximo de manos a detectar
        self.maxHands = maxHands
        # detectionCon: umbral de confianza para la detección de la mano
        self.detectionCon = detectionCon
        # trackCon: umbral de confianza para el seguimiento de la mano
        self.trackCon = trackCon

        # Cargamos la solución de manos de MediaPipe y configuramos con los parámetros definidos
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, int(
            self.detectionCon), int(self.trackCon))

        # Cargamos la utilidad de dibujo de MediaPipe
        self.mpDraw = mp.solutions.drawing_utils
        # Definimos los ids de las puntas de los dedos en el modelo de mano de MediaPipe
        self.tipIds = [4, 8, 12, 16, 20]

    # Método para detectar y dibujar las manos en la imagen
    def findHands(self, img, draw=True):
        # Convertimos la imagen a RGB ya que la solución de manos usa imágenes en ese formato
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Procesamos la imagen para encontrar las manos
        self.results = self.hands.process(imgRGB)

        # Si se encuentran manos, recorremos cada una de ellas
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Dibujamos las landmarks (puntos clave) de cada mano
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    # Método para encontrar la posición de cada landmark en la mano
    def findPosition(self, img, handNo=0, draw=False):
        xList = []  # Lista para almacenar las coordenadas x de cada landmark
        yList = []  # Lista para almacenar las coordenadas y de cada landmark
        bbox = []   # Lista para almacenar las coordenadas del bounding box de la mano
        self.lmList = []  # Lista para almacenar la posición de cada landmark

        # Si se encuentran manos, elegimos una de ellas según handNo
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            # Recorremos cada landmark de la mano
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape  # Altura, ancho y canales de la imagen
                # Calculamos la posición del landmark en la imagen (los valores en lm son proporcionales al tamaño de la imagen)
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # Almacenamos la posición del landmark
                self.lmList.append([id, cx, cy])

                if draw:  # Si queremos dibujar los landmarks
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            # Calculamos las coordenadas del bounding box de la mano
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = [xmin, ymin, xmax, ymax]

            if draw:  # Si queremos dibujar el bounding box
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                              (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)

        return self.lmList, bbox

    # Método para comprobar si cada dedo está levantado o no
    def fingersUp(self):
        # Lista para almacenar el estado de cada dedo (1 = levantado, 0 = no levantado)
        fingers = []
        # Suponemos que el primer punto de la punta de la lista representa el pulgar
        # Si la posición en x del pulgar es mayor que la del punto inmediatamente anterior, el pulgar está levantado
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # Para los 4 dedos restantes
        for id in range(1, 5):
            # Si la posición en y de la punta del dedo es menor que la del punto dos posiciones antes, el dedo está levantado
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    # Método para encontrar la distancia entre dos puntos
    def findDistance(self, p1, p2, img, draw=True):
        # Posición del primer punto
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        # Posición del segundo punto
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Posición del punto medio

        if draw:  # Si queremos dibujar la línea y los puntos
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Calculamos la longitud de la línea (distancia entre los puntos)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]
