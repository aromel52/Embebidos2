import cv2

#Codes: cv2.COLOR_BGR2GRAY, cv2.COLOR_BGR2HSV	
def change_color(img, code):
	changed_color = cv2.cvtColor(img,code)
	return changed_color
	
if __name__ == "__main__":
	color1 = cv2.imread("colors/color1.jpg")
	color2 = cv2.imread("colors/color2.jpg")
	color3 = cv2.imread("colors/color3.jpg")
	
	gcolor1 = change_color(color1,cv2.COLOR_BGR2GRAY)
	gcolor2 = change_color(color2,cv2.COLOR_BGR2GRAY)
	gcolor3 = change_color(color3,cv2.COLOR_BGR2GRAY)
	
	cv2.imshow("GrayScale Color 1",gcolor1)
	cv2.imshow("GrayScale Color 2",gcolor2)
	cv2.imshow("GrayScale Color 3",gcolor3)
	
	cv2.waitKey(0)
