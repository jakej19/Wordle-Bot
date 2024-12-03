from collections import Counter, defaultdict
import os
import pickle
from tqdm import tqdm
from itertools import combinations
import random
from colorama import Fore, Style
import colorama
import math

WORDS_FILE = "WORDS.TXT"
COLOUR_DICT_FILE = "colour_dict.p"

colorama.init(autoreset=True)
colour_map = {
    0: Fore.LIGHTBLACK_EX,  # Grey
    1: Fore.YELLOW,  # Yellow
    2: Fore.GREEN,  # Green
}


def calc_colours(guess, target):
    """Calculates the colour pattern given an input guess and target word, with 0, 1, and 2 representing
    grey, yellow and green respectively

    Args:
        guess (str)
        target (str)

    Returns:
        tuple: five numbers representing the wordle colours
    """
    wrong_letter_indices = [
        index for index, letter in enumerate(guess) if letter != target[index]
    ]
    wrong_letter_counts = Counter(target[index] for index in wrong_letter_indices)
    colours = [2] * 5
    for index in wrong_letter_indices:
        letter = guess[index]
        if wrong_letter_counts[letter] > 0:
            colours[index] = 1
            wrong_letter_counts[letter] -= 1
        else:
            colours[index] = 0
    return tuple(colours)


def gen_colour_dict(words):
    """Generate dictionary of remaining words indexed by guess word and colour pattern from given list of words.

    Args:
        words (list(str)): List of words

    Returns:
        dict: contains all possible remaining words for each (guess, colours) pair
    """

    # Uses defaultdict and lambda function such that each key if missing will be initialised as a new defaultdict(set)
    colour_dict = defaultdict(lambda: defaultdict(set))

    for target in tqdm(words):
        for guess in words:
            colours = calc_colours(guess, target)
            colour_dict[guess][colours].add(target)
    # Return as regular dictionary as don't need to continue adding to dict.
    return dict(colour_dict)


def get_letter_freqs(words):
    letter_scores = [0] * 26
    for word in words:
        for letter in word:
            letter_scores[ord(letter) - 65] += 1
    return {chr(i + 65): math.log(letter_scores[i] + 1) for i in range(26)}


def select_guess(remaining_words, all_words):
    letter_scores = get_letter_freqs(remaining_words)
    guess_scores = {
        guess: sum([letter_scores[letter] for letter in set(list(guess))])
        for guess in remaining_words
    }
    return max(guess_scores, key=guess_scores.get)


def main():

    try:
        with open(WORDS_FILE, "r") as f:
            WORDS = f.read().upper().split()
    except Exception as e:
        print(e)

    if COLOUR_DICT_FILE in os.listdir("."):
        colour_dict = pickle.load(open(COLOUR_DICT_FILE, "rb"))
        print("Dictionary loaded.")
    else:
        colour_dict = gen_colour_dict(WORDS)
        pickle.dump(colour_dict, open(COLOUR_DICT_FILE, "wb"))
        print("Dictionary saved and loaded.")

    #### Game loop
    round_no = 0
    target = random.choice(WORDS)
    guess = ""
    remaining_words = set(WORDS)
    while round_no < 6 and guess != target:
        guess = select_guess(remaining_words, WORDS)
        colours = calc_colours(guess, target)
        remaining_words.remove(guess)
        remaining_words = colour_dict[guess][colours] & remaining_words
        coloured_string = ""
        for char, color_code in zip(guess, colours):
            colour = colour_map.get(
                color_code, Fore.RESET
            )  # Default to no color if invalid code
            coloured_string += colour + char
        coloured_string += Style.RESET_ALL
        print(f"{round_no+1}) {coloured_string}")
        round_no += 1

    if guess == target:
        print(f"Solved in {round_no} rounds.")
    else:
        print(f"Failed to solve, the word was {target}")


main()
