import random
# A basic python implementation of Wordle
remainingTurns = 6
guessCounter = 0
availableLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
misplacedLetter = []
guessedWords = []
unusedLetters = []
result = ['_','_','_','_','_']
resultList = [['+','+','+','+','+'],['+','+','+','+','+'],['+','+','+','+','+'],['+','+','+','+','+'],['+','+','+','+','+'],['+','+','+','+','+']]

def isValidGuess(theGuess):
    errorString = ""

    if len(theGuess) != 5:
        errorString += "Guesses must contain exactly 5 letters!\r\n"

    if not theGuess.isalpha():
        errorString += "Guesses must contain only letters!\r\n"

    if theGuess in guessedWords:
        errorString += theGuess + " was already guessed!\r\n"

    if theGuess not in wordList:
        errorString += theGuess + " is not an available word!\r\n"
    
    if len(errorString) > 1:
        print(errorString)
        return False
    else:
        return True

def foundLetter(currentLetter, currentWord):
    containsLetter = False

    for checkLetter in currentWord:
        #print(f">>>{currentLetter} - {checkLetter}")
        if currentLetter == checkLetter:
            #print("true")
            containsLetter = True

    return containsLetter

def findFirstLetterIndex(searchLetter, searchWord):
    letterIndex = -1

    for x in range(len(searchWord)):
        if searchWord[x] == searchLetter:
            letterIndex = x
    
    return letterIndex

def printHelp():
    print("\033[104m" + "Letters in blue are in the correct location" + "\033[0m")
    print("\033[103m" + "Letters in yellow are in the word, but not in the correct location" + "\033[0m")
    print("\033[100m" + "Letters in gray are not in the word" + "\033[0m")

wordListFile = open("words.txt", "r")

wordList = wordListFile.read().splitlines() # This method removed the \n\r at the end of each word. readlines() leaves them.

wordIndex = random.randint(0, len(wordList)-1)

#print(f"The selected word is \"{wordList[wordIndex]}\" at index {wordIndex}.")

print("Welcome to WordQuest. You have 6 guesses to determine today's 5-letter word.")

currentGuess = ""

while remainingTurns > 0:
    #print(f"You have {remainingTurns} guesses remaining.")
    validGuess = False

    # Validate the guess meets the requirements
    while validGuess == False:
        currentGuess = input(f"What is your guess [{remainingTurns}] ? ").lower()
        if currentGuess in ['help', 'HELP']:
            printHelp()

        validGuess = isValidGuess(currentGuess)

    remainingTurns -= 1
    
    guessedWords.append(currentGuess)
    #print(guessedWords)

    # Split target word into list of letters
    # Split guess word into list of letters
    targetLetters = []
    guessLetters = []

    for letter in wordList[wordIndex]:
        targetLetters.append(letter)
    #print(targetLetters)
    
    for letter in currentGuess:
        guessLetters.append(letter)
    #print(guessLetters)

    # Check guess word against the target
    
    result = ['_','_','_','_','_']


    # Is the letter in the target word
    # is the letter in the correct place in the target word

    # Check if the word is correct
    if currentGuess == wordList[wordIndex]:
        print("WELL DONE!!!")
        print(wordList[wordIndex].upper())

   # Check for all letters that are in the right position
    for index in range(5):
        if guessLetters[index] == targetLetters[index]:
            targetLetters[index] = targetLetters[index].upper()
            result[index] = "\033[104m" + guessLetters[index].upper() + "\033[0m"
            availableLetters[findFirstLetterIndex(guessLetters[index], availableLetters)] = "\033[104m" + guessLetters[index].upper() + "\033[0m"

            continue
    
        # if target word contains this letter, then set as lower case 
        if foundLetter(guessLetters[index], targetLetters):
            #Need to change target letter occurance to upper, not this letter
            misplacedIndex = findFirstLetterIndex(guessLetters[index], targetLetters)
            targetLetters[misplacedIndex] = targetLetters[misplacedIndex].upper()
            result[index] = "\033[103m" + guessLetters[index].upper() + "\033[0m"
            availableLetters[findFirstLetterIndex(guessLetters[index], availableLetters)] = "\033[103m" + guessLetters[index].upper() + "\033[0m"
        else:
            # letter not in the word, so remove from available letters
            if foundLetter(guessLetters[index], availableLetters):
                availableLetters[findFirstLetterIndex(guessLetters[index], availableLetters)] = "\033[100m" + guessLetters[index].upper() + "\033[0m"
                #availableLetters.remove(guessLetters[index])

        #print("")
        #print(f"T Letters >> {targetLetters}")
        #print(f"G Letters >> {guessLetters}")
        #print(f"C Letters >> {result}")

    # fill in remaining letters
    for index in range(5):
        if result[index] == "_":
            result[index] = "\033[100m" + guessLetters[index].upper() + "\033[0m"

    resultList[guessCounter] = result
    for x in range(len(resultList)):
        print(''.join(resultList[x]))         

    guessCounter += 1

    #print("\033[93m" +  ''.join(resultList[len(resultList)-1]) + "\033[0m")
    print(' '.join(availableLetters))
