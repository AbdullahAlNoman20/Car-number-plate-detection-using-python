import cv2
import pytesseract
import imutils

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

image = cv2.imread("image/car3.jpg")

# For img Resize
image = imutils.resize(image, width=500)

# To reduce dimension & Complexity
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# To Reduce Noise & make Smooth
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edge = cv2.Canny(gray, 170, 200)



# Function for Delete the Black Part

cnts, new = cv2.findContours(edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1 = image.copy()
cv2.drawContours(image1, cnts, -1, (0, 225, 0), 3)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]

NumberPlateCount = None
image2 = image.copy()

# For Detecting the Number plate

cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)
count = 0
name = 1

for i in cnts:
    perimeter = cv2.arcLength(i, True)

    # For More Sharply take the Number plate
    approx = cv2.approxPolyDP(i, 0.02*perimeter, True)

    # Thicnace the border color

    if(len(approx)==4):
        NumberPlateCount = approx

        # Create Rectangle

        x, y, w, h = cv2.boundingRect(i)
        crp_img = image[y:y+h, x:x+w]

        cv2.imwrite(str(name) + '.png', crp_img)
        name += 1
        break


cv2.drawContours(image, [NumberPlateCount], -1, (0, 255, 0), 3)
crpImg = '1.png'
cv2.imshow("Cropped Image", cv2.imread(crpImg))

# Convert img to string by using pytesseract
text = pytesseract.image_to_string(crpImg, lang = 'eng')
print("Car Number is : ", text)

# Show Section
cv2.imshow('original image', image)
# cv2.imshow('Gray Image', gray)
# cv2.imshow('Smoother', gray)
# cv2.imshow("canny image", edge)
# cv2.imshow("Canny after contours", image1)
# cv2.imshow("Top 30 contours",image2)
cv2.imshow("Final Image", image)
cv2.waitKey(0)
