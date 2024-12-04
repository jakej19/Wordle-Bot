from collections import Counter, defaultdict
import os
import pickle
from tqdm import tqdm
from itertools import combinations
import random
from colorama import Fore, Style, init
import colorama
import math


# Functions
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
    """Generate dictionary of remaining words indexed by guess word and colour pattern from given list of words

    Args:
        words (list of str): List of words

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
    """Calculates the frequencies of all letters in the input words set,
    and returns a dictionary where letters are keys, and frequencies values.

    Args:
        words (set of str): Set of words to find letter frequencies from.

    Returns:
        Dict: Dictionary mapping characters to letter frequencies.
    """
    letter_scores = [0] * 26
    for word in words:
        for letter in word:
            letter_scores[ord(letter) - 65] += 1
    return {chr(i + 65): letter_scores[i] for i in range(26)}


def select_guess(remaining_words):
    """Returns the best guess by calculating a score for each word, then
    selecting the guess with maximal score. The score is the sum of
    letter frequencies for unique letters in the remaining words.

    Args:
        remaining_words set of str): Set of strings containing words to select guess from.

    Returns:
        string: A string with the selected guess.
    """
    letter_scores = get_letter_freqs(remaining_words)
    # Score is sum of letter freqencies(in remaining words) of unique letters
    # in the guess, uses set to get unique letters
    guess_scores = {
        guess: sum([letter_scores[letter] for letter in set(list(guess))])
        for guess in remaining_words
    }
    return max(guess_scores, key=guess_scores.get)


def load_words(DATA_DIR, WORDS_FILE):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if WORDS_FILE in os.listdir(DATA_DIR):
        with open(os.path.join(DATA_DIR, WORDS_FILE), "r") as f:
            WORDS = f.read().upper().split()
    return WORDS


def load_dict(WORDS, DATA_DIR, COLOUR_DICT_FILE):
    """First creates and saves dictionary if it doesn't exist, then loads dictionary
    of colour patterns.

    Args:
        WORDS (list): List of words
        DATA_DIR (string): Data directory location
        COLOUR_DICT_FILE (string): File location for colour dictionary

    Returns:
        Dict: Dictionary of dictionaries mapping words and colour patterns to remaining words.
    """
    BIN_DIR = os.path.join(DATA_DIR, "bin/")
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(BIN_DIR):
        os.makedirs(BIN_DIR)

    if COLOUR_DICT_FILE in os.listdir(BIN_DIR):
        colour_dict = pickle.load(open(os.path.join(BIN_DIR, COLOUR_DICT_FILE), "rb"))
        print("Dictionary loaded.")
    else:
        colour_dict = gen_colour_dict(WORDS)
        pickle.dump(colour_dict, open(os.path.join(BIN_DIR, COLOUR_DICT_FILE), "wb"))
        print("Dictionary saved and loaded.")

    return colour_dict


def initialise_colorama():
    colorama.init(autoreset=True)
    global colour_map
    colour_map = {
        0: Fore.LIGHTBLACK_EX,  # Grey
        1: Fore.YELLOW,  # Yellow
        2: Fore.GREEN,  # Green
    }


def run_game_loop(WORDS, COLOUR_DICT, target="", display=False):
    """Simulates a game of wordle with given word set, colour dictionary,
    and target word if entered. Display toggles whether the guesses and game are written to console.

    Args:
        WORDS (List of str): List of words
        COLOUR_DICT (Dict): Dictionary of dictionaries of sets of strings
        target (str, optional): Word to guess. Defaults to "".
        display (bool, optional): Display game on console if True. Defaults to False.

    Returns:
        (bool, int): Game sucess boolean, and number of rounds taken.
    """
    if display:
        initialise_colorama()
    round_no = 0
    if not target:
        target = random.choice(WORDS)
    guess = ""
    remaining_words = set(WORDS)

    while round_no < 6 and guess != target:

        guess = select_guess(remaining_words)
        colours = calc_colours(guess, target)
        remaining_words.remove(guess)
        remaining_words = COLOUR_DICT[guess][colours] & remaining_words

        if display:
            coloured_string = ""
            for char, color_code in zip(guess, colours):
                colour = colour_map.get(
                    color_code, Fore.RESET
                )  # Default to no color if invalid code
                coloured_string += colour + char
            coloured_string += Style.RESET_ALL
            print(f"{round_no+1}) {coloured_string}")

        round_no += 1

    if display:
        if guess == target:
            print(f"Solved in {round_no} rounds.")
        else:
            print(f"Failed to solve, the word was {target}")
    return guess == target, round_no


def main():
    # Constants
    DATA_DIR = "data/"
    WORDS_FILE = "ALL ANSWERS.txt"
    COLOUR_DICT_FILE = "colour_dict.p"

    WORDS = load_words(DATA_DIR, WORDS_FILE)
    COLOUR_DICT = load_dict(WORDS, DATA_DIR, COLOUR_DICT_FILE)

    # Game loop
    run_game_loop(WORDS, COLOUR_DICT, display=True)


if __name__ == "__main__":
    main()
