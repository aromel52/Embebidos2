import customtkinter as ctk 
from PIL import Image, ImageTk
import cv2
import threading
import numpy as np
import RPi.GPIO as GPIO

# Configuración de pines GPIO para L298N
MOTOR_LEFT_IN1 = 17  # GPIO17 para IN1 (Motor izquierdo, avance)
MOTOR_LEFT_IN2 = 18  # GPIO18 para IN2 (Motor izquierdo, retroceso)
MOTOR_RIGHT_IN3 = 22 # GPIO22 para IN3 (Motor derecho, avance)
MOTOR_RIGHT_IN4 = 23 # GPIO23 para IN4 (Motor derecho, retroceso)

# Configurar GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_LEFT_IN1, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_IN2, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_IN3, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_IN4, GPIO.OUT)

# Inicializar pines en LOW
GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)
GPIO.output(MOTOR_RIGHT_IN3, GPIO.LOW)
GPIO.output(MOTOR_RIGHT_IN4, GPIO.LOW)

# Parámetros para la estimación de distancia
REAL_WIDTH_CM = 5.0
KNOWN_DISTANCE_CM = 20.0
KNOWN_WIDTH_PIXELS = 100
FOCAL_LENGTH = (KNOWN_WIDTH_PIXELS * KNOWN_DISTANCE_CM) / REAL_WIDTH_CM

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Funciones para controlar los motores
def motor_avanzar():
    GPIO.output(MOTOR_LEFT_IN1, GPIO.HIGH)
    GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_IN3, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_IN4, GPIO.LOW)

def motor_retroceder():
    GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_IN2, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_IN3, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_IN4, GPIO.HIGH)

def motor_girar_izquierda():
    GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_IN2, GPIO.HIGH)  # Izquierdo retrocede
    GPIO.output(MOTOR_RIGHT_IN3, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_IN4, GPIO.LOW)  # Derecho avanza

def motor_girar_derecha():
    GPIO.output(MOTOR_LEFT_IN1, GPIO.HIGH)
    GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)   # Izquierdo avanza
    GPIO.output(MOTOR_RIGHT_IN3, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_IN4, GPIO.HIGH) # Derecho retrocede

