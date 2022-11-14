from ast import Break, operator
from collections import defaultdict
from tkinter import Y
from colorama import Fore
from operator import *
import random
import operator
from xmlrpc.client import Boolean

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

# define pattern and count number of words to wordFamilyNum if letter occur = 1 (efficiency in mind for larger lists)
# or add word to wordFamilyWords as a list and score word if letter occur > 1 (as word list gets smaller)
# return both dictionaries
def defWordFamDict(targetWordList,letterGuess,letterOccur):
    wordFamilyNum = dict()
    wordFamilyWords = defaultdict(list)
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
                score = scoreWord(word)
                A = [word,score]
                wordFamilyWords[temp].append(A)
                print(f"wordFamilyWords[temp].append(A) = {temp = }, {score = },{word = }")
        else:
            if (letterOccur == 1):
                wordFamilyNum[temp] = wordFamilyNum[temp] + 1
            else:
                # add each word as a separate list with score
                score = scoreWord(word)
                A = [word,score]
                wordFamilyWords[temp].append(A)
                print(f"wordFamilyWords[temp] = wordFamilyWords[temp].append[word,score] = {temp = }, {score = },{word = }")
                
    print(f"DefWordFamDict: {wordFamilyNum = }")
    print(f"DefWordFamDict: {wordFamilyWords = }")
    return wordFamilyNum,wordFamilyWords

def scoreWord(word):
    letterWeight = alphabetWeighting()
    letterScore = 0.0
    for letter in word:
        ls = [v for k,v in letterWeight.items() if k==letter]
        letterScore += ls[0]
    return letterScore


# pass in a word list and filter according to the user letter guess, return new list
def filter_wordList_easy(setLevel,wordList,wordLength,letterGuess):
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
    
    if len(targetWordList) <= 10: ###################### delete after testing
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
        #return all word family patterns according to letterOccur and number of words that letter occurs
        wordFamilyNum,wordFamilyWords = defWordFamDict(targetWordList,letterGuess,letterOccur)
        # calculating best pattern by scoring words in each pattern
        optimizedPatternChoice = weightingForEachFamily(wordFamilyWords)
        # best pattern
        familyChoice = []
        ########### MAYBE FOR HARD LEVEL RATHER DO SOMETHING ELSE ##############
        if setLevel == 'hard':
            print(f"Hard level selected: {setLevel = }")
            # get weight for each letter
            #letterWeight = alphabetWeighting() ##used scoreWord
            # get patterns with sum score of each matching word set 
            ## optimizedPatternChoice = weightingForEachFamily(wordFamilyWords)
            # select pattern to use that equals the least score sum 
            minFamily =  min(optimizedPatternChoice.items(), key=operator.itemgetter(1))[0]
            familyChoice = minFamily
        else:
          # choose max word count for patterns
            print("Easy level selected")
            if (len(wordFamilyNum)>0):
                largestFamily = max(wordFamilyNum.items(), key=operator.itemgetter(1))[0]
            else:
                largestFamily = max(optimizedPatternChoice.items(), key=operator.itemgetter(1))[0]
            print(f"{largestFamily = }")
            familyChoice = largestFamily
        
        #letterOccurSplitIdx.append(largestFamily.index(ele for ele in largestFamily if (ele in largestFamily) == letterGuess))
        # get indexes of family choice to pass and get indices to use in word display
        count=-1
        for letter in familyChoice:
            count +=1
            if letter == letterGuess:
                # return each index of letterOccur, resorted to count
                letterOccurSplitIdx.append(count)
        print(f"Indexes of letterGuess in chosen family: {letterOccurSplitIdx =}")
    
    
    # add words according to largest group of words according to letterGuess count
    targetWordListSplit: list.clear
    listLength = len(targetWordList)
    # filtered word list by index of letters in letterOccurSplitIdx
    #################
    ###################  might be where the bug is (see screenshot) ################
    ################# 'and', '&' between indices acting as 'or'
    targetWordListSplit = []
    if letterOccur == 2:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess and word[letterOccurSplitIdx[1]] == letterGuess]
        print(f"Check 2 occurrences of letter, print list ->\n{targetWordListSplit = } ")
    elif letterOccur == 3:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess and word[letterOccurSplitIdx[1]] == letterGuess and word[letterOccurSplitIdx[2]] == letterGuess]
        print(f"Check 3 occurrences of letter, print list ->\n{targetWordListSplit = } ")
    else:
        targetWordListSplit = [word for word in targetWordList if word[letterOccurSplitIdx[0]] == letterGuess]
        print(f"For single occurrence of letter. print list length = {listLength}")        
    functionComplete = True 
    wordList1.clear()
    targetWordList.clear()
    return (targetWordListSplit,letterOccurSplitIdx,functionComplete) # filtered words above so may not need splitIdx num for word display
    
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
    
    print(Fore.RED + f"Letter occurrence in split list: {res}")
    return res

# for hard level return list of letters with weighting
def alphabetWeighting():
        my_file = open("dictionary.txt","r")
        wordList  = my_file.read().split()
        my_file.close()
        
        alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        letterTotal = {}
        sumLetters = 0
        # get total occurrence each letter in alphabet in word list.
        for i in alphabet:
            tot=0
            for j in wordList:
                if i in j:
                    tot = tot + 1
            letterTotal[i] = tot
        #print(letterTotal)
        # total letters in word list summed from aWeighting dictionary
        sumLetters = sum(letterTotal.values()) 
        #print(f"Sum of all letters in dictionary: \n{sumLetters}") # 863600 letters

        # for each alphabet letter calc. weighting
        # total each letter / total letters * 10 to 2 d.p should give range 0 - 1
        # assign to new dictionary
        # first sort aWeighting by value
        res = {key: val for key, val in sorted(letterTotal.items(), key = lambda ele: ele[1], reverse = True)}
        #print(f" Result of sorted action: \n{res}")
        letterWeight = res
        
        # round value to 2 d.p eg 'e'=0.99, 'q'=0.02
        letterWeight.update((x,round(y / sumLetters * 10,2 )) for x,y in letterWeight.items())
        #print(f"Letter weight update: \n{letterWeight}")
        #returns dict of weights for each word in the original dictionary
        return letterWeight

# for hard level
def weightingForEachFamily(wordFamilyWords):
    # when comparing which family to choose can calc weight for each word in family
    # and total for each family to choose the least which interprets as the 
    # least common letters in dictionary should make the hardest word to guess.
    dictOfPatternScore = {}
    score = 0
    # wordFamilyWords contain pattern with list of each [word , score],[word , score]
    # for each pattern sum each word score, index[1], add pattern and sum to dict.
    # return dict
    wordFamily = wordFamilyWords
    for pattern in wordFamily:
        score = 0
        #score = [[v for v in wordFamily[i]] for i in wordFamily.keys() if wordFamily.values(1) ]
        for list in wordFamily[pattern]:
            s = list[index(1)]
            score = score+s
        if pattern not in dictOfPatternScore: 
            dictOfPatternScore[pattern] =  score 
        else:
            dictOfPatternScore[pattern] =  dictOfPatternScore[pattern] + score
    # return dict of patterns and sum score of all matching words ie '_OO__' = 128
    print(f"{dictOfPatternScore = }")
    return dictOfPatternScore

    
