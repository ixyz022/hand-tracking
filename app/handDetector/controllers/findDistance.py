import cv2
import math

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
