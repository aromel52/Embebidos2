import cv2

if __name__ == "__main__":
	color1 = cv2.imread("colors/color1.jpg")
	color2 = cv2.imread("colors/color2.jpg")
	color3 = cv2.imread("colors/color3.jpg")
	
	(b1,g1,r1) = color1[1,1]
	(b2,g2,r2) = color2[1,1]
	(b3,g3,r3) = color3[1,1]
	
	print("Color 1 [Blue,Green,Red]: ",b1,g1,r1)
	print("Color 2 [Blue,Green,Red]: ",b2,g2,r2)
	print("Color 3 [Blue,Green,Red]: ",b3,g3,r3)
