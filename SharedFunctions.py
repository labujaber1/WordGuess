from ast import Break, Return
from cgitb import text
import collections
from operator import countOf
import re
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
        new_list = [ word for word in wordFamilyList if len(word) == wordLen ]
        return new_list
    except FileNotFoundError:
        print(f"Dictionary file not found.")
        Return
    
    

#used to sort list by word length GetWordFamilyList()
#def ByWordLen(e):
    #return len(e)

def Algor_Method(e,f):
    #setLevel = 'easy' or 'hard',wordFamilyList = new_list from above, params

    return e


# not dependant on diff level so can be used by both algorithms
def Partition_Words(wordList,wordLength,letterGuess,letterIndex):
    
    # get list length
    wordListLen = len(wordList)
    print(f"Total number of words in the list is {wordListLen}")

    # works to give count of words do not contain a letterGuess
    '''res0 = len(list(filter(lambda ele : letterGuess not in ele, wordList)))
    print(f"Occurrence for no letter '{letterGuess }' = {res0}")'''
    
    # gives count of all words contain a letterGuess 
    '''res1 = len(list(filter(lambda ele : letterGuess in ele, wordList)))
    print(f"Occurrence for one letter '{letterGuess }' = {res1}")'''
    
    # Append count totals to a list of all occurrences of letterGuess between 0-3
    bool = True
    index2 = 0
    listTotal = []
    while bool == True:
        if index2 < 4:
            listOccurTotal = len(list(word for word in wordList if countOf(word,letterGuess) == index2))
            listTotal.append(listOccurTotal)
            #print(f"No. of letters = {index2}, and total words = {listTotal}")
            index2 += 1
        else:
            bool = False
    print(f"No. of letters = {index2}, and total words = {listTotal}")
    print(f"Number of word groups should equal 4 (letterGuess from 0-3): {len(listTotal)}") 
    #print(targetList)
    
    # select the largest count occurrence of the letterGuess param
    letterOccur = listTotal.index(max(listTotal))
    
    # if largest list of letter occurrence == zero (not contain the letter guessed)
    # then RETURN 'letter not guessed'
    if letterOccur == 0:
        ''' End function '''
        return print("letter not guessed")
        
    targetWordList = []
    # get all words from wordList param that is in the largest group of occurrences 
    # if not equal to zero. Add to new list targetWordList
    if letterOccur > 0: 
        targetWordList = [word for word in wordList if countOf(word,letterGuess) == letterOccur]
        print(f"Word length: {wordLength}, Max list of words for letter {letterGuess}: {len(targetWordList)}")
        print(f"Index {letterOccur = }") 
    
    # count occurrence of guessed letter for each index position in each word in the list
    # ------- SPLIT SECTION --------
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
            #print(f"{res=}")
        else:
            bool = False

    print(f"Letter occurrence in split list: {res}")

    letterOccurSplit = res.index(max(res))
    targetWordListSplit = []
    targetWordListSplit = [word for word in targetWordList if word[letterOccurSplit] == letterGuess]
    print(f"Word length still: {wordLength}, Max list of words for letter {letterGuess}: {len(targetWordListSplit)}")
    print(f"Index {letterOccurSplit = }") 
    # remove all from targetWordList that does not equal largest group where letterGuess 
    # is in position index

    # replace original param list wordList with end result targetWordList to process 
    # newly entered letterGuess from user
    # clear all lists 
    # RETURN index position, word list, guessed letter
    ## need to check positions of letterGuess what happens if list is 
    ## chosen that contains 2 letters as the counts look for 1 occur
    ## index position used to display guessed letter in wordDisplay var for user
    

