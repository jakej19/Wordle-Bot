import wordle2
from tqdm import tqdm


def main():
    WORDS_FILE = "ALL ANSWERS.TXT"
    COLOUR_DICT_FILE = "colour_dict.p"

    WORDS = wordle2.load_words(WORDS_FILE)
    COLOUR_DICT = wordle2.load_dict(WORDS, COLOUR_DICT_FILE)
    num_solved, total = 0, 0
    round_counts = [0] * 6
    for word in tqdm(WORDS):
        solved, rounds = wordle2.run_game_loop(WORDS, COLOUR_DICT, target=word)
        total += 1
        num_solved += solved
        round_counts[rounds - 1] += 1
    average_rounds = sum([round_counts[i] * (i + 1) for i in range(6)]) / total
    print(f"Solve rate: {round(100*num_solved/total, 2)}%")
    print(f"Average rounds to solve: {round(average_rounds, 2)}")
    print({i for i in range(6)})
    print(f"{round_counts}")


if __name__ == "__main__":
    main()
