""" Bulls and Cows (also known as Cows and Bulls or Pigs and Bulls or Bulls and Cleots) is an old code-breaking mind or paper and pencil game for two or more players, predating the similar commercially marketed board game Mastermind.
The numerical version of the game is usually played with 4 digits, but can also be played with 3 or any other number of digits.

On a sheet of paper, the players each write a 4-digit secret number. The digits must be all different. Then, in turn, the players try to guess their opponent's number who gives the number of matches. If the matching digits are in their right positions, they are "bulls", if in different positions, they are "cows". Example:

Secret number: 4271
Opponent's try: 1234
Answer: 1 bull and 2 cows. (The bull is "2", the cows are "4" and "1".)
The first one to reveal the other's secret number wins the game. As the "first one to try" has a logical advantage, on every game the "first" player changes. In some places, the winner of the previous game will play "second". Sometimes, if the "first" player finds the number, the "second" has one more move to make and if he also succeeds, the result is even.

The game may also be played by two teams of 2–3 players. The players of every team discuss before making their move, much like in chess.

A computer program moo, written in 1970 by J. M. Grochow at MIT in the PL/I computer language for the Multics operating system, was amongst the first
 Bulls and Cows computer implementations, inspired by a similar program written by Frank King in 1968 and running on the Cambridge University mainframe.
 Because the game has simple rules, while it is difficult and entertaining, there are many computer variants; it is often included in telephones and PDAs.

It is proven that any number could be solved using up to seven turns. Minimal average game length is 26274/5040=5.2131 turns

Below Class can be used to create your own game.
"""
from sys import exit
from random  import sample
class cowbull(object):
	
	def __init__(self):
		
		self.chance=0
		self.secret_number = sample(range(1, 10),4)

	def input_validation(self, input_number):
		
		if len(input_number) != 4:
##			print ("Enter 4 digit number.")   ## Input should be 4 digit number.
			return 1
		elif len(input_number) > len(set(input_number)): ## checking uniqueness input_numbers.
##			print ("Enter all 4 unique digits.")
			return 2
		elif 0 in input_number:    ## Input should not contain 0.
##			print ("Input should not contain 0.")
			return 3
		else:
			return 0

	def count_bull(self, input_number):

		num_bull=0
		
		for i in (range(len(input_number))):
			if self.secret_number[i]==input_number[i]:
				num_bull+=1
		return num_bull
		

	def count_cow(self, input_number):

		num_cow=0

		for i in range(len(input_number)):
			temp_input_number = []
			for j in range(len(input_number)):
				temp_input_number.append(input_number[j])
			del temp_input_number[i]
			if self.secret_number[i] in temp_input_number:
				num_cow+=1
		return num_cow
		
""" Sample game code """

""" Start

cb_ins=cowbull()

k=0
while (True):
	
	try:
		in_num=raw_input("Chance " + str(k + 1) + ": " )
		if in_num == "0":
			exit()
		input_number=map(int, str(in_num))

	except:
		if in_num == "0":
			exit(0)
		print "Enter valid number"
		print ""
		continue

	if cb_ins.input_validation(input_number) > 0:
		print ""
		continue
	
	cow=cb_ins.count_cow(input_number)
	bull=cb_ins.count_bull(input_number)
	print str(cow) + " Cow, " + str (bull) + " Bull."
	print ""
	
	if cow == 4:
		break
	
	k=k+1
	
	if k==10:
		print "secret_number: " 
		print cb_ins.secret_number
		print "Try next time."
		exit(0)

print "You got it."


End """