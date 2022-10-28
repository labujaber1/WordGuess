from colorama import Fore
from operator import countOf
import random
from xmlrpc.client import Boolean
import numpy as np
import pandas as pd

#At the start of the program

#read in dictionary.txt and sort by word length
#write new list of words from random length selector
#return new list for user to try and choose from
def Get_WordFamilyList(wordLen):
    try:
        my_file = open("dictionary.txt","r")
        wordFamilyList  = my_file.read().split()
        my_file.close() # change to contact manager look it up
        print(Fore.RED + f"Original list length = {len(wordFamilyList)}")
        new_list = [ word for word in wordFamilyList if len(word) == wordLen ]
        return new_list
    except FileNotFoundError:
        print(Fore.WHITE+f"Dictionary file not found.")
        return
    
# Add successful letter(s) 1 to 3 to word display
def AddLetterToWordDisplay(wordDisplay,letterIndex,letterGuess):
    word1=list(wordDisplay)
    word1[letterIndex[0]] = letterGuess
    if len(letterIndex)==2:
        word1[letterIndex[1]] = letterGuess
    if len(letterIndex)==3:
        word1[letterIndex[1]] = letterGuess 
        word1[letterIndex[2]] = letterGuess 
    word = ''.join(word1)
    return word
    
# if no guesses left select a word from remaining list to display for user
# make them think it was this word they were trying to guess all along
def SelectWinningWord(wordList):
    listLength = len(wordList)
    num = random.randrange(0,listLength)
    word = wordList[num]
    return word 

# not dependant on diff level so can be used by both algorithms
# pass in a word list and filter according to the user letter guess
# return new filtered word list with either a successful or failed guess result.
def Filter_wordList_easy(wordList,wordLength,letterGuess):
    # setup list to use
    wordList1: list = wordList
    functionComplete: Boolean = False #false
    # make new word list from param list reset length checker to zero
    paramWordListLen = 0
    wordList1Len = 0
    
    ####  get list length used in testing to check word list each cycle
    paramWordListLen = len(wordList)
    wordList1Len = len(wordList1)
    # check they match and nothing included from memory for testing
    res1 = wordList1Len - paramWordListLen
    if res1 != 0:
        raise Exception (Fore.RED + "Length of word lists do not match, cannot proceed\n")
    ### delete above when testing complete 

    ## ------ FIRST LIST SPLIT SECTION -------- ##
    ## ---- RULE: pick largest group of words that contain letter
    # COUNT THEN ADD TO LIST to save memory space and reduce process time 
    # Append COUNT totals to a list of all occurrences of letterGuess between 0-3
    # how many times letter ie 'e' appears 0,1,2,3 times any more is no point
    bool = True
    index2 = 0
    listTotal = []
    while bool is True:
        if index2 < 4:
            listOccurTotal = len(list(word for word in wordList1 if countOf(word,letterGuess) == index2))
            listTotal.append(listOccurTotal)
            index2 += 1
        else:
            bool = False
    print(Fore.RED + f"Total times the letter {letterGuess} appears in word 0-3 times = {listTotal}")
    # select the largest count occurrence of the letterGuess param
    letterOccur = int(listTotal.index(max(listTotal)))
    
    # if largest list of letter occurrence == zero (not contain the letter guessed)
    # then RETURN 'letter not guessed'
    if letterOccur == 0:
        ''' End function '''
        # KEEP all words that don't contain the letter to list and return
        wordList1 = [word for word in wordList1 if countOf(word,letterGuess) == letterOccur]
        print(Fore.GREEN + "letter not in word, try again")
        return wordList1,letterOccur,functionComplete

    # if a letter is in list (letterOccur > 0) then continue...
    ## ------- SECOND LIST SPLIT SECTION -------- ##
    ## ----- RULE: Pick largest group of words where the index of the letter appears
    # COUNT, THEN ADD TO LIST to save memory space and reduce process time
    targetWordList = []
    # get all words from wordList param that is in the largest group of occurrences 
    # if not equal to zero. ADD to new list targetWordList
    if letterOccur > 0: 
        targetWordList = [word for word in wordList1 if countOf(word,letterGuess) == letterOccur]
        print(Fore.RED + f"Word length: {wordLength}, Max list of words for letter {letterGuess}: {len(targetWordList)}")
        #print(f"Index {letterOccur = }") 
        
    # get count occurrence of guessed letter for each index position in each word in the list
    bool = True
    idx = 0 
    count = 0
    res = []
    while bool is True:
        if idx < wordLength:
            # for each word in list count letterGuess in each index of word
            for word in targetWordList:
                if word[idx] == letterGuess:
                    count = count + 1
            idx+=1
            res.append(count)
            count = 0
        else:
            bool = False
    print(Fore.RED + f"Letter occurrence in split list: {res}")

    # create list of words that have largest group of words where
    # letterGuess is in a certain position within wordLength
    letterOccurSplitIdx = []
    letterOccurSplitIdx.append(res.index(max(res)))   # change to list to take two indexes 
    
    # find second largest letter occurrences to filter list if letterOccur > 1
    if letterOccur == 2:
        res.sort()
        resSortSecBigVal:int = res[-2]# returning val or index?
        print(f"{resSortSecBigVal = }")
        letterOccurSplitIdx.append(res.index(resSortSecBigVal))
    ############## missing something here ?????????
    # append second largest position index
     
    targetWordListSplit = []
    listLength = len(targetWordList)
   
    # replace original param list wordList with end result targetWordListSplit to process 
    # newly entered letterGuess from user
    if listLength > 50:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess]
        print(f"List length > 50 line 149 = {listLength}")
    # start identifying 2 occurrences of a letter to display 
    # but may reduce list significantly but no choice, adjust list length to get balance
    elif listLength <= 50 and letterOccur == 2:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0] and letterOccurSplitIdx[1]]== letterGuess]
        print(f"Check 2 occurrences of letter, print list ->\n{targetWordListSplit = } ")
    elif listLength <= 50 and letterOccur == 3:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0] and letterOccurSplitIdx[1] and letterOccurSplitIdx[2]]== letterGuess]
        print(f"Check 2 occurrences of letter, print list ->\n{targetWordListSplit = } ")
    
    else:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess]
        print(f"List length else line 164 = {listLength}")        
    #if completed with letter return true else already returned false line 89
    functionComplete = True 
     # clear PREVIOUS USED temp word lists ready to pass in for next cycle  
    wordList1.clear()
    targetWordList.clear()
    # RETURN new word list,index position of successful letter, and function complete marker (true/false)
    return (targetWordListSplit,letterOccurSplitIdx,functionComplete) # filtered words above so may not need splitIdx num for word display
    ## index position used to display guessed letter in wordDisplay var for user
    

def Filter_wordList_hard(wordList,wordLength,letterGuess):

    #return (targetWordListSplit,letterOccurSplitIdx,functionComplete)
    return 'not ready yet'
