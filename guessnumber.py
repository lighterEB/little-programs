# coding:utf-8
import random
import time
import sys


promit = """
************************************************************\t
Program:Guess Number
Author:\tCheng_CN
Date:\t2018-05-11
description：I will let you guess my number in my heart，\t
             you have three chance to guess,here we go!\t
************************************************************\t
"""


def SecretNum():
	robotnum = random.randint(1,100)
	return robotnum

def GetNum():
	while True:
		usernum = input("Please input the number you want to guess：")
		try:
			if 1 <= int(usernum) <= 100:
				return usernum
				break
			else:
				print("You must input 1 to 100 number! Please Try Again!")
				continue
			
		except:
			print("Please Input Number!")
			continue
			
	return

def main():
	print(promit)
	while True:
		
		try:
			entry = input("choose:\t1.start game\t\n\t2.quit game\t\n")
			if int(entry) == 1:
				live = 3
				robotnum = SecretNum()
				while live >= 1:
					print("you have %d chance."% live)
					user = GetNum()
					if int(user) > robotnum:
						live -= 1
						print("the number is more than my number,try again!\n")
						continue
					elif int(user) < robotnum:
						live -= 1
						print("the number is less than my number,try again!\n")
						continue
					elif int(user) == robotnum:
						print("congratulations!you guessed it! the truth number is %d!\n" % robotnum)
						break
				if live == 0:
					print("sorry man,you used out your chance, the truth number is %d!\n" % robotnum)
					time.sleep(1)
					print("\n")
			elif int(entry) == 2:
				print("the program will be exit...")
				time.sleep(1)
				break
				sys.exit(0)
			else:
				print("Entry Error!")
				continue

		except KeyboardInterrupt:
			sys.exit(0)
		except:
			print("You must input number and not another type! Please try again!")
		
						
if __name__ == "__main__":
	main()


		
	