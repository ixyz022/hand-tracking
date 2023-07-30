import cv2

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
