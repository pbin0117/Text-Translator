from image_to_text import image_to_text
from translate import translate
from replace import replace_text
import time
import cv2


startTime = time.time()

img = cv2.imread("images\\test4.png")

print("load time: ", str(round(time.time() - startTime, 3)), "s")

sentences, box_coor = image_to_text(img, "eng")

print('box coor: ', str(box_coor))


translations = translate(sentences, 'es')

print(translations)

replace_text(box_coor, translations, img)

print("run time: ", str(round(time.time() - startTime, 3)), "s")

cv2.imshow("img", img)
cv2.waitKey(0)
