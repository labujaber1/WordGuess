############################################################################
##                                                                        ##
## Title: Word Guess Game                                                 ##
## Author: 2018481                                                        ##
## Date: 09/12/2022                                                       ##
## Description: Hangman without the graphics and a little bit of naughty  ##
## Version: 1.0                                                           ##
##                                                                        ##
############################################################################


from ast import operator
from collections import defaultdict
from colorama import Fore
from operator import *
import random
import operator
from xmlrpc.client import Boolean

# List of functions and line number
# get_WordDictList 269 addLetterToWordDisplay 41, selectWinningWord 54, getCountOfList 64,
# defWordFamDict 81, getLetterIdxInWord 114, scoreWord 124, filter_wordList 133, 
# filter_wordList_hard 198, getCountOfList 210, filterDuplicateLetters 294, 
# wordListCountOccurEachIndex 311, alphabetWeighting 331, weightingForEachFamily 362
#    
#read in dictionary.txt and sort by word length
#write new list of words from random length selector
#return new list for user to try and choose from
def get_WordDictList():
    try:
        my_file = open("dictionary.txt","r")
        wordDict  = my_file.read().split()
        my_file.close() # change to contact manager look it up
        #print(Fore.RED + f"Original list length = {len(wordFamilyList)}")
        return wordDict
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
    #print(Fore.RED + f"Total times the letter {letterGuess} appears in word 0-3 times = {listTotals}")
    return listTotals

# define pattern and count number of words to wordFamilyNum if letter occur = 1 (efficiency in mind for larger lists)
# or add word to wordFamilyWords as a list and score word if letter occur > 1 (as word list gets smaller)
# return both dictionaries
def defWordFamDict(targetWordList,letterGuess,letterOccur):
    wordFamilyNum = dict()
    wordFamilyWords = defaultdict(list)
    letterWeight = alphabetWeighting()
    for word in targetWordList:
        temp = ""
        for ele in word:
            if ele == letterGuess:
                temp += letterGuess
            else:
                temp += '-'
        if (temp not in wordFamilyNum and temp not in wordFamilyWords):
            # add count of matching words to wordFamilyNum
            if (letterOccur == 1):
                wordFamilyNum[temp] = 1
            else:
                # add word to wordFamilyWords if match pattern
                score = scoreWord(word,letterWeight)
                A = [word,score]
                wordFamilyWords[temp].append(A)
                #print(f"wordFamilyWords[temp].append(A) = {temp = }, {score = },{word = }")
        else:
            if (letterOccur == 1):
                wordFamilyNum[temp] = wordFamilyNum[temp] + 1
            else:
                # add each word as a separate list with score
                score = scoreWord(word,letterWeight)
                A = [word,score]
                wordFamilyWords[temp].append(A)
                #print(f"wordFamilyWords[temp] = wordFamilyWords[temp].append[word,score] = {temp = }, {score = },{word = }")
    return wordFamilyNum,wordFamilyWords

# return index of chosen letter
def getLetterIdxInWord(familyChoice,letterGuess):
    letterOccurSplitIdx = []
    count=-1
    for letter in familyChoice:
        count +=1
        if letter == letterGuess:
            letterOccurSplitIdx.append(count)
    return letterOccurSplitIdx

# give score for each word
def scoreWord(word,letterWeight:dict):
    # letterWeight is dict of alphabet scores
    letterScore = 0.0
    for letter in word:
        ls = [v for k,v in letterWeight.items() if k==letter]
        letterScore += ls[0]
    return letterScore

