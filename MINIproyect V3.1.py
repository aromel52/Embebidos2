import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading

# Inicializar estilo
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VisionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Vision Tracker Interface")
        self.geometry("900x600")
        self.resizable(False, False)

        # Fondo
        self.bg_image = Image.open("C:\Users\MSI\Desktop\7mo semestre\background.png")  # Usa una imagen tuya estilo futurista
        self.bg_image = self.bg_image.resize((900, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Panel blanco moderno
        self.panel = ctk.CTkFrame(self, width=400, height=500, corner_radius=20, fg_color="white")
        self.panel.place(relx=0.5, rely=0.5, anchor="center")

        self.init_ui()

    def init_ui(self):
        # Título
        title = ctk.CTkLabel(self.panel, text="Object Tracker", text_color="#222222", font=("Arial Bold", 28))
        title.pack(pady=(30, 10))

        # Menú de selección de color
        self.color_var = ctk.StringVar(value="Rojo")
        color_label = ctk.CTkLabel(self.panel, text="Color:", text_color="#444444")
        color_label.pack(pady=(20, 5))
        color_menu = ctk.CTkOptionMenu(self.panel, variable=self.color_var, values=["Rojo", "Verde", "Azul"])
        color_menu.pack()

        # Menú de selección de figura
        self.shape_var = ctk.StringVar(value="Triángulo")
        shape_label = ctk.CTkLabel(self.panel, text="Figura:", text_color="#444444")
        shape_label.pack(pady=(20, 5))
        shape_menu = ctk.CTkOptionMenu(self.panel, variable=self.shape_var, values=["Triángulo", "Cuadrado", "Círculo"])
        shape_menu.pack()

        # Botón de iniciar
        start_button = ctk.CTkButton(self.panel, text="Iniciar detección", command=self.start_detection)
        start_button.pack(pady=(30, 10))

        # Lugar para cámara (próximo paso)
        self.video_frame = ctk.CTkLabel(self.panel, text="Vista previa de cámara", width=300, height=200,
                                        fg_color="#dddddd", corner_radius=10, text_color="#888888")
        self.video_frame.pack(pady=(20, 10))

    def start_detection(self):
        selected_color = self.color_var.get()
        selected_shape = self.shape_var.get()
        print(f"Iniciando detección de: {selected_shape} {selected_color}")
        # Aquí iniciarías el hilo para visión artificial

if __name__ == "__main__":
    app = VisionApp()
    app.mainloop()
