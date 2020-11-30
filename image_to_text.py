import pytesseract
from pytesseract import Output
import cv2


img = cv2.imread("test.png")


text = pytesseract.image_to_string(img)
print(text)

ha = text.split('\n')


sentences = []
phrase = ""
for i in ha:
	
	if i == "" or i=='\x0c':
		sentences.append(phrase)
		phrase = ""

	phrase += i + " "


words = []
for i in range(len(sentences)):
	words.append(sentences[i].split(" "))
	while True:
		try:
			words[i].remove("")
		except ValueError:
			break
#print(words)
#print(sentences)


d = pytesseract.image_to_data(img, output_type=Output.DICT)

coor = []

n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        coor.append((x, y, w, h))
        
        # put rectangle around words
        # img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

count = 0
box_coor = []
for i in words:
	x_max = 0
	x_min = 100000 # something really big
	y_max = 0
	y_min = 100000 # somthing really big
	for x in range(len(i)):
		
		if coor[count][0] + coor[count][2] > x_max:
			x_max = coor[count][0] + coor[count][2]

		if coor[count][0] < x_min:
			x_min = coor[count][0]

		if coor[count][1] + coor[count][3] > y_max:
			y_max = coor[count][1] + coor[count][3]

		if coor[count][1] < y_min:
			y_min = coor[count][1]
		
		count += 1


	box_coor.append((x_min, y_min, x_max, y_max))

print(box_coor)
for i in box_coor:
	img = cv2.rectangle(img, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
