import cv2

class ImageColorConverter:
    def __init__(self,img_path):
        self.original = cv2.imread(img_path)
        
    def to_gray(self):
        img_gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        return img_gray
        
    def to_hsv(self):
        img_hsv = cv2.cvtColor(self.original, cv2.COLOR_BGR2HSV)
        return img_hsv
        
    def get_original(self):
        return self.original
        
if __name__ == "__main__":
    converter = ImageColorConverter("image2.jpg")
    
    original = converter.get_original()
    gray = converter.to_gray()
    hsv = converter.to_hsv()
    
    cv2.imshow("Original", original)
    cv2.imshow("Gray Scale", gray)
    cv2.imshow("HSV", hsv)
    cv2.waitKey(0)
