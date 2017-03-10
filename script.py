import os
os.chdir('/Users/Sriram/Desktop/DePaul/Q5/CSC480/Name-Generator')

import random

startProgram = True

maleNamesFile = 'namesBoys.txt'
femaleNamesFile = 'namesGirls.txt'

################################## FUNCTIONS ##################################

# reads in data and adds '__' before the name and '**' after the name
# kind: male or female
# k: the order of the markov model
def readInTrainData(kind, k):
    
    if kind == 'male':
        
        data = open(maleNamesFile, 'r')
    
    if kind == 'female':
        
        data = open(femaleNamesFile, 'r')

    orig_names = data.read().split('\r\n')     
    
    # Add '__' to start of name and '**' at end of name
    nameLst = ['_'*k + name + '*'*k for name in orig_names]
    
    return nameLst, orig_names
    
# creates transition matrix as a dictionary
# names: list of names with start and end identifiers added
# k: the order of the markov model
def createTransitionMatrix(names, k):
    
    countDict = {}
    
    for name in names:

        letters = list(name) # split name to letters
        
        for i in range(len(letters)):
            
            # creating the reference sequence of letters for a given k
            tempLst = []
            
            for x in range(i,i+k):
                
                tempLst.append(letters[x])
            
            letterSeq = tuple(tempLst)
            
            if letterSeq not in countDict.keys():
                
                countDict[letterSeq] = {}
                
            if sum([1 if x =='*' else 0 for x in letterSeq]): # reached end of name
                
                break
            
            if letters[i+k] not in countDict[letterSeq].keys(): 
                
                countDict[letterSeq][letters[i+k]] = 0
            
            countDict[letterSeq][letters[i+k]] += 1
    
    # convert raw counts into percentages
    # changing **in-place** to save memory
    probDict = countDict

    for key in probDict.keys():
        
        sumOfSeq = sum(countDict[key].values())
        
        for letter in probDict[key].keys():
            
            probDict[key][letter] = float(probDict[key][letter])/sumOfSeq
        
    
    return probDict
    

# returns list of names using a markov chain
# lenRange: a list with the min and max length of name
# number: the number of names to return
# kind: male or female
# k: the order of the markov model to use

def genNames(lenRange, number, kind, k):
    
    minLen,maxLen = lenRange
    
    names, orig_names = readInTrainData(kind, k)
    
    transDict = createTransitionMatrix(names, k)
        
    namesLst = []
        
    while len(namesLst) <= number: 
        
        parentSeq = tuple(list('_'*k)) # to find the first letter
        
        name = ''
        
        tryCount = 0
        
        while True:
            
            if len(name) > maxLen:
                
                break
        
            successorLst = []
        
            for letter, count in transDict[parentSeq].items():
                
                # multiply count 100 to get a non-decimal 
                # value (we can only have 28 diff successors)
                successorLst += [letter] * int(count*100) 
                
            nextLetter = random.choice(successorLst)
            
        
            if nextLetter == '*' and len(name) >= minLen:
                                
                if name not in orig_names: # only new and novel names are added
                
                    namesLst.append(name)
                
                break
            
            if nextLetter == '*' and len(name) < minLen:
                
                tryCount += 1
                
                if tryCount == 5: # break if we try 5 times
                    
                    break 
                
                continue # try another letter
        
            name += nextLetter            
            
            parentSeq = tuple(list(parentSeq[1:]) + [nextLetter])
                
    return namesLst
        
###################################### TESTS ##################################

#genNames([4,10], 5, 'female', k=3)    
#genNames([2,12], 5, 'female', k=2)   
#genNames([5,13], 10, 'male', 4) 
#genNames([8,13], 10, 'male', 2) 
#genNames([8,8], 10, 'male', 1) 
#genNames([8,10], 10, 'female', 2) 

    
###################################### PROGRAM ################################
while startProgram:
    
    print 'Hello, this program will generate names.'
    
    print 'Please answer the following questions, so that the results may be \
    personalized to your needs '
    
    kind = input('What is the gender? (Please answer "male" or "female"): ')
    
    number = input('How many names do you need?: ')
    
    maxLen = input('What is the maximum permissible length of name?: ')
    
    minLen = input('What is the minimum permissible length of name?: ')
    
    k = input('What order Markov Chain would you like used in generating the\
    names? (2 is recommended): ')
    
    names = genNames([minLen, maxLen], number, kind, k)
    
    print 'Here are the names: '    
        
    for name in names:
        
        print name
    
    print '\n\n\n'
    
    genMore = input('Would you like to generate another set of names? ("Yes" or "No"): ')
    
    if genMore == 'No':
        
        startProgram = False
        
        print 'Thank you.'
        
    else:
        
        startProgram = True
    
###############################################################################        
        
    
    
    
    
            
            
        
    
    
    
    