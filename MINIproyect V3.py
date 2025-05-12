import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

class VisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seguimiento de Figuras y Colores")
        self.root.configure(bg="#f0f0f0")
        self.figura_seleccionada = tk.StringVar(value="Círculo")
        self.color_seleccionado = tk.StringVar(value="Rojo")
        self.deteccion_activa = False
        self.cap = cv2.VideoCapture(0)

        self.setup_ui()
        self.update_frame()

    def setup_ui(self):
        title = tk.Label(self.root, text="Detector de Figuras y Colores", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack()

        ttk.Label(control_frame, text="Figura:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(control_frame, textvariable=self.figura_seleccionada, values=["Círculo", "Cuadrado", "Triángulo"], width=12).grid(row=0, column=1, padx=5)

        ttk.Label(control_frame, text="Color:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Combobox(control_frame, textvariable=self.color_seleccionado, values=["Rojo", "Verde", "Azul"], width=12).grid(row=1, column=1, padx=5)

        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Iniciar Detección", command=self.iniciar_deteccion).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Detener", command=self.detener_deteccion).grid(row=0, column=1, padx=10)

        self.status_label = tk.Label(self.root, text="Estado: Esperando...", font=("Helvetica", 12), bg="#f0f0f0")
        self.status_label.pack(pady=5)

        self.lienzo = tk.Label(self.root, bd=4, relief="solid")
        self.lienzo.pack()

    def iniciar_deteccion(self):
        self.deteccion_activa = True
        self.status_label.config(text="Estado: Detectando...")

    def detener_deteccion(self):
        self.deteccion_activa = False
        self.status_label.config(text="Estado: Detención manual.")

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.resize(frame, (640, 480))
        resultado = frame.copy()

        detectado = False
        if self.deteccion_activa:
            detectado = self.detectar_figura_color(resultado)

        frame_rgb = cv2.cvtColor(resultado, cv2.COLOR_BGR2RGB)
        borde_color = "#0f0" if detectado else "#f00"
        self.lienzo.config(highlightbackground=borde_color)

        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lienzo.imgtk = imgtk
        self.lienzo.configure(image=imgtk)

        self.root.after(10, self.update_frame)

    def detectar_figura_color(self, frame):
        color = self.color_seleccionado.get()
        figura = self.figura_seleccionada.get()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        rangos = {
            "Rojo": [((0, 100, 100), (10, 255, 255)), ((160, 100, 100), (180, 255, 255))],
            "Verde": [((40, 50, 50), (80, 255, 255))],
            "Azul": [((100, 150, 0), (140, 255, 255))]
        }

        mascara = None
        for rango in rangos[color]:
            parcial = cv2.inRange(hsv, rango[0], rango[1])
            mascara = parcial if mascara is None else cv2.bitwise_or(mascara, parcial)

        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > 1000:
                approx = cv2.approxPolyDP(contorno, 0.04 * cv2.arcLength(contorno, True), True)
                vertices = len(approx)
                figura_detectada = "Desconocida"

                if vertices == 3:
                    figura_detectada = "Triángulo"
                elif vertices == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    aspect_ratio = w / float(h)
                    if 0.9 <= aspect_ratio <= 1.1:
                        figura_detectada = "Cuadrado"
                elif vertices > 6:
                    figura_detectada = "Círculo"

                if figura_detectada == figura:
                    x, y, w, h = cv2.boundingRect(contorno)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{figura} {color}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                    self.status_label.config(text=f"Estado: {figura} {color} Detectado")
                    return True

        self.status_label.config(text="Estado: Buscando...")
        return False

    def cerrar(self):
        self.cap.release()
        self.root.quit()

# Ejecutar la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    app = VisionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar)
    root.mainloop()
