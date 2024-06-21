import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

img = cv2.imread("D:\\projects @\\car number\\36601__Skoda_Octavia_2017-001.jpg")
cv2.imshow("org", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", gray)

canny = cv2.Canny(gray, 170, 224)
cv2.imshow("canny", canny)


contours, _ = cv2.findContours(canny.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

contour_with_license_plate = None
license_plate = None
x = None
y = None
w = None
h = None

contour_img = img.copy()
cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
cv2.imshow("img with contours", contour_img)

for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
    print("approx", len(approx))
    if len(approx) == 4:
        contour_with_license_plate = approx
        x, y, w, h = cv2.boundingRect(contour)
        license_plate = gray[y:y+h, x:x+w]
        break

(thresh, license_plate) = cv2.threshold(license_plate, 129, 255, cv2.THRESH_BINARY)
cv2.imshow("plate1", license_plate)
license_plate = cv2.bilateralFilter(license_plate, 11, 17, 19)

txt = pytesseract.image_to_string(license_plate)


text_x = max(x - 100, 0)
text_y = max(y - 200, 0)

image = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
image = cv2.putText(image, txt, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.imshow("plate", image)
print("license plate:", txt)

cv2.waitKey(0)
cv2.destroyAllWindows()
