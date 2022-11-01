from ast import Break, operator
from tkinter import Y
from colorama import Fore
from operator import *
import random
import operator
from xmlrpc.client import Boolean
import numpy as np
import pandas as pd

#At the start of the program

#read in dictionary.txt and sort by word length
#write new list of words from random length selector
#return new list for user to try and choose from
def get_WordFamilyList(wordLen):
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
    
# Add successful letter(s) 1 or 2 to word display
def addLetterToWordDisplay(wordDisplay,letterIndex,letterGuess):
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
def selectWinningWord(wordList):
    listLength = len(wordList)
    num = 0
    if listLength > 1:
        num = random.randrange(0,listLength)
    word = wordList[num]
    return word 

# Append COUNT totals to a list of all occurrences of letterGuess between 0-2
# how many times letter ie 'e' appears 0,1,2,3 times any more is no point
def getCountOfList(wordList1,letterGuess):
    bool = True
    index2 = 0
    listTotals = []
    while bool is True:
        if index2 < 4:
            listOccurTotal = len(list(word for word in wordList1 if countOf(word,letterGuess) == index2))
            listTotals.append(listOccurTotal)
            index2 += 1
        else:
            bool = False
    print(Fore.RED + f"Total times the letter {letterGuess} appears in word 0-3 times = {listTotals}")
    return listTotals

def defWordFamDict(targetWordList,letterGuess):
    wordFamily = dict()
    #temp = str(ele for word in targetWordList for ele in word if ele == letterGuess(ele = letterGuess) if ele != letterGuess(ele == '_'))
    #temp: str = temp1[0]
    
    for word in targetWordList:
        temp = ""
        for ele in word:
            if ele == letterGuess:
                temp += letterGuess
            else:
                temp += '-'
        if (temp not in wordFamily):
            wordFamily[temp] = 1
        else:
            wordFamily[temp] = wordFamily[temp] +1
    print(f"DefWordFamDict: {wordFamily = }")
    return wordFamily



# pass in a word list and filter according to the user letter guess return new list
def filter_wordList_easy(wordList,wordLength,letterGuess):
    wordList1: list = wordList
    functionComplete: Boolean = False #false
    ## ------ FIRST LIST SPLIT SECTION -------- ##
    ## ---- RULE: pick largest group of words that contain letter
    # COUNT THEN ADD TO LIST to save memory space and reduce process time 
    listTotal = getCountOfList(wordList1,letterGuess)
    # select the largest count occurrence of the letterGuess param
    letterOccur = int(listTotal.index(max(listTotal)))
    
    if letterOccur == 0:
        ''' End function '''
        # KEEP all words that don't contain the letter to list and return
        wordList1 = [word for word in wordList1 if countOf(word,letterGuess) == letterOccur]
        print(Fore.GREEN + "letter not in word, try again")
        return wordList1,letterOccur,functionComplete

    # if a letter is in list (letterOccur > 0) then continue...
    ## ------- SECOND LIST SPLIT SECTION -------- ##
    ## ----- RULE: Pick largest group of words where the index of the letter appears
    targetWordList = []
    if letterOccur > 0: 
        # list of words with largest count of letterGuess
        targetWordList = [word for word in wordList1 if countOf(word,letterGuess) == letterOccur]
        print(Fore.RED + f"Word length: {wordLength}, Max list of words for letter {letterGuess}: {len(targetWordList)}")
    
    if len(targetWordList) <= 10: ######################
        print(f"{targetWordList = }")

    # print all index occur of letterGuess for word display prep
    wordIdx1 = []
    wordIdx1 = wordListCountOccurEachIndex(wordLength,targetWordList,letterGuess)
    
    letterOccurSplitIdx = []
    # get index of letter if only 1 letterOccur for word display, word list already created line 111'ish
    if letterOccur == 1:
        letterOccurSplitIdx.append(wordIdx1.index(max(wordIdx1)))   # list with first largest letterOccur index position 
        print(f"index of max value in {letterOccurSplitIdx = }") 

    # get largest family indexes of letterGuess if letterOccur > 1
    if letterOccur >= 2:
        #return all word families
        family = defWordFamDict(targetWordList,letterGuess)
        #largestFamily1 = []
        #largestFamily1.append(enumerate(max(family,key=family.get)))
        # if more than two families only unpack 1st tuple 
        
        # choose best by max word count words not actually split yet
        largestFamily = max(family.items(), key=operator.itemgetter(1))[0]
        print(f"{largestFamily = }")
        
        
        #letterOccurSplitIdx.append(largestFamily.index(ele for ele in largestFamily if (ele in largestFamily) == letterGuess))
        # get indexes of best family to pass and get words line 158'ish
        count=-1
        for letter in largestFamily:
            count +=1
            if letter == letterGuess:
                # return each index of letterOccur, resorted to count
                letterOccurSplitIdx.append(count)
        print(f"Indexes of letterGuess in chosen family: {letterOccurSplitIdx =}")
    
    
    # add words according to largest group of words according to letterGuess count
    targetWordListSplit = []
    listLength = len(targetWordList)
    if letterOccur == 2:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0] and letterOccurSplitIdx[1]]== letterGuess]
        print(f"Check 2 occurrences of letter, print list ->\n{targetWordListSplit = } ")
    elif letterOccur == 3:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0] and letterOccurSplitIdx[1] and letterOccurSplitIdx[2]]== letterGuess]
        print(f"Check 3 occurrences of letter, print list ->\n{targetWordListSplit = } ")
    else:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess]
        print(f"List length else line 164 = {listLength}")        
    functionComplete = True 
    wordList1.clear()
    targetWordList.clear()
    return (targetWordListSplit,letterOccurSplitIdx,functionComplete) # filtered words above so may not need splitIdx num for word display
    

def wordListCountOccurEachIndex(wordLength,targetWordList,letterGuess):
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
    return res
    


def filter_wordList_hard(wordList,wordLength,letterGuess):

    #return (targetWordListSplit,letterOccurSplitIdx,functionComplete)
    return 'not ready yet'


