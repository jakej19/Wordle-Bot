import WordleBotV1 as wordleBOT
from tqdm import tqdm
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Constants
WORDS_FILE = "data/inputs/ALL ANSWERS.txt"
COLOUR_DICT_FILE = "data/bin/colour_dict.p"
OUTPUT_DIR = "data/outputs/"


def save_histogram(round_counts, total, output_subdir):
    """Saves a histogram of rounds taken to solve, with a vertical red line for the average."""
    # Calculate statistics
    total_solved = sum(round_counts[:-1])  # Exclude unsolved words
    solve_percentage = 100 * total_solved / total
    average_rounds = sum(
        [round_counts[i] * (i + 1) for i in range(len(round_counts) - 1)]
    ) / max(total_solved, 1)

    # Create histogram
    plt.figure(figsize=(10, 6))
    bar_colors = ["blue"] * 6 + ["red"]  # Last bar (unsolved) is red
    bars = plt.bar(
        range(1, 8),
        round_counts,
        tick_label=range(1, 8),
        edgecolor="black",
        align="center",
        color=bar_colors,
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

    # Add solve percentage to the title
    plt.title(
        f"Histogram of Rounds Taken to Solve (Solve Rate: {solve_percentage:.2f}%)"
    )
    plt.xlabel("Rounds")
    plt.ylabel("Frequency")
    plt.legend()

    # Save the plot in the output subdirectory
    filename = os.path.join(output_subdir, "rounds_histogram.png")
    plt.savefig(filename)
    plt.close()


def save_incorrect_words(incorrect_words, output_subdir):
    """Saves the incorrect words to a file."""
    filepath = os.path.join(output_subdir, "incorrect_words.txt")
    with open(filepath, "w") as f:
        f.write("\n".join(incorrect_words))


def main():
    WORDS = wordleBOT.load_words(WORDS_FILE)
    COLOUR_DICT = wordleBOT.load_dict(WORDS, COLOUR_DICT_FILE)

    num_solved, total = 0, 0
    round_counts = [0] * 7  # Include a 7th column for unsolved words
    incorrect_words = []

    # Process each word
    for word in tqdm(WORDS, "Testing Bot on all words"):
        solved, rounds = wordleBOT.run_game_loop(WORDS, COLOUR_DICT, target=word)
        total += 1
        if solved:
            num_solved += 1
            round_counts[rounds - 1] += 1
        else:
            round_counts[6] += 1  # Increment unsolved count
            incorrect_words.append(word)

    # Calculate statistics
    solve_percentage = round(100 * num_solved / total, 2)
    average_rounds = sum([round_counts[i] * (i + 1) for i in range(6)]) / max(
        num_solved, 1
    )
    print(f"Solve rate: {solve_percentage}%")
    print(f"Average rounds to solve (excluding unsolved): {round(average_rounds, 2)}")
    print(f"Round counts: {round_counts}")

    # Create output subdirectory for this attempt
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_subdir = os.path.join(OUTPUT_DIR, f"attempt_{timestamp}")
    os.makedirs(output_subdir, exist_ok=True)

    # Save results
    save_histogram(round_counts, total, output_subdir)
    save_incorrect_words(incorrect_words, output_subdir)

    print(f"Results saved in {output_subdir}")


if __name__ == "__main__":
    main()