def motor_detener():
    GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_IN3, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_IN4, GPIO.LOW)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Interfase 99")
        self.geometry("900x700")
        self.resizable(False, False)

        # Fondo
        self.bg_image = ImageTk.PhotoImage(Image.open("C:/Users/MSI/Desktop/7semestre/background.jpg").resize((900, 700)))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Main Frame
        self.main_frame = ctk.CTkFrame(self, width=500, height=620, corner_radius=25, fg_color="white")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        self.title_label = ctk.CTkLabel(self.main_frame, text="Detector de Objetos", font=("Arial", 24), text_color="#222")
        self.title_label.pack(pady=(20, 10))

        # Selecciones
        self.color_label = ctk.CTkLabel(self.main_frame, text="Color:", font=("Arial", 16), text_color="#333")
        self.color_label.pack()
        self.color_option = ctk.CTkOptionMenu(self.main_frame, values=["Rojo", "Verde", "Azul"], width=200)
        self.color_option.pack(pady=5)

        self.shape_label = ctk.CTkLabel(self.main_frame, text="Figura:", font=("Arial", 16), text_color="#333")
        self.shape_label.pack()
        self.shape_option = ctk.CTkOptionMenu(self.main_frame, values=["Triangulo", "Cuadrado", "Circulo"], width=200)
        self.shape_option.pack(pady=5)

        # Botones
        self.start_button = ctk.CTkButton(self.main_frame, text="Iniciar detección", width=180, command=self.iniciar_deteccion)
        self.start_button.pack(pady=5)

        self.stop_button = ctk.CTkButton(self.main_frame, text="Detener detección", width=180, command=self.detener_deteccion, fg_color="red", hover_color="#cc0000")
        self.stop_button.pack(pady=5)

        # Vista previa
        self.preview_frame = ctk.CTkFrame(self.main_frame, width=450, height=350, fg_color="#f2f2f2", corner_radius=15)
        self.preview_frame.pack(pady=10)
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="")
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

        # Mensaje
        self.message_label = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 14), text_color="red")
        self.message_label.pack(pady=(5, 10))

        self.running = False

    def iniciar_deteccion(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.detectar_objeto, daemon=True).start()

    def detener_deteccion(self):
        self.running = False
        motor_detener()  # Detener motores al detener detección
        self.preview_label.configure(image="")
        self.message_label.configure(text="")

    def detectar_objeto(self):
        cap = cv2.VideoCapture(0)
        color = self.color_option.get()
        figura = self.shape_option.get()
        centro_imagen = 450 // 2  # Centro de la imagen (ancho = 450 píxeles)
        tolerancia_centro = 20    # Tolerancia para considerar el objeto centrado (±20 píxeles)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                motor_detener()
                break

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (450, 350))
            img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = self.get_color_mask(img_hsv, color)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            count_detected = 0

            # Procesar el primer objeto válido encontrado
            objeto_detectado = False
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 500:
                    approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
                    shape_name = self.detect_shape(approx)
                    if shape_name == figura:
                        count_detected += 1
                        x, y, w, h = cv2.boundingRect(cnt)
                        distancia_cm = (REAL_WIDTH_CM * FOCAL_LENGTH) / w
                        centro_objeto = x + w // 2  # Centro horizontal del objeto
                        objeto_detectado = True

                        # Lógica de control
                        if abs(centro_objeto - centro_imagen) > tolerancia_centro:
                            if centro_objeto < centro_imagen:
                                motor_girar_izquierda()
                            else:
                                motor_girar_derecha()
                        else:
                            if distancia_cm > 12:
                                motor_avanzar()
                            elif distancia_cm < 8:
                                motor_retroceder()
                            elif 8 <= distancia_cm <= 12:
                                motor_detener()

                        # Dibujar contorno y texto
                        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)
                        cv2.putText(frame, f"{color} {figura}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 255, 50), 2)
                        cv2.putText(frame, f"Distancia: {distancia_cm:.1f} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 100), 2)
                        break  # Procesar solo el primer objeto válido

            # Si no se detecta el objeto, detener los motores
            if not objeto_detectado:
                motor_detener()

            # Mensaje general
            if count_detected > 2:
                self.message_label.configure(text="¡Más de 2 objetos detectados!")
            else:
                self.message_label.configure(text=f"Objetos detectados: {count_detected}")

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.preview_label.configure(image=imgtk)
            self.preview_label.image = imgtk

        cap.release()
        motor_detener()  # Detener motores al salir

    def detect_shape(self, approx):
        vertices = len(approx)
        if vertices == 3:
            return "Triangulo"
        elif vertices == 4:
            x, y, w, h = cv2.boundingRect(approx)
            if 0.95 <= w/h <= 1.05:
                return "Cuadrado"
        elif vertices > 6:
            return "Circulo"
        return "Otro"

    def get_color_mask(self, hsv, color):
        if color == "Rojo":
            lower1 = np.array([0, 120, 70])
            upper1 = np.array([10, 255, 255])
            lower2 = np.array([170, 120, 70])
            upper2 = np.array([180, 255, 255])
            return cv2.inRange(hsv, lower1, upper1) + cv2.inRange(hsv, lower2, upper2)
        elif color == "Verde":
            lower = np.array([35, 100, 100])
            upper = np.array([85, 255, 255])
            return cv2.inRange(hsv, lower, upper)
        elif color == "Azul":
            lower = np.array([100, 150, 0])
            upper = np.array([140, 255, 255])
            return cv2.inRange(hsv, lower, upper)

try:
    app = App()
    app.mainloop()
finally:
    GPIO.cleanup()  # Limpiar configuración de GPIO al cerrar