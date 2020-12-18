import cv2
import math

def replace_text(box_coor, text, img):
	font = cv2.FONT_HERSHEY_SIMPLEX
	numOfTexts = range(len(text))
	minFontScale = 0.6
	
	fontScale = [0 for i in numOfTexts]
	width = [box_coor[i][2] - box_coor[i][0] for i in numOfTexts]

	for i in numOfTexts:
		wordNum = len(text[i])
		
		characterLength = width[i]/wordNum if wordNum != 0 else 0
		
		scale = characterLength / 15

		fontScale[i] = scale if scale > minFontScale else minFontScale

	fontColor = (0, 0, 0)
	lineType = 2
	color = (255, 255, 255)
	


	new_box_coor, new_text, newNumOfTexts, newFontScale = new_line(box_coor, text, fontScale, numOfTexts, width)
	topLeftCorner = [(new_box_coor[i][0], new_box_coor[i][1]) for i in newNumOfTexts]


	
	for i in numOfTexts:
		cv2.rectangle(img, (box_coor[i][0], box_coor[i][1]), (box_coor[i][2], box_coor[i][3]), color, -1)
	
	for i in newNumOfTexts:
		cv2.putText(img, new_text[i], topLeftCorner[i], font, newFontScale[i], fontColor, lineType)
	
		


def new_line(box_coor, text, fontScale, numOfTexts, width):
	new_box_coor = []
	padding = 5
	new_text = []
	newFontScale = []


	for i in numOfTexts:
		print("num of characters: ",len(text[i]))
		print("fontScale: ",fontScale[i])
		print("width: ",width[i])

		if len(text[i]) * fontScale[i] * 15 > width[i]:
			cuttingPoint = math.floor(width[i]/(15*fontScale[i])) - padding
			print(cuttingPoint)

			iterations = math.ceil(len(text[i])/cuttingPoint)
			print("iter: ", iterations)

			snipping = 0
			spaceBetweenLines = 40
			for j in range(int(iterations)):
				snipped_text = text[i][snipping:snipping+cuttingPoint]
				new_text.append(snipped_text)

				snipping += cuttingPoint

				new_box_coor.append([box_coor[i][0], round(box_coor[i][1] + fontScale[i]*spaceBetweenLines*j), box_coor[i][2], round(box_coor[i][3] + fontScale[i]*spaceBetweenLines*j)])

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
	box_coor = [[210, 221, 498, 287], [767, 503, 896, 531], [50, 549, 445, 605]]
	img = cv2.imread("images\\test2.png")
	text = ['Hola chicos', 'Qué pasa', 'Esto es una prueba']

	replace_text(box_coor, text, img)

	cv2.imshow("img", img)
	cv2.waitKey(0)

