from wordle import get_word_colours

#assert get_word_colours("HELLO", "PLANE") == [0, 1, 0, 0, 1]
#assert get_word_colours("HELLO", "BLEEP") == [0, 1, 1, 0, 0]
#assert get_word_colours("HELLO", "HELLO") == [2, 2, 2, 2, 2]
#assert get_word_colours("HELLO", "ALLAH") == [0, 1, 2, 0, 1]
assert get_word_colours("HELLO", "PLANE") == {'L': ([], [1], []), 'A': ([], [], [2]), 'N': ([], [], [3]), 'P': ([], [], [0]), 'E': ([], [4], [])}
assert get_word_colours("HELLO", "BLEEP") == {'P': ([], [], [4]), 'E': ([], [2], [3]), 'B': ([], [], [0]), 'L': ([], [1], [])}
assert get_word_colours("HELLO", "HELLO") == {'E': ([1], [], []), 'O': ([4], [], []), 'H': ([0], [], []), 'L': ([2, 3], [], [])}
assert get_word_colours("HELLO", "ALLAH") == {'A': ([], [], [0, 3]), 'H': ([], [4], []), 'L': ([2], [1], [])}