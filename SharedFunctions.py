from ast import Break, Return
from operator import countOf
import re
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
        my_file.close()
        print(f"Original list length = {len(wordFamilyList)}")
        new_list = [ word for word in wordFamilyList if len(word) == wordLen ]
        return new_list
    except FileNotFoundError:
        print(f"Dictionary file not found.")
        return
    
    

#used to sort list by word length GetWordFamilyList()
#def ByWordLen(e):
    #return len(e)

def Algor_Method(e,f):
    #setLevel = 'easy' or 'hard',wordFamilyList = new_list from above, params

    return e


# not dependant on diff level so can be used by both algorithms
# pass in a word list and filter according to the user letter guess
# return new filtered word list with either a successful or failed guess result.
def Filter_wordList(wordList,wordLength,letterGuess):
    # setup list to use
    wordList1: list = wordList
    functionComplete: Boolean = False #false
    # make new word list from param list reset length checker to zero
    paramWordListLen = 0
    wordList1Len = 0
    
    ####  get list length used in testing to check word list each cycle
    paramWordListLen = len(wordList)
    wordList1Len = len(wordList1)
    print(f"Total number of words in the param list is {wordList1Len}\nnew list length is {paramWordListLen}\n")
    # check they match and nothing included from memory for testing
    res1 = wordList1Len - paramWordListLen
    if res1 != 0:
        raise Exception ("Length of word lists do not match, cannot proceed\n")
    ### delete above when testing complete 

    ## ------ FIRST LIST SPLIT SECTION -------- ##
    ## ---- RULE: pick largest group of words that contain letter
    # COUNT THEN ADD TO LIST to save memory space and reduce process time 
    # Append COUNT totals to a list of all occurrences of letterGuess between 0-3
    # how many times letter ie 'e' appears 0,1,2,3 times any more is no point
    bool = True
    index2 = 0
    listTotal = []
    while bool == True:
        if index2 < 4:
            listOccurTotal = len(list(word for word in wordList1 if countOf(word,letterGuess) == index2))
            listTotal.append(listOccurTotal)
            #print(f"No. of letters = {index2}, and total words = {listTotal}")
            index2 += 1
        else:
            bool = False
    print(f"Total times the letter {letterGuess} appears in word 0-3 times = {listTotal}")
    # select the largest count occurrence of the letterGuess param
    letterOccur = int(listTotal.index(max(listTotal)))
    
    # if largest list of letter occurrence == zero (not contain the letter guessed)
    # then RETURN 'letter not guessed'
    if letterOccur == 0:
        ''' End function '''
        # add all words to list and return
        wordList1 = [word for word in wordList1 if countOf(word,letterGuess) == letterOccur]
        print("letter not in word, try again")
        return wordList1,letterOccur,functionComplete
        


    ## ------- SECOND LIST SPLIT SECTION -------- ##
    ## ----- RULE: Pick largest group of words where the index of the letter appears
    # COUNT THEN ADD TO LIST to save memory space and reduce process time

    targetWordList = []
    # get all words from wordList param that is in the largest group of occurrences 
    # if not equal to zero. ADD to new list targetWordList
    if letterOccur > 0: 
        targetWordList = [word for word in wordList1 if countOf(word,letterGuess) == letterOccur]
        print(f"Word length: {wordLength}, Max list of words for letter {letterGuess}: {len(targetWordList)}")
        print(f"Index {letterOccur = }") 
        
    # get count occurrence of guessed letter for each index position in each word in the list
    bool = True
    idx = 0 
    count = 0
    res = []
    while bool == True:
        if idx < wordLength:
            # for each word in list count letterGuess in each word index
            for word in targetWordList:
                if word[idx] == letterGuess:
                    count = count + 1
                #res = [idx for idx in targetWordList if idx[num].lower() == letterGuess.lower()]
            idx+=1
            res.append(count)
            count = 0
        else:
            bool = False

    print(f"Letter occurrence in split list: {res}")

    # create list of words that have largest group of words where
    # letterGuess is in a certain position within wordLength
    letterOccurSplitIdx = res.index(max(res))
    targetWordListSplit = []
    targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx] == letterGuess]
    print(f"Word length still: {wordLength}, Max list of words for letter {letterGuess}: {len(targetWordListSplit)}")
    print(f"Index {letterOccurSplitIdx = }") 
    #if completed with letter return true else already returned false line 89
    functionComplete = True #true
    # replace original param list wordList with end result targetWordListSplit to process 
    # newly entered letterGuess from user
    
    # clear PREVIOUS USED temp word lists ready to pass in for next cycle  
    wordList1.clear()
    targetWordList.clear()
    print("Ending Filter_WordList function")
    # RETURN new word list,index position of successful letter, and function complete marker (true/false)
    return (targetWordListSplit,letterOccurSplitIdx,functionComplete)
    ## index position used to display guessed letter in wordDisplay var for user
    
# Add successful letter guessed to word to display to user 
# index out of range for successful last letter and not adding entire word length,
# and not concatenating successful guesses, bit of a cock up really!  
def addLetterToWordDisplay(wordDisplay,letterIndex,letterGuess):
    print(f"Printing word display before trying to add letters -> {wordDisplay}")
    word = wordDisplay
    #word = word[:letterIndex]+letterGuess+word[letterIndex]+wordLength-letterIndex
    word = word[:letterIndex]+letterGuess+word[letterIndex]
    print("Ending addLetterToWordDisplay function")
    return word




