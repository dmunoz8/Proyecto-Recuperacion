# Necesita cv2 para obtener características. 3.10 usado
import numpy as np
import cv2

class DescriptorImg:
    def __init__(self, bins):
        # guarda números de características por dimension (hsv)
        self.bins = bins

    def describe(self, imagen):
        # convierte la imagen al espacio HSV.
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        # inicia vector de características
        caracts = []

        # obtiene las dimensiones y calcula centro
        (h, w) = imagen.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))

        # divide la imagen en cuatro segmentos (principio de localidad)
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
            (0, cX, cY, h)]

        # máscara elíptica del centro de la imagen
        (axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
        ellipMask = np.zeros(imagen.shape[:2], dtype = "uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

        # itera los segmentos
        for (startX, endX, startY, endY) in segments:
            # construye una máscara para cada esquina, restándole el elipsis del centro
            cornerMask = np.zeros(imagen.shape[:2], dtype = "uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)

            # extrae el histograma de la imagen y actualiza las características.
            hist = self.histogram(imagen, cornerMask)
            caracts.extend(hist)

        # extrae las características del elipsis central.
        hist = self.histogram(imagen, ellipMask)
        caracts.extend(hist)

        # devuelve características
        return caracts

    def histogram(self, imagen, mask):
        # extrae un histograma de color 3D a partir de la región enmascarada 
        # por @mask de la imagen @imagen, utilizando @bins contenedores por 
        # canal Luego lo normaliza
        hist = cv2.calcHist([imagen], [0, 1, 2], mask, self.bins,
            [0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist).flatten()

        # devuelve el resultado
        return hist