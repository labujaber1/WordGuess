from ast import Return
from dataclasses import dataclass
from datetime import datetime
import random
from SharedFunctions import Get_WordFamilyList, Algor_Method, Filter_wordList, addLetterToWordDisplay

@dataclass() #(frozen=True, order=True)
class WordGuess:
    setLevel = "easy"
    gameComplete = False
    guesses = 0
    wordFamilyList = []
    wordLength = 0
    CallAlgorithm = ""
    usedLetters = []
    wordDisplay = ""
    letterGuess = ""
    letterIndex = 0



    def setupLevel(self):
        # getting the word size for word list and double for number of guesses
        self.wordLength = random.randrange(4,12)
        self.guesses = self.wordLength*2

        #open text file and save to list
        self.wordFamilyList = Get_WordFamilyList(self.wordLength)
        print(f"Main list filtered by word length {self.wordLength} \nand returned new list length {len(self.wordFamilyList)}")
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
        self.usedLetters = []
        self.wordDisplay = '-'*self.wordLength

        # put in while loop when ready 
        game_complete = False
        while game_complete == False:
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
                        print(f"WordList length before function wordGuess line66 = {len(self.wordFamilyList)}")
                        # put partition_words function here?
                        # returning targetWordListSplit,letterOccurSplit,functionComplete
                        returnStuff = Filter_wordList(self.wordFamilyList,self.wordLength,self.letterGuess)
                        self.wordFamilyList = returnStuff[0]
                        letterGuessIdx = returnStuff[1]
                        functionComplete = returnStuff[2]
                        print(f"WordList length after function = {len(self.wordFamilyList)}")
                        print(f"Letter occurred index = {letterGuessIdx}, and function complete = {functionComplete}")
                        # when no letter matched letterOccurred is 0
                        if functionComplete == False:
                            self.usedLetters.append(self.letterGuess)
                            self.guesses -= 1
                            #print(f"Word display: {self.wordDisplay}")
                            Return
                        if functionComplete == True:
                            wordAmend = addLetterToWordDisplay(self.wordDisplay,letterGuessIdx,self.letterGuess)
                            self.wordDisplay = wordAmend
                            self.usedLetters.append(self.letterGuess)
                            # add 1 to guesses when safe to append letter that has not been guessed already
                            self.guesses -= 1
                            print(f"Word display: {self.wordDisplay}")
                        else:
                            print("Filter_wordList completeFunction is false")
                            break
                else:
                    print("Eh computer says no, please try again")
            if self.guesses == 0:
                self.wordGuess_end()
                
        #
        # first run with first guess need to include to above loop 
        # partition_words function returns 2: list (new word list) and int (letter index)
        #newWordList,displayWordIndex,done = Partition_Words(self.wordFamilyList,self.wordLength,self.letterGuess,self.letterIndex)
        # display word if letter guess is accepted

        print("Good guess")


    def wordGuess_end(self):
        if self.guesses == 0:
            self.game_complete = True
            print("You have no guesses left, the computer has won..hoorah!")
        if "-" not in self.wordDisplay:
            print(self.wordDisplay)
            print("Well done you have guessed the word and beaten the computer")
        else:
            return




newGame = WordGuess()

# call separate methods to test and then amalgamate them
def main():
    #Word guess game using an easy level (on-cheat) and hard level (cheat)
    now = datetime.now()
    displayDatetime = now.strftime("Date-> %d-%m-%Y, Time-> %H:%M")
    print(f"\n{displayDatetime}")

    print(f"Welcome to the Word Guess game\n")
    newGame.setupLevel()
    newGame.wordGuess_game()
    newGame.wordGuess_end() # only here to finish program while testing
    
    
    

# this is how the program starts
if __name__ == '__main__':
    main()
    



