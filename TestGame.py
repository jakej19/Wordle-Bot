import WordleBotV1 as wordleBOT
from tqdm import tqdm
import os
import matplotlib.pyplot as plt
from datetime import datetime


def save_histogram(round_counts, total, graph_dir):
    """Saves a histogram of rounds taken to solve, with a vertical red line for the average."""
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)

    # Calculate average rounds (excluding unsolved words)
    total_solved = sum(round_counts[:-1])  # Exclude unsolved words
    average_rounds = (
        sum([round_counts[i] * (i + 1) for i in range(len(round_counts) - 1)])
        / total_solved
    )

    # Create histogram
    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        range(1, 8),
        round_counts,
        tick_label=range(1, 8),
        edgecolor="black",
        align="center",
    )

    # Annotate frequencies above bars
    for bar, count in zip(bars, round_counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(count),
            ha="center",
            va="bottom",
        )

    # Add vertical line for average rounds
    plt.axvline(
        average_rounds,
        color="red",
        linestyle="--",
        label=f"Average Rounds ({average_rounds:.2f})",
    )

    plt.title("Histogram of Rounds Taken to Solve")
    plt.xlabel("Rounds")
    plt.ylabel("Frequency")
    plt.legend()
    # Add datetime to the filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"rounds_histogram_{timestamp}.png"
    plt.savefig(os.path.join(graph_dir, filename))
    plt.close()

    plt.close()


def save_incorrect_words(incorrect_words, file_path):
    """Saves the incorrect words to a file."""
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, "w") as f:
        f.write("\n".join(incorrect_words))


def main():

    # Constants
    WORDS_FILE = "ALL ANSWERS.TXT"
    COLOUR_DICT_FILE = "colour_dict.p"
    GRAPH_DIR = "data/graphs/"
    INCORRECT_WORDS_FILE = "data/incorrect_words.txt"

    WORDS = wordleBOT.load_words(WORDS_FILE)
    COLOUR_DICT = wordleBOT.load_dict(WORDS, COLOUR_DICT_FILE)
    num_solved, total = 0, 0
    round_counts = [0] * 7  # Include a 7th column for unsolved words
    incorrect_words = []

    # Process each word
    for word in tqdm(WORDS):
        solved, rounds = wordleBOT.run_game_loop(WORDS, COLOUR_DICT, target=word)
        total += 1
        if solved:
            num_solved += 1
            round_counts[rounds - 1] += 1
        else:
            round_counts[6] += 1  # Increment unsolved count
            incorrect_words.append(word)

    # Calculate statistics
    average_rounds = sum([round_counts[i] * (i + 1) for i in range(6)]) / max(
        num_solved, 1
    )
    solve_rate = round(100 * num_solved / total, 2)

    # Print results
    print(f"Solve rate: {solve_rate}%")
    print(f"Average rounds to solve (excluding unsolved): {round(average_rounds, 2)}")
    print(f"Round counts: {round_counts}")

    # Save results
    save_histogram(round_counts, total, GRAPH_DIR)
    save_incorrect_words(incorrect_words, INCORRECT_WORDS_FILE)
    print(
        f"Results saved: Histogram in {GRAPH_DIR}, incorrect words in {INCORRECT_WORDS_FILE}"
    )


if __name__ == "__main__":
    main()
