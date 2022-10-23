
from ast import Return
from dataclasses import dataclass
from datetime import datetime

import random
from SharedFunctions import Get_WordFamilyList,Algor_Method, Partition_Words

@dataclass() #(frozen=True, order=True)
class WordGuess:
    setLevel: str = "easy"
    gameComplete: bool = False
    guesses: int = 0
    wordFamilyList = []
    wordLength: int = 0
    CallAlgorithm: str = ""
    usedLetters = []
    wordDisplay: str = ""
    letterGuess: str = ""
    letterIndex: int = 0



    def setup(self):
        # getting the word size for word list and double for number of guesses
        self.wordLength = random.randrange(4,12)
        self.guesses = self.wordLength*2

        #open text file and save to list
        self.wordFamilyList = Get_WordFamilyList(self.wordLength)

        # asking user to set the level for the game.
        while True:
            answer = input("Would you like to play on easy mode y/n: ").lower()
            if answer == 'y':
                self.setLevel = "easy"
                print("Good choice, you may stand a chance")
                break
            elif answer == 'n':
                self.setLevel = "hard"
                print("Ok hard it is then, good luck")
                break
            else:
                print("Did not compute..try again")
            

    def wordGuess_game(self):
        # set algorithm to use and call when ever its actually created add letterGuess as param
        self.CallAlgorithm = Algor_Method(self.setLevel,self.wordFamilyList)
        self.usedLetters = ['a']
        self.wordDisplay = ['-'*self.wordLength]

        # put in while loop when ready 
        #loop = False
        #while game_complete == False
        print("You have {0} guesses left".format(self.guesses))
        print("Used letters so far: {0}".format(self.usedLetters))
        print("Word: ",self.wordDisplay)
        while True:
            self.letterGuess = input("Enter a letter: ").lower()
            if self.letterGuess.isalpha() == True & len(self.letterGuess) == 1:
                # if letter not already guessed then append
                if self.letterGuess in self.usedLetters:
                    print("This has already been guessed try again")
                    Return
                else:
                    self.usedLetters.append(self.letterGuess)
                    # add 1 to guesses when safe to append letter that has not been guessed already
                    self.guesses -= 1
                    break
            else:
                print("Eh computer says no, please try again")


        Partition_Words(self.wordFamilyList,self.wordLength,self.letterGuess,self.letterIndex)
        print("Good guess")


    def wordGuess_end(self):
        if self.guesses == 0:
            self.game_complete = True
            print("You have no guesses left, the computer has won..hoorah!")
        if "-" not in self.wordDisplay:
            print(self.wordDisplay)
            print("Well done you have guessed the word and beaten the computer")

newGame = WordGuess()

# call separate methods to test and then amalgamate them
def main():
    #Word guess game using an easy level (on-cheat) and hard level (cheat)
    now = datetime.now()
    displayDatetime = now.strftime("Date-> %d-%m-%Y, Time-> %H:%M")
    print(f"\n{displayDatetime}")

    print(f"Welcome to the Word Guess game\n")

    newGame.setup()
    newGame.wordGuess_game()
    newGame.wordGuess_end()
    

# this is how the program starts
if __name__ == '__main__':
    main()
    



