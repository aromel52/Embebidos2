import cv2
import numpy as np

# Función para detectar el color
def get_color_name(hsv_value):
    h, s, v = hsv_value
    if s > 100 and v > 50:
        if 0 <= h <= 10 or 160 <= h <= 180:
            return "Rojo"
        elif 35 <= h <= 85:
            return "Verde"
        elif 90 <= h <= 130:
            return "Azul"
    return "Desconocido"

# Inicializar cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionar si es muy grande
    frame = cv2.resize(frame, (640, 480))
    blur = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Crear máscara de color (rojo, verde y azul combinados)
    masks = {
        "Rojo": cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255])) +
                cv2.inRange(hsv, np.array([160, 100, 100]), np.array([180, 255, 255])),
        "Verde": cv2.inRange(hsv, np.array([35, 100, 100]), np.array([85, 255, 255])),
        "Azul": cv2.inRange(hsv, np.array([90, 100, 100]), np.array([130, 255, 255]))
    }

    for color, mask in masks.items():
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                epsilon = 0.04 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)

                if len(approx) == 3:  # Triángulo
                    x, y, w, h = cv2.boundingRect(approx)
                    cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
                    cv2.putText(frame, f'Triángulo {color}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Detección de Triángulos", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
