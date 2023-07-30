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