# pass in a word list and filter according to the user letter guess, return new list
def filter_wordList(wordList,wordLength,letterGuess):
    wordList1: list = []
    functionComplete: Boolean = False #false
    ## ------ FIRST LIST SPLIT SECTION -------- ##
    ## ---- RULE: pick largest group of words that contain letter, if hard then filter duplicate letters
    wordList1 = wordList
    # COUNT THEN ADD TO LIST to save memory space and reduce process time 
    listTotal = getCountOfList(wordList1,letterGuess)
    # select the largest count occurrence of the letterGuess param
    letterOccur = int(listTotal.index(max(listTotal)))
    if letterOccur == 0:
        ''' End function return to main '''
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
    # print all index occur of letterGuess for word display prep
    wordIdx1 = []
    wordIdx1 = wordListCountOccurEachIndex(wordLength,targetWordList,letterGuess)
    # best pattern
    familyChoice = []
    letterOccurSplitIdx = []
    # get index of letter if only 1 letterOccur for word display
    if letterOccur == 1:
        letterOccurSplitIdx.append(wordIdx1.index(max(wordIdx1)))   # list with first largest letterOccur index position 
    # get largest family indexes of letterGuess if letterOccur > 1 (optimise)
    if letterOccur >= 2:
        #return all word family patterns according to letterOccur and number of words that letter occurs
        wordFamilyNum,wordFamilyWords = defWordFamDict(targetWordList,letterGuess,letterOccur)
        # choose max word count for patterns
        if (len(wordFamilyNum)>0):
            largestFamily = max(wordFamilyNum.items(), key=operator.itemgetter(1))[0]
        else:
            # calculating best pattern by scoring words in each pattern
            optimizedPatternChoice = weightingForEachFamily(wordFamilyWords)
            largestFamily = max(optimizedPatternChoice.items(), key=operator.itemgetter(1))[0]
        familyChoice = largestFamily
        # get indexes of family choice to pass and get indices to use in word display
        letterOccurSplitIdx = getLetterIdxInWord(familyChoice,letterGuess)
    # add words according to largest group of words according to letterGuess count
    targetWordListSplit: list.clear
    # filter word list by index of letters in letterOccurSplitIdx
    targetWordListSplit = []
    if letterOccur == 2:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess and word[letterOccurSplitIdx[1]] == letterGuess]
    elif letterOccur == 3:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess and word[letterOccurSplitIdx[1]] == letterGuess and word[letterOccurSplitIdx[2]] == letterGuess]
    else:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess]
    functionComplete = True 
    wordList1.clear()
    targetWordList.clear()
    return (targetWordListSplit,letterOccurSplitIdx,functionComplete) # filtered words above so may not need splitIdx num for word display


# pass in a word list and filter according to the user letter guess, return new list
# try to reduce chance of duplicate letters and increase chance of 0 letters if its a reasonably large group
# add optimisation if large duplicate letter word group
def filter_wordList_hard(wordList,wordLength,letterGuess):
    wordList1: list = []
    functionComplete: Boolean = False #false
    ## ------ FIRST LIST SPLIT SECTION -------- ##
    ## ---- RULE: pick largest group of words that contain letter, if hard then filter duplicate letters
    # filter out words with duplicate chars if size greater than half the original list size
    if wordLength > 9 and wordLength < 12:
        wordList1 = filterDuplicateLetters(wordList)
        #print(f"Duplicate filter wordList length: {len(wordList1)}")
    else:
        wordList1 = wordList
        #print("No duplicate letter filter")

    # COUNT THEN ADD TO LIST to save memory space and reduce process time 
    listTotal = getCountOfList(wordList1,letterGuess)
    try:
        p=0
        if listTotal[1] != 0: 
            # if a small diff between 0 and 1 letter then choose 0 letter group else largest group
            p = (listTotal[0]/listTotal[1])*100 
        if p > 98:
            letterOccur = 0
            #print(f"In list percentage > 98 (line 207) = {p}")
        else:     
            # select the largest count occurrence of the letterGuess param
            letterOccur = int(listTotal.index(max(listTotal)))
    except Exception:
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
    #if letterOccur > 0: 
        # list of words with largest count of letterGuess
    targetWordList = [word for word in wordList1 if countOf(word,letterGuess) == letterOccur]
    #print(Fore.RED + f"Word length: {wordLength}, Max list of words for letter {letterGuess}: {len(targetWordList)}")
    # print all index occur of letterGuess for word display prep
    wordIdx1 = []
    wordIdx1 = wordListCountOccurEachIndex(wordLength,targetWordList,letterGuess)
    # best pattern
    familyChoice = []
    letterOccurSplitIdx = []
    # get index of letter if only 1 letterOccur for word display
    if letterOccur == 1:
        if wordLength >= 4 and wordLength < 9:
            letterOccurSplitIdx.append(wordIdx1.index(max(wordIdx1)))   # list with first largest letterOccur index position 
            #print(f"index of max value in {letterOccurSplitIdx = }")
        else:
            wordFamilyNum,wordFamilyWords = defWordFamDict(targetWordList,letterGuess,letterOccur)
            if len(wordFamilyNum) > 0:
                largestFamily = max(wordFamilyNum.items(), key=operator.itemgetter(1))[0]
                familyChoice = largestFamily
            else:
                optimizedPatternChoice = weightingForEachFamily(wordFamilyWords)
                minFamily = min(optimizedPatternChoice.items(), key=operator.itemgetter(1))[0]
                familyChoice = minFamily
    # get largest family indexes of letterGuess if letterOccur > 1 (optimise)
    if letterOccur >= 2:
        # return all word family patterns according to letterOccur and number of words that letter occurs
        wordFamilyNum,wordFamilyWords = defWordFamDict(targetWordList,letterGuess,letterOccur)
        # calculating best pattern by scoring words in each pattern
        optimizedPatternChoice = weightingForEachFamily(wordFamilyWords)
        minFamily = min(optimizedPatternChoice.items(), key=operator.itemgetter(1))[0]
        familyChoice = minFamily
    
    if len(letterOccurSplitIdx) == 0:
        # get indexes of family choice to pass and get indices to use in word display
        letterOccurSplitIdx = getLetterIdxInWord(familyChoice,letterGuess)
        #print(f"Indexes of letterGuess in chosen family: {letterOccurSplitIdx=}")
    
    # add words according to largest group of words according to letterGuess count
    targetWordListSplit: list.clear
    # filtered word list by index of letters in letterOccurSplitIdx
    targetWordListSplit = []
    if letterOccur == 2:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess and word[letterOccurSplitIdx[1]] == letterGuess]
        #print(f"Check 2 occurrences of letter, print list ->\n{targetWordListSplit = } ")
    elif letterOccur == 3:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess and word[letterOccurSplitIdx[1]] == letterGuess and word[letterOccurSplitIdx[2]] == letterGuess]
        #print(f"Check 3 occurrences of letter, print list ->\n{targetWordListSplit = } ")
    else:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess]
        #print(f"For single occurrence of letter. print list length = {len(targetWordList)}")        
    functionComplete = True 
    wordList1.clear()
    targetWordList.clear()
    return (targetWordListSplit,letterOccurSplitIdx,functionComplete) # filtered words above so may not need splitIdx num for word display

