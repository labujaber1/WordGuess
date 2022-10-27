from ast import Break, Return

from dataclasses import dataclass
from datetime import datetime
import random
from colorama import Fore
from SharedFunctions import Get_WordFamilyList, Filter_wordList_easy, Filter_wordList_hard, addLetterToWordDisplay, selectWinningWord

@dataclass() #(frozen=True, order=True)
class WordGuess:
    setLevel = None
    game_complete = None
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
        print(Fore.RED + f"Main list filtered by word length {self.wordLength} \nand returned new list length {len(self.wordFamilyList)}")
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
            
    # main game loop easy level 
    def wordGuess_game(self):
       
        self.usedLetters = []
        self.wordDisplay = '-'*self.wordLength
        self.game_complete = False
        # start game loop till game complete is true
        while self.game_complete == False:
            #self.Rules()
            self.usedLetters.sort()
            print(Fore.CYAN+"You have {0} guesses left".format(self.guesses))
            print(Fore.CYAN+"Used letters so far: {0}".format(self.usedLetters))
            print(Fore.GREEN+"Word: ",self.wordDisplay)
            self.letterGuess = input(Fore.WHITE+"Enter a letter: ").lower()
            if self.letterGuess.isalpha() == True and len(self.letterGuess) == 1:
                # if letter not already guessed then append
                if self.letterGuess in self.usedLetters:
                    print(Fore.RED + "This has already been guessed try again")
                    Return
                # used filter_wordList as easy algorithm, need to relabel and include 
                # setlevel if else line 70, all others to be used as is
                elif self.guesses>0:
                    print(Fore.RED + f"WordList length before function wordGuess line66 = {len(self.wordFamilyList)}")
                    # returning in tuple: targetWordListSplit,letterOccurSplit,functionComplete
                    if self.setLevel == 'easy':
                        returnStuff = Filter_wordList_easy(self.wordFamilyList,self.wordLength,self.letterGuess)
                    if self.setLevel == 'hard':
                        returnStuff = Filter_wordList_easy(self.wordFamilyList,self.wordLength,self.letterGuess)
                        #returnStuff = Filter_wordList_hard(self.wordFamilyList,self.wordLength,self.letterGuess)
                    self.wordFamilyList, letterGuessIdx, functionComplete = returnStuff # unpack tuple
                    print(Fore.RED + f"WordList length after function = {len(self.wordFamilyList)}")
                    # when no letter matched letterOccurred is 0
                    if functionComplete is False:
                        self.usedLetters.append(self.letterGuess)
                        self.guesses -= 1
                    # if a letter is matched
                    elif functionComplete is True:
                        wordAmend = addLetterToWordDisplay(self.wordDisplay,letterGuessIdx,self.letterGuess)
                        self.wordDisplay = wordAmend
                        self.usedLetters.append(self.letterGuess)
                        #self.guesses -= 1 #used in testing 
                        print(Fore.GREEN+f"Word display: {self.wordDisplay}")
                    else:
                        #print(f"Filter_wordList completeFunction = {functionComplete}")
                        break
                    self.gameEndConditions()
            else:
                print(Fore.RED + "Eh computer says no, please try again")
            
                

    def wordGuess_end(self):
        word = selectWinningWord(self.wordFamilyList)
        if self.guesses == 0:
            self.game_complete = True
            print(Fore.GREEN+f"You have no guesses left,\nthe word you could not guess was {word}.")
            print(Fore.GREEN+"The computer has won..hoorah!")
        if "-" not in self.wordDisplay:
            print(self.wordDisplay)
            print(Fore.GREEN+"Well done you have guessed the word and beaten the computer.")
            print(Fore.GREEN+"\nOne bows to your superiority. \nVery well done.")
        else:
            return

    # crispy logic rules
    def gameEndConditions(self):
        if self.guesses == 0:
            self.game_complete = True
        if len(self.wordFamilyList) == 1 and self.guesses > 0:
            print(Fore.GREEN+f"The only word left is {self.wordFamilyList} you won well done")
            self.game_complete = True
        if len(self.wordFamilyList) == 1 and self.guesses == 0:
            print(Fore.GREEN+f"The only word left is {self.wordFamilyList}")
            self.game_complete = True
        if '-' not in self.wordDisplay:
            self.game_complete = True
        


# Issues and bugs
# if largest group involves more than 2 occurrences need to account for it as only one entered in word display
# set rules as not setout as crispy logic DONE
# 0 guesses still showing up DONE
# if all letters guessed and still have guesses does not end DONE
# set different algorithms for optimized easy and hard.
# add option to replay in main DONE
# sort guessed letters list DONE
# 

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
                
    

    
    
    

# this is how the program starts
if __name__ == '__main__':
    main()
    



