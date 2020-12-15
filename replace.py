import cv2

def replace_text(box_coor, text, img):
	font = cv2.FONT_HERSHEY_SIMPLEX
	
	fontScale = [(box_coor[i][3] - box_coor[i][1])/30 for i in range(len(box_coor))]
	fontScale[3] = 1.2
	print(fontScale)
	fontColor = (0, 0, 0)
	lineType = 2
	color = (255, 255, 255)
	bottomLeftCorner = [(box_coor[i][0], box_coor[i][3]) for i in range(len(box_coor))]

	
	for i in range(len(box_coor)):
		cv2.rectangle(img, (box_coor[i][0], box_coor[i][1]), (box_coor[i][2], box_coor[i][3]), color, -1)
		cv2.putText(img, text[i], bottomLeftCorner[i], font, fontScale[i], fontColor, lineType)

		

if __name__ == "__main__":
	box_coor = [[1, 14, 95, 40], [167, 218, 954, 284], [930, 453, 1172, 473], [368, 482, 1178, 527]]
	img = cv2.imread("images\\test_spa2.png")
	text = ['español', 'Hello, my name is Paul.', "I'm fine. Pleasure.", 'How are you? This is a test. I do not speak.']
	print(len(text[3]))
	replace_text(box_coor, text, img)

	cv2.imshow("img", img)
	cv2.waitKey(0)