# strip wordList of any words with duplicate letters if size is not less than half size of original list 
def filterDuplicateLetters(wordList:list):
    newWordList = []
    #print(f"Word list before hard filter: {len(wordList)}") 
    # add words that don't have duplicate chars
    newWordList = [word for word in wordList if not len(word) > len(set(word))]
    #print(f"length hard word list: {len(newWordList)} ")
    tempLen:int=len(newWordList)
    wordListLen:int=len(wordList)
    percentage = (tempLen/wordListLen)*100
    # if filtered list with duplicate chars removed is less than half then don't use filtered list
    if (percentage > 50):
        return newWordList
    return wordList
        

# for each word in list count letterGuess in each index of word
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
    #print(Fore.RED + f"Letter occurrence in split list: {res}")
    return res

# for optimisation 
def alphabetWeighting():
        wordList  = get_WordDictList()
        alphabet = [
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t',
            'u','v','w','x','y','z']
        letterTotal = {}
        sumLetters = 0
        # get total occurrence each letter in alphabet in word list.
        for letter in alphabet:
            tot=0
            for word in wordList:
                if letter in word:
                    tot = tot + 1
            letterTotal[letter] = tot
        # total letters in word list summed from aWeighting dictionary 863600 letters
        sumLetters = sum(letterTotal.values()) 
        #print(f"Sum of all letters in dictionary: \n{sumLetters}") 

        # for each alphabet letter calc. weighting
        # total each letter / total letters * 10 to 2 d.p should give range 0 - 1
        # assign to new dictionary
        # first sort aWeighting by value
        res = {key: val for key, val in sorted(letterTotal.items(), key = lambda ele: ele[1], reverse = True)}
        #print(f" Result of sorted action: \n{res}")
        letterWeight = res
        letterWeight.update((x,round(y / sumLetters * 10,2 )) for x,y in letterWeight.items())
        #print(f"Letter weight update: \n{letterWeight}")
        #returns dict of weights for each word in the original dictionary
        return letterWeight

# for optimisation
def weightingForEachFamily(wordFamilyWords):
    #print("Starting weightingForEachFamily function")
    # when comparing which family to choose can calc weight for each word in family
    # and total for each family to choose the least which interprets as the 
    # least common letters in dictionary should make the hardest word to guess.
    dictOfPatternScore = {}
    score = 0
    # wordFamilyWords contain pattern with list of each [word , score],[word , score]
    # for each pattern sum each word score, index[1], add pattern and sum to dict.
    # Divide pattern sum by number of lists to get average, return dict
    wordFamily = wordFamilyWords
    for pattern in wordFamily:
        score = 0
        listCount = 0
        for list in wordFamily[pattern]:
            s = list[index(1)]
            score = round(score + s,2)
            listCount += 1
        if pattern not in dictOfPatternScore: 
            dictOfPatternScore[pattern] =  round(score / listCount,2)
        else:
            dictOfPatternScore[pattern] = round((dictOfPatternScore[pattern] + score) / listCount,2)
    # return dict of patterns and sum score of all matching words ie '_OO__' = 128
    #print(f"{dictOfPatternScore = }")
    return dictOfPatternScore

    