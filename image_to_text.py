import pytesseract
from pytesseract import Output
import cv2


img = cv2.imread("test2.png")

print(pytesseract.image_to_string(img))

# Boxes around Characters
"""h,w,c = img.shape
boxes = pytesseract.image_to_boxes(img)
for b in boxes.splitlines():
	b = b.split(' ')
	img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
"""

d = pytesseract.image_to_data(img, output_type=Output.DICT)

info = []

n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        info.append((text, x, y, w, h))
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

#print(info)

sentences = []
horizontal_padding = 30
vertical_padding = 20

search = 0



while search < len(info) - 2:
	

	words = [info[search]]

	while info[search+1][1] < info[search][1] + info[search][3] + horizontal_padding and info[search][2] - vertical_padding < info[search+1][2] < info[search][2] + vertical_padding:
		words.append(info[search+1])
		search += 1

		if search == len(info) - 1:
			break

	search += 1
	
	sentences.append(words)
	
		

print(sentences)

cv2.imshow('img', img)
cv2.waitKey(0)