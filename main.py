# Importamos las librerías necesarias
from app.handDetector.handDetectorClass import handDetector
import cv2
import time

# Inicializamos las variables de tiempo pTime y cTime a 0

pTime = 0
cTime = 0

# Creamos un objeto de captura de video cap, que captura el video de la cámara por defecto (generalmente la cámara web del ordenador)
cap = cv2.VideoCapture(0)

# Creamos un objeto detector utilizando la clase handDetector que hemos definido anteriormente
detector = handDetector()

# Entramos en un bucle infinito para capturar y procesar cada cuadro de la cámara de video
while True:
    # Leemos un cuadro del objeto de captura de video
    success, img = cap.read()

    # Usamos el objeto detector para encontrar y dibujar las manos en el cuadro capturado
    img = detector.findHands(img)

    # Usamos el objeto detector para encontrar la posición de cada landmark en la imagen
    lmList, bbox = detector.findPosition(img)

    # Si hemos encontrado landmarks en la imagen, imprimimos la posición del landmark 4 (la punta del pulgar)
    if len(lmList) != 0:
        print(lmList[4])  # Imprime la posición de la punta del pulgar

    # Obtenemos el tiempo actual y lo almacenamos en cTime
    cTime = time.time()

    # Calculamos los frames por segundo (fps) como la inversa de la diferencia entre el tiempo actual y el tiempo anterior
    fps = 1 / (cTime - pTime)

    # Actualizamos el tiempo anterior al tiempo actual
    pTime = cTime

    # Dibujamos los fps calculados en la imagen en la posición (10, 70) con un tamaño de fuente de 3 y un color de (255, 0, 255)
    cv2.putText(img, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Mostramos la imagen en una ventana llamada "Image"
    cv2.imshow("Image", img)

    # Esperamos durante 1 milisegundo para cualquier entrada de teclado
    cv2.waitKey(1)
