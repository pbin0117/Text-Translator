import pytesseract
from pytesseract import Output
import cv2
import time

def preprocessing_typing_detection(inputImage):
    img_gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    
    return img_gray

def show_box(box_coor, img):
	# for showing the boxes
	for i in box_coor:
		img = cv2.rectangle(img, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 2)



	cv2.imshow('img', img)
	cv2.waitKey(0)



def assign_box_coor(count, d, par_num):
	n_boxes = len(d['text'])
	box_coor = [[100000, 100000, 0, 0] for x in range(count)]

	# for errors of the ocr
	for i in range(n_boxes-len(par_num)):
		par_num.append(0)
	
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

	return box_coor

def form_sentence(text):
	sentences = []
	phrase = ""
	for i in text:
		
		if i == "" or i=='\x0c':
			sentences.append(phrase)
			phrase = ""

		phrase += i + " "

	return sentences

def get_par_num(sentences):
	par_num = []
	count = 0

	for i in range(len(sentences)):

		aa = 1 if i == 0 else 2


		num_words = len(sentences[i].split(" "))-aa
		

		for j in range(num_words):
			par_num += [count]

		count += 1

	return par_num, count

def image_to_text(img, language):
	img = preprocessing_typing_detection(img)

	text = pytesseract.image_to_string(img, lang=language)
	actual_text = text.split('\n')

	# creates a list of sentences for each paragraph
	sentences = form_sentence(actual_text)


	# assign paragraph number to each word
	par_num, count = get_par_num(sentences)
		

	# getting coordinates for each sentence blocks
	d = pytesseract.image_to_data(img, output_type=Output.DICT, lang=language)
	box_coor = assign_box_coor(count, d, par_num)


	return sentences, box_coor
	

if __name__ == "__main__":
	startTime = time.time()

	img = cv2.imread("images\\test_spa2.png")

	sentences, box_coor = image_to_text(img, "spa")

	print('box coor: ', str(box_coor))
	print("run time: ", str(round(time.time() - startTime, 3)), "s")

	show_box(box_coor, img)
	

	