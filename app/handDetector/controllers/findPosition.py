import cv2

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
