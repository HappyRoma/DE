import re
from os import write

def read_file():
    with open('first_task.txt', encoding="utf-8") as file:
        return file.readlines()

def words_split(lines):
    words = []

    for line in lines:
        newLine = (re.sub(r"[-,?!.\n]", '', line))

        words += newLine.lower().split(" ")

    return words

def calc_words_count(wordsArray):
    word_library = {}
    for word in wordsArray:
        if word in word_library:
            word_library[word] += 1
        else:
            word_library[word] = 1

    return sorted(word_library.items(), key=lambda x: x[1], reverse=True)

def write_to_file(data):
    with open('first_task_result.txt', 'w', encoding="utf-8") as file:
        for key, value in data:
            file.write(f"{key}: {value}\n")

def count_consonant(words):
    count = 0
    countConsonants = 0
    consonantLetters = 'bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ'
    for word in words:
        for letter in word:
            if letter.isalpha():
                count += 1
                if letter in consonantLetters:
                    countConsonants += 1

    ratio = countConsonants / count

    with open("first_task_6_result.txt", "w", encoding="utf-8") as file:
        file.write(f"Количество согласных букв: {countConsonants}\n")
        file.write(f"Доля согласных букв: {ratio:.2f}\n")

wordsArray = words_split(read_file())

print(calc_words_count(wordsArray))
write_to_file(calc_words_count(wordsArray))

count_consonant(wordsArray)
