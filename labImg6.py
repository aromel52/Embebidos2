import cv2
from abc import ABC, abstractmethod
import os

output_dir = "Captures"
os.makedirs(output_dir, exist_ok=True)

cont = 1
captured_images = []

class video_Capture_abs(ABC):
	@abstractmethod
	def display_camera(self):
		pass
		
	@abstractmethod
	def stop_display(self):
		pass
		
	@abstractmethod
	def camera_visualization(self):
		pass
		
class video_Capture(video_Capture_abs):
	def __init__(self, camera) -> None:
		self.camera = camera
		self.displayed = False
		
	def display_camera(self):
		self.displayed = True
		self.camera_visualization()
		
	def stop_display(self):
		self.displayed = False
		
	def camera_visualization(self):
	    global cont
	    while self.displayed:
	        check, frame = self.camera.read()
	        cv2.imshow("Video Frame", frame)
	        key = cv2.waitKey(1)
	        
	        if key == 99:
	            filename = f"{output_dir}/image{cont}.jpg"
	            cv2.imwrite(filename, frame)
	            captured_images.append(filename)
	            print(f"Imagen Guardada: {filename}")
	            cont  += 1
	            
	        if key == 27:
	            self.stop_display()
	            
if __name__ == "__main__":
	#Video Capture
	camera = cv2.VideoCapture(2)
	camera_object = video_Capture(camera)
	camera_object.display_camera()
	camera.release()
