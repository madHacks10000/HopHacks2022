#importing modules
import pytesseract
from PIL import Image
import sys
import cv2
import enchant
from collections import deque
import numpy as np
import re
import time


"""
Usage:
	When calling im_to_text add file path as a string in command line following function name

Test Paths
	r"C:/Users/OwenJ/OneDrive/Desktop/realistic-receipt-template_23-2147938550.jpg"



NOTE: CREDIT CARD HAWS A 4 digit size --> implement this please and thanks

"""




global name_stopwords
name_stopwords = ["addr","address","date","time"]
global d
d = enchant.DictWithPWL("en_US","mywords.txt")
global card_words
card_words = ["number", "acount","credit","card","bank","visa","amex","chip"]
global total_words
total_words = ["sum","total","owed","amount","amex","visa"]
global month_to_digit
month_to_digit = {"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06","jul":"07","aug":"08","sep":"09","oct":"10","nov":"11","dec":"12"}

def isTimeFormat(inp):
	inp = inp.replace("p","").replace("pm","").replace("a","").replace("am","")
	try:
		time.strptime(inp, '%H:%M')
		return True
	except ValueError:
		try:
			time.strptime(inp, '%H:%M:%S')
			return True
		except ValueError:
			return False

def fix_month(word,splitter):
	tword = word.split(splitter)
	word = ""
	for count, part in enumerate(tword):
		if part in month_to_digit.keys():
			part = month_to_digit[part]
		if count < 2 and len(part) <2 and part.isnumeric():
			part = '0' + part
		if count == 2 and len(part) == 2 and part.isnumeric():
			part = '20' + part
		word+=part+splitter
	return word[:-1]

def check_date(date_buffer):
	full_string = ""

	#used to detect date
	correct_slashes = (date_buffer[2] == date_buffer[5] == "/" or date_buffer[2] == date_buffer[5] == "-")
	dmy_check = True

	#run through buffer
	for x in range(len(date_buffer)):
		full_string += date_buffer[x]
		#checks for correct date month and year
		# if (dmy_check and x != 2 and x!= 5):
		# 	if (not date_buffer[x].isnumeric()):
		# 		dmy_check == False
	if (dmy_check == correct_slashes == True):
		return full_string
	return None
		

def process_text(raw_text):
	#init returned values
	store_name = date = time = total = card_number = ""

	#used to keep track of 8 most recent chars to see if we found a valid date/time
	date_buffer = deque(maxlen=10)

	date_buffer.extend(["" for x in range(10)])

	#used to see if we are still in the part that lists the name
	in_name = False
	name_done = False

	#used to see if we are in the part that lists the card number
	in_card = False
	found_digit = False #sees if we found any digits for the credit card number
	card_done = False

	#used to see if we are in the part that lists the total
	in_total = False
	found_digit_tot = False #sees if we found any digits for the total
	total_done = False

	#used to check for additional information about the time
	AM_PM_Check = False

	#begin check
	for count, word in enumerate(raw_text.split()):
		if word != "":
			word = word.lower()
			word = word.strip("$#@!%^&*()~`’'\"'")

			#fix strange date formats
			if '-' in word:
				word = fix_month(word,'-')
			if '/' in word:
				word = fix_month(word,'/')

			if word !="" and d.check(word) and not name_done:
				in_name = True
			#find store name
			if in_name and (word in name_stopwords or not d.check(word) or word.isnumeric()):
				in_name = False
				name_done = True
			if in_name:
				store_name+=word+" "

			#look for date or time
			for char in word:
				date_buffer.append(char)
			dt = check_date(date_buffer)
			if (dt!=None):
				date = dt
			if (AM_PM_Check == True):
				AM_PM_Check == False
				if (word == "am" or word == "pm" or word == "p" or word == "a"):
					time += " " + word
			if (isTimeFormat(word)):
				time = word
				AM_PM_Check = True
		


		#detect credit card number
		if (not card_done):
			if (in_card and ((not word.isnumeric()) and d.check(word))):
				in_card = False
				print("CLOSE")
				if (found_digit):
					print("DONE")
					card_done = True
			if word.strip(":-;") in card_words:
				print("FOUND")
				in_card = True
				card_number = ""
			elif (in_card and word.strip("¥hx*#k. ").isnumeric()): 
				print("ADDED")
				card_number+=word.strip("¥hx*#k. ")
				found_digit = True


		#detect total
		if (not total_done):
			if word in total_words:

				in_total = True
				total = ""
			if (in_total and (not np.prod([word.replace("$",'.').split(".")[x].isnumeric() for x in range(len(word.replace("$",'.').split(".")))]) and found_digit_tot and d.check(word))):

				in_total = False
				if (found_digit_tot):
					total_done = True
			elif (in_total and np.prod([word.replace("$",'.').split(".")[x].isnumeric() for x in range(len(word.replace("$",'.').split(".")))])): 
				total+=word
				found_digit_tot = True


		print(word)
	print(raw_text)
	print("Store Name:", store_name)
	print("Date:",date)
	print("Time:",time)
	print("Total:",total)
	print("Card Number:",card_number)
	return [store_name,date,time,total,card_number]

if __name__ == '__main__':
	count = 1
	for arg in sys.argv[1:]:
		#do work with arg! arg is a string type!
		with open(arg) as fp:
			print("Processing Receipt #" + str(count))
			# If you don't have tesseract executable in your PATH, include the following:
			pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
			
			# img = Image.open(arg)
			img = cv2.imread(arg)

			img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			kernel = np.ones((1,1), np.uint8)
			img = cv2.dilate(img, kernel, iterations=1)
			img = cv2.erode(img, kernel, iterations=1)

			img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]




			#converting image to text
			raw_text = pytesseract.image_to_string(img,)
			synth_text = process_text(raw_text)
		print()
		count+=1

