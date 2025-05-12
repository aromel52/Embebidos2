import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import threading
import numpy as np

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

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
        self.main_frame = ctk.CTkFrame(self, width=500, height=600, corner_radius=25, fg_color="white")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        self.title_label = ctk.CTkLabel(self.main_frame, text="Detector de Objetos", font=("Arial", 24), text_color="#222")
        self.title_label.pack(pady=(30, 20))

        # Selecciones
        self.color_label = ctk.CTkLabel(self.main_frame, text="Color:", font=("Arial", 16), text_color="#333")
        self.color_label.pack()
        self.color_option = ctk.CTkOptionMenu(self.main_frame, values=["Rojo", "Verde", "Azul"], width=200)
        self.color_option.pack(pady=10)

        self.shape_label = ctk.CTkLabel(self.main_frame, text="Figura:", font=("Arial", 16), text_color="#333")
        self.shape_label.pack()
        self.shape_option = ctk.CTkOptionMenu(self.main_frame, values=["Triangulo", "Cuadrado", "Circulo"], width=200)
        self.shape_option.pack(pady=10)

        # Botones
        self.start_button = ctk.CTkButton(self.main_frame, text="Iniciar detección", width=180, command=self.iniciar_deteccion)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self.main_frame, text="Detener detección", width=180, command=self.detener_deteccion, fg_color="red", hover_color="#cc0000")
        self.stop_button.pack(pady=(0, 20))

        # Vista previa ampliada
        self.preview_frame = ctk.CTkFrame(self.main_frame, width=400, height=300, fg_color="#f2f2f2", corner_radius=15)
        self.preview_frame.pack(pady=10)
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="")
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

        self.running = False

    def iniciar_deteccion(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.detectar_objeto, daemon=True).start()

    def detener_deteccion(self):
        self.running = False
        self.preview_label.configure(image="")  

    def detectar_objeto(self):
        cap = cv2.VideoCapture(0)
        color = self.color_option.get()
        figura = self.shape_option.get()

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            # Preprocesamiento
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (400, 300))
            img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = self.get_color_mask(img_hsv, color)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 500:
                    approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
                    shape_name = self.detect_shape(approx)
                    if shape_name == figura:
                        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)
                        cv2.putText(frame, f"{color} {figura}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 50), 2)

            # Mostrar en GUI
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.preview_label.configure(image=imgtk)
            self.preview_label.image = imgtk

        cap.release()

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



app = App()
app.mainloop()
