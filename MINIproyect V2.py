
import cv2
import numpy as np

class FiguraDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.color_ranges = {
            "Rojo": [
                (np.array([0, 100, 100]), np.array([10, 255, 255])),
                (np.array([160, 100, 100]), np.array([180, 255, 255]))
            ],
            "Verde": [(np.array([35, 100, 100]), np.array([85, 255, 255]))],
            "Azul": [(np.array([90, 100, 100]), np.array([130, 255, 255]))]
        }

    def detectar_color(self, hsv_pixel):
        h, s, v = hsv_pixel
        for color, ranges in self.color_ranges.items():
            for lower, upper in ranges:
                if lower[0] <= h <= upper[0] and lower[1] <= s <= upper[1] and lower[2] <= v <= upper[2]:
                    return color
        return "Desconocido"

    def detectar_formas_y_colores(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        resultados = []

        for color, rangos in self.color_ranges.items():
            mascara_total = np.zeros(hsv.shape[:2], dtype=np.uint8)
            for rango in rangos:
                mascara = cv2.inRange(hsv, rango[0], rango[1])
                mascara_total = cv2.bitwise_or(mascara_total, mascara)

            contours, _ = cv2.findContours(mascara_total, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 500:
                    approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
                    x, y, w, h = cv2.boundingRect(approx)
                    forma = self.identificar_forma(approx)
                    if forma != "Desconocido":
                        resultados.append((forma, color, (x, y, w, h), approx))
        return resultados

    def identificar_forma(self, approx):
        lados = len(approx)
        if lados == 3:
            return "Triángulo"
        elif lados == 4:
            return "Cuadrado"
        elif lados > 6:
            return "Círculo"
        else:
            return "Desconocido"

    def ejecutar(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))
            figuras = self.detectar_formas_y_colores(frame)

            for forma, color, (x, y, w, h), contorno in figuras:
                cv2.drawContours(frame, [contorno], -1, (0, 255, 0), 2)
                texto = f"{forma} {color}"
                cv2.putText(frame, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("Detección de Figuras y Colores", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

# Ejecutar
if __name__ == "__main__":
    detector = FiguraDetector()
    detector.ejecutar()

