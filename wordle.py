import math
import re

WORDS_FILE = "WORDS.TXT"
with open(WORDS_FILE, "r") as f:
    WORDS = f.read().upper().split()


"""def get_word_colours(target_word, guess_word):
    # Colours are:
    # 0 = Grey = Letter not present
    # 1 = Yellow = Letter present but in wrong place
    # 2 = Green = Letter in correct place
    colours = [(letter, 0) for letter in guess_word]
    # First check for greens, and replace any found with 0s to deal with duplicates
    target_word = list(target_word)
    for index, letter in enumerate(guess_word):
        if letter == target_word[index]:
            colours[1][index] = 2
            target_word[index] = 0
            
    for guess_index, guess_letter in enumerate(guess_word):
        for target_index, target_letter in enumerate(target_word):
            if guess_letter == target_letter:
                colours[1][guess_index] = 1
                target_word[target_index] = 0
    return colours
"""


def get_word_colours(target_word, guess_word):
    # letter : ([green index], [yellow index], [grey_index])
    colours = {letter: ([], [], []) for letter in set(guess_word)}
    # First check for greens, and replace any found with 0s to deal with duplicates
    target_word = list(target_word)
    guess_word = list(guess_word)
    for index, letter in enumerate(guess_word):
        if letter == target_word[index]:
            colours[letter][0].append(index)
            target_word[index] = "0"
            guess_word[index] = "0"
    for index, letter in enumerate(guess_word):
        if letter != "0":
            if letter in target_word:
                target_index = target_word.index(letter)
                colours[letter][1].append(index)
                target_word[target_index] = "0"
            else:
                colours[letter][2].append(index)
    return colours


def get_remaining_words(words_list, colours):
    remaining_words = words_list.copy()
    for letter, (green_list, yellow_list, grey_list) in colours.items():
        if grey_list and (green_list or yellow_list):
            letter_count = len(green_list) + len(yellow_list)
            remaining_words = [
                word for word in remaining_words if word.count(letter) == letter_count
            ]
        elif grey_list:
            remaining_words = [word for word in remaining_words if letter not in word]
        for index in green_list:
            remaining_words = [
                word for word in remaining_words if word[index] == letter
            ]
        for index in yellow_list:
            remaining_words = [
                word
                for word in remaining_words
                if word[index] != letter and letter in word
            ]
    return remaining_words


num_guesses = 0
target_word = "APPLE"
remaining_words = WORDS.copy()
best_guess = ""
while best_guess != target_word and num_guesses < 6:
    best_remaining_words = math.inf
    best_guess = ""
    for guess_word in remaining_words:
        total_remaining_words = 0
        for possible_target_word in remaining_words:
            colours = get_word_colours(possible_target_word, guess_word)
            remaining_word_count = len(get_remaining_words(remaining_words, colours))
            total_remaining_words += remaining_word_count
        if total_remaining_words < best_remaining_words:
            best_remaining_words = total_remaining_words
            best_guess = guess_word
    print(
        f"Guess {num_guesses}: {best_guess} with expected remaining words {best_remaining_words/len(remaining_words)}"
    )
    colours = get_word_colours(target_word, best_guess)
    remaining_words = get_remaining_words(remaining_words, colours)
    num_guesses+=1
    print(f"{best_guess} has actual remaining words: {len(remaining_words)}")
    print(f"with colours {colours}")
