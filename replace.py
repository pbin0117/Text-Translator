import cv2
from math import floor

def replace_text(box_coor, text, img):
	font = cv2.FONT_HERSHEY_SIMPLEX
	numOfTexts = range(len(text))
	minFontScale = 0.6
	
	fontScale = [0 for i in numOfTexts]
	width = [box_coor[i][2] - box_coor[i][0] for i in numOfTexts]

	for i in numOfTexts:
		wordNum = len(text[i])
		
		characterLength = width[i]/wordNum
		
		scale = characterLength / 15

		fontScale[i] = scale if scale > minFontScale else minFontScale

	fontColor = (0, 0, 0)
	lineType = 2
	color = (255, 255, 255)
	


	new_box_coor, new_text, newNumOfTexts, newFontScale = new_line(box_coor, text, fontScale, numOfTexts, width)
	bottomLeftCorner = [(new_box_coor[i][0], new_box_coor[i][3]) for i in newNumOfTexts]


	
	for i in numOfTexts:
		cv2.rectangle(img, (box_coor[i][0], box_coor[i][1]), (box_coor[i][2], box_coor[i][3]), color, -1)
	
	for i in newNumOfTexts:
		cv2.putText(img, new_text[i], bottomLeftCorner[i], font, newFontScale[i], fontColor, lineType)
	
		


def new_line(box_coor, text, fontScale, numOfTexts, width):
	new_box_coor = []
	padding = 10
	new_text = []
	newFontScale = []


	for i in numOfTexts:
		print("num of characters: ",len(text[i]))
		print("fontScale: ",fontScale[i])
		print("width: ",width[i])

		if len(text[i]) * fontScale[i] * 15 > width[i]:
			cuttingPoint = floor(width[i]/(15*fontScale[i])) - padding

			iterations = floor(len(text[i])/cuttingPoint)
			print("iter: ", iterations)


			print(cuttingPoint)

			for j in range(int(iterations / 2)):

				index1 = (cuttingPoint * j * 2, cuttingPoint + cuttingPoint * j * 2)
				index2 = (cuttingPoint + cuttingPoint * j * 2, cuttingPoint * 2 + cuttingPoint * j * 2)

				new_text.append(text[i][index1[0]:index1[1]])
				new_text.append(text[i][index2[0]: index2[1]])



				new_box_coor.append([box_coor[i][0], round(box_coor[i][1] + fontScale[i]*80*j), box_coor[i][2], round(box_coor[i][3] + fontScale[i]*80*j)])
				new_box_coor.append([box_coor[i][0], round(box_coor[i][1] + fontScale[i]*40 + fontScale[i]*80*j), box_coor[i][2], round(box_coor[i][3] + fontScale[i]*40 + fontScale[i]*80*j)])

				newFontScale.append(fontScale[i])
				newFontScale.append(fontScale[i])

		else:
			new_text.append(text[i])
			new_box_coor.append(box_coor[i])

			newFontScale.append(fontScale[i])

	print(new_box_coor)
	print(new_text[2:])

	newNumOfTexts = range(len(new_box_coor))

	return new_box_coor, new_text, newNumOfTexts, newFontScale
			

			


if __name__ == "__main__":
	box_coor = [[36, 92, 618, 184], [36, 194, 597, 361]]
	img = cv2.imread("images\\test.png")
	text = ['Se trata de una gran cantidad de texto de 12 puntos para probar el código OCR y ver si funciona en todos los tipos de formato de archivo.', 
			'El veloz perro marrón saltó sobre el zorro perezoso. El veloz perro marrón saltó sobre el zorro perezoso. El veloz perro marrón saltó sobre el zorro perezoso. El veloz perro marrón saltó sobre el zorro perezoso.']

	replace_text(box_coor, text, img)

	cv2.imshow("img", img)
	cv2.waitKey(0)

