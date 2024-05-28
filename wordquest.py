import sys,random
# A basic python implementation of a certain word guessing game
remainingTurns = 6
guessCounter = 0
availableLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
guessedWords = []
result = ['_','_','_','_','_']
resultList = [['+','+','+','+','+'],['+','+','+','+','+'],['+','+','+','+','+'],['+','+','+','+','+'],['+','+','+','+','+'],['+','+','+','+','+']]

# Check to make sure that guess provided meets all the requirements
# Print informative error messages if it does not
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

# Check if the given letter is contained with the provided word
def foundLetter(currentLetter, currentWord):
    containsLetter = False

    for checkLetter in currentWord:
        if currentLetter == checkLetter:
            containsLetter = True

    return containsLetter

# Find the index of the first occurance of the given letter within the provided word
def findFirstLetterIndex(searchLetter, searchWord):
    letterIndex = -1

    for x in range(len(searchWord)):
        if searchWord[x] == searchLetter:
            letterIndex = x
    
    return letterIndex

# Print some formatted help to explain how the game works
def printHelp():
    print("\033[104m" + "Letters in blue are in the correct location" + "\033[0m")
    print("\033[103m" + "Letters in yellow are in the word, but not in the correct location" + "\033[0m")
    print("\033[100m" + "Letters in gray are not in the word" + "\033[0m")

# Populate the wordlist from the external file and randomly select the target word from that list
wordListFile = open("words.txt", "r")
wordList = wordListFile.read().splitlines() # This method removed the \n\r at the end of each word. readlines() leaves them.
wordIndex = random.randint(0, len(wordList)-1)

# Print the selected word and index (for debugging purposes only)
#print(f"The selected word is \"{wordList[wordIndex]}\" at index {wordIndex}.")

print("Welcome to WordQuest. You have 6 guesses to determine today's 5-letter word.")

currentGuess = ""

# Main game. Loop until the player guesses the correct word or runs out of guesses
while remainingTurns > 0:
    validGuess = False

    # Do not accept a guess unless it passes all the requirements
    while validGuess == False:
        currentGuess = input(f"What is your guess [{remainingTurns}] ? ").lower()
        if currentGuess.lower  == "help":
            printHelp()

        validGuess = isValidGuess(currentGuess)

    # Do not decrement remaining turns until a valid guess was received
    remainingTurns -= 1
    
    # Add the validated guess word to the list
    guessedWords.append(currentGuess)

    # Split guess and target words into lists of letters
    targetLetters = []
    for letter in wordList[wordIndex]:
        targetLetters.append(letter)
    
    guessLetters = []
    for letter in currentGuess:
        guessLetters.append(letter)

    # Result list is used to display outcome for each letter in the guessed word
    result = ['_','_','_','_','_']

    # Check the result for each letter in the guessed word
    # Note the conversion to uppercase if there is a match. This ensures that letter will not be found again.
    # ANSI escape sequences are used to color-code the output based on the result
    for index in range(5):

        # Does this guessed letter match the letter in the target word?
        if guessLetters[index] == targetLetters[index]:
            targetLetters[index] = targetLetters[index].upper()
            result[index] = "\033[104m" + guessLetters[index].upper() + "\033[0m"

            # Mark this letter as found in the available letters list
            availableLetters[findFirstLetterIndex(guessLetters[index], availableLetters)] = "\033[104m" + guessLetters[index].upper() + "\033[0m"

            # No need to check anthing else, move to the next letter
            continue
    
        # Does the guessed letter exist anywhere in the word?
        if foundLetter(guessLetters[index], targetLetters):
            # Change the matching target letter to uppercase to indicate it was found (the index will not match the current index)
            misplacedIndex = findFirstLetterIndex(guessLetters[index], targetLetters)
            targetLetters[misplacedIndex] = targetLetters[misplacedIndex].upper()
            result[index] = "\033[103m" + guessLetters[index].upper() + "\033[0m"

            # Mark this letter as found in the available letters list
            availableLetters[findFirstLetterIndex(guessLetters[index], availableLetters)] = "\033[103m" + guessLetters[index].upper() + "\033[0m"
        else:
            # Reaching this point indicates that the current guessed letter is not in the word
            # Mark the letter as not found in the available letters list
            if foundLetter(guessLetters[index], availableLetters):
                availableLetters[findFirstLetterIndex(guessLetters[index], availableLetters)] = "\033[100m" + guessLetters[index].upper() + "\033[0m"
                #availableLetters.remove(guessLetters[index])

    # Update the result list with the remaining letters from the guessed word
    # Mark them as not found
    for index in range(5):
        if result[index] == "_":
            result[index] = "\033[100m" + guessLetters[index].upper() + "\033[0m"

    # Add the latest result to the list of guess results and print the formatted list
    resultList[guessCounter] = result
    for x in range(len(resultList)):
        print(''.join(resultList[x]))         

    # If the guessed word is correct, then the player has won
    # Print a victory message and exit the game
    if currentGuess == wordList[wordIndex]:
        print(f"WELL DONE!!! {guessCounter+1}/6")
        #print(wordList[wordIndex].upper())
        sys.exit()

    # Print the updated list of available letters
    print(' '.join(availableLetters))

    # Move to the next guess
    guessCounter += 1

print(f"The word was {wordList[wordIndex].upper()}")
print("Better luck next time!")