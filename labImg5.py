import cv2
from abc import ABC, abstractmethod

#Codes: cv2.COLOR_BGR2GRAY, cv2.COLOR_BGR2HSV	
def change_color(img, code):
	changed_color = cv2.cvtColor(img,code)
	return changed_color
	
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
		while self.displayed:
			check, frame = self.camera.read()
			hsv_video = change_color(frame,cv2.COLOR_BGR2HSV)
			#cv2.imshow("camera",frame)
			key = cv2.waitKey(1)
			filter_mode = key
			if filter_mode == 81:
			    filter_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			else:
			    filter_frame = frame
			cv2.imshow("Frame",filter_frame)
			if key == 27:
				self.stop_display()
	
if __name__ == "__main__":
	#Video Capture
	camera = cv2.VideoCapture(2)
	camera_object = video_Capture(camera)
	camera_object.display_camera()
	camera.release()

