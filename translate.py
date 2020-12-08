from googletrans import Translator
import time

def translate(text, lang):
	translator = Translator()

	translations = translator.translate(text, dest=lang)
	actual_translations = [x.text for x in translations]

	return actual_translations

if __name__ == "__main__":
	startTime = time.time()

	text = ['The quick brown fox', 'jumps over', 'the lazy dog']
	print(translate(text, 'ko'))

	print("run time: ", str(round(time.time() - startTime, 3)), "s")
