import pytesseract
from pytesseract import Output
import cv2


img = cv2.imread("images\\test2.png")


text = pytesseract.image_to_string(img)
# print(text)

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

print(words)
par_num = []
count = 0
for i in words:
	for j in range(len(i)):
		par_num += [count]

	count += 1

print(count)
print(par_num)


d = pytesseract.image_to_data(img, output_type=Output.DICT)


n_boxes = len(d['text'])
box_coor = [[100000, 100000, 0, 0] for x in range(count)]

num = 0
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (par, x, y, w, h) = (par_num[num], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        
        if x + w > box_coor[par][2]:
        	box_coor[par][2] = x + w
        if x < box_coor[par][0]:
        	box_coor[par][0] = x
        if y + h > box_coor[par][3]:
        	box_coor[par][3] = y + h
        if y < box_coor[par][1]:
        	box_coor[par][1] = y
        num += 1

        
print('new box coor ', str(box_coor))

for i in box_coor:
	img = cv2.rectangle(img, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 2)



# cv2.imshow('img', img)
# cv2.waitKey(0)
