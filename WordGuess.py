############################################################################
##                                                                        ##
## Title: Word Guess Game                                                 ##
## Author: 2018481                                                        ##
## Date: 09/12/2022                                                       ##
## Description: Hangman without the graphics and a little bit of naughty  ##
## Version: 1.0                                                           ##
##                                                                        ##
############################################################################

from ast import Return
from dataclasses import dataclass
from datetime import datetime
from numpy.random import choice
from colorama import Fore
from SharedFunctions import get_WordDictList, filter_wordList, filter_wordList_hard, addLetterToWordDisplay, selectWinningWord

# Function list and line number
# setupLevel 34, wordGuess_game 64, wordGuess_end 112, gameEndConditions 126, 
# main 143, randomC 167


@dataclass() #(frozen=True, order=True)
class WordGuess:
    setLevel = None
    game_complete = None
    guesses = 0
    wordFamilyList = []
    wordLength = 0
    usedLetters = []
    wordDisplay = ""
    letterGuess = ""
    letterIndex = 0

    def setupLevel(self):
        # getting the word size for word list and double for number of guesses
        self.wordLength = randomC()
        self.guesses = self.wordLength*2

        #open text file and save to list
        wordDict = get_WordDictList() 
        if len(wordDict) > 0:
            self.wordFamilyList = [ word for word in wordDict if len(word) == self.wordLength ]
        else:
            print("Program ending")
            return
        #print(Fore.RED + f"Main list filtered by word length {self.wordLength} \nand returned new list length {len(self.wordFamilyList)}")
        # asking user to set the level for the game.
        while True:
            answer = input(Fore.CYAN+"Would you like to play on easy mode y/n: ").upper()
            if answer == 'Y':
                self.setLevel = "easy"
                print(Fore.YELLOW+"Good choice, you may stand a chance")
                break
            elif answer == 'N':
                self.setLevel = "hard"
                print(Fore.YELLOW+"Ok hard it is then, good luck")
                break
            else:
                print(Fore.RED+"Did not compute..try again")

    

    # main game loop
    def wordGuess_game(self):
       
        self.usedLetters = []
        self.wordDisplay = '-'*self.wordLength
        self.game_complete = False
        # start game loop till game complete is true
        while self.game_complete == False:
            self.usedLetters.sort()
            if self.guesses == 1:
                print(Fore.CYAN+"\nYou have {0} guess left".format(self.guesses))
            else:
                print(Fore.CYAN+"\nYou have {0} guesses left".format(self.guesses))
            print(Fore.CYAN+"Used letters so far: {0}".format(self.usedLetters))
            print(Fore.GREEN+"Word: ",self.wordDisplay)
            self.letterGuess = input(Fore.WHITE+"Enter a letter: ").lower()
            if self.letterGuess.isalpha() == True and len(self.letterGuess) == 1:
                # if letter not already guessed then append
                if self.letterGuess in self.usedLetters:
                    print(Fore.RED + "This has already been guessed try again")
                    Return
                elif self.guesses>0:
                    #print(Fore.RED + f"WordList length before function wordGuess line66 = {len(self.wordFamilyList)}")
                    # returning in tuple: targetWordListSplit,letterOccurSplit,functionComplete
                    if self.setLevel == 'easy':
                        returnStuff = filter_wordList(self.wordFamilyList,self.wordLength,self.letterGuess)
                    if self.setLevel == 'hard':
                        returnStuff = filter_wordList_hard(self.wordFamilyList,self.wordLength,self.letterGuess)
                    self.wordFamilyList, letterGuessIdx, functionComplete = returnStuff # unpack tuple
                    #print(Fore.RED + f"WordList length after function = {len(self.wordFamilyList)}")
                    # when no letter matched letterOccurred is 0
                    if functionComplete is False:
                        self.usedLetters.append(self.letterGuess)
                        self.guesses -= 1
                    # if a letter is matched
                    elif functionComplete is True:
                        wordDisplayAmend = addLetterToWordDisplay(self.wordDisplay,letterGuessIdx,self.letterGuess)
                        self.wordDisplay = wordDisplayAmend
                        self.usedLetters.append(self.letterGuess)
                        self.guesses -= 1
                        print(Fore.GREEN+f"Word display: {self.wordDisplay}")
                    else:
                        #print(f"Filter_wordList completeFunction = {functionComplete}")
                        break
                    self.gameEndConditions()
            else:
                print(Fore.RED + "Eh computer says no, please try again")
            
                
    # end game messages
    def wordGuess_end(self):
        word = selectWinningWord(self.wordFamilyList)
        if self.guesses == 0:
            self.game_complete = True
            print(Fore.GREEN+f"You have no guesses left,\nthe word you could not guess was {word}.")
            print(Fore.GREEN+"The computer has won..hoorah!")
        if "-" not in self.wordDisplay:
            print(self.wordDisplay)
            print(Fore.GREEN+"Well done you have guessed the word and beaten the computer.")
            print(Fore.GREEN+"One bows to your superiority. __!==O__ \nVery well done.")
        else:
            return

    # conditions to end the game
    def gameEndConditions(self):
        if self.guesses == 0:
            self.game_complete = True
        if len(self.wordFamilyList) <= 1 and self.guesses == 0:
            print(Fore.GREEN+f"The only word left is {self.wordFamilyList}")
            self.game_complete = True
        if '-' not in self.wordDisplay:
            self.game_complete = True
        if len(self.wordFamilyList) == 0:    
            # don't want to throw Exception but carry on with another try   
            print(Fore.GREEN+f"Sorry, something seems to have gone wrong.") 
            self.game_complete = True 

newGame = WordGuess()

# call separate methods to test and then amalgamate them
def main():
    ans = 'y'
    while ans == 'y':
        #Word guess game using an easy level (on-cheat) and hard level (cheat)
        now = datetime.now()
        displayDatetime = now.strftime(Fore.BLUE+"Date-> %d-%m-%Y, Time-> %H:%M")
        print(Fore.BLUE+f"\n{displayDatetime}")
        print(Fore.CYAN+f"Welcome to the Word Guess game\n")
        #newGame.alphabetWeighting()
        newGame.setupLevel()
        newGame.wordGuess_game()
        newGame.wordGuess_end() 
        while True:
            try:
                ans = input("Would you like to play again y/n: ").lower()
                if ans == 'y':
                    break
                elif ans == 'n':
                    print("Thankyou for playing. \nHave a nice day.")
                    exit() 
            except ValueError:
                print("Don't understand, try again")

# sneaky stuff 
def randomC():
    numList = [4,5,6,7,8,9,10,11,12]
    numL = choice(numList, 1, p=[0.15,0.15,0.15,0.13,0.12,0.1,0.1,0.05,0.05])
    num = numL[0]
    return num

# this is how the program starts calling main function 
if __name__ == '__main__':
    main()
    



