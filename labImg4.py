import cv2
import numpy as np

#Codes: cv2.COLOR_BGR2GRAY, cv2.COLOR_BGR2HSV	
def change_color(img, code):
	changed_color = cv2.cvtColor(img,code)
	return changed_color

if __name__ == "__main__":
    img = cv2.imread("image2.jpg")
    hsv = change_color(img,cv2.COLOR_BGR2HSV)
    #Definir rangos para el rojo en HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    #Crear mascaras
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)
    #Detectar pixeles rojos
    coords = cv2.findNonZero(red_mask)
    cv2.imshow("HSV", hsv)
    cv2.waitKey(0)
    
    if coords is not None:
        print(f"\n Se encontraron {len(coords)} pixeles rojos.")
        print("Valores de saturacion de algunos pixeles rojos: ")
        
        for i in range(min(10,len(coords))):
            x, y = coords[i][0]
            s = hsv[y, x][1]
            print(f"Pixel en ({x},{y}) -> Saturacion: {s}")
