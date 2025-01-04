import random

what_range = input("Type a Maximum Range Number: ") 

if what_range.isdigit(): 
    what_range = int(what_range)
    if what_range <= 0:
        print("Please Type a Number Larger Than Zero Next Time.")
        quit()
else:
    print("Please Type a Number Next Time.")
    quit()

rNum = random.randint(0, what_range)
guesses = 0 # keeping track of guesses made by player

while True:
    guesses += 1 #add +1 for every guess the user makes 
    user_guess = input("Make a Guess: ")
    if user_guess.isdigit():
        user_guess = int(user_guess)
    else:
        print("Please Type a Number!")
        continue

    if user_guess == rNum:
        print("You Got It!")
        print("You Got It In", guesses, "guesses!")
        break # Exit loop if the guess is correct
    elif user_guess > rNum:
        print("You Are Above The Number!")
    else:
        print("You Are Below The Number!")