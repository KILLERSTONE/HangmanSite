import csv
import random


def getRandomWords(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    if not data:
        return None

    row = data[0]
    index = random.randint(0, len(row)-1)

    if index < 0 or index >= len(row):
        return None

    rand = row[index]

    return rand


def hangmanGame():
    word = getRandomWords("wordbank.csv").strip()
    print(word)
    getLen = len(word)
    ourWord = ['_'] * (getLen)
    print(''.join(ourWord))
    attempts = 1

    print("Welcome to the hangman game: ")
    print(f"Total attemps given to you {getLen-attempts}")
    while attempts < getLen:
        print('\n\n')
        if ''.join(ourWord) == word:
            print("Congratulations, you found the word!")
            print(f"Total attempts taken: {attempts}")
            break

        userInput = input("Enter the character: ")
        if word.find(userInput) == -1:
            print("Not present in the word. Try again.")
            attempts += 1
            print(f"Attempts left now {getLen - attempts}")
            continue
        else:
            print("Yes! This character exists in our word.")
            idx = [i for i, letter in enumerate(word) if letter == userInput]
            for i in idx:
                if i < len(ourWord):
                    ourWord[i] = userInput
            print(''.join(ourWord))

    if attempts == getLen:
        print("Sorry you failed to find the word in the given attemps")


