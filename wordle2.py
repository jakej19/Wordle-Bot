from collections import Counter, defaultdict
import pandas as pd
import os
import pickle
from tqdm import tqdm

WORDS_FILE = "WORDS.TXT"
COLOUR_DICT_FILE = "bin/colour_dict.p"


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


def main():

    try:
        with open(WORDS_FILE, "r") as f:
            WORDS = f.read().upper().split()
    except Exception as e:
        print(e)

    if COLOUR_DICT_FILE in os.listdir("./bin"):
        colour_dict = pickle.load(open(COLOUR_DICT_FILE, "rb"))
        print("Dictionary loaded.")
    else:
        colour_dict = gen_colour_dict(WORDS)
        pickle.dump(colour_dict, open(COLOUR_DICT_FILE, "wb"))
        print("Dictionary saved and loaded.")


main()
