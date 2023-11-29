#!/usr/bin/env python3

import sys
import random
import json
from pathlib import Path
from itertools import combinations
import argparse


def download_dictionary(file_path):
    # Download the file using a 'curl -O' command
    url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears-medium.txt"
    import os

    os.system(f"curl {url} -o {file_path}")
    if file_path.exists():
        return file_path

    print(f"Failed to download file: {url}")
    exit(1)


def ensure_dictionary():
    file_path = Path(__file__).resolve().parent / "google-10k-english.txt"

    # If the file doesn't exist, download it
    if not file_path.exists():
        file_path = download_dictionary(file_path)

    # Generate each line from the file
    with file_path.open() as f:
        for line in f:
            # Remove the newline character from the end of the line
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Yield the line
            yield line


def generate_six_letter_words(english_dictionary):
    # Loop through the dictionary and yield words that are 6 letters long
    for word in english_dictionary:
        if len(word) != 6:
            continue
        yield word


def generate_four_letter_substrings(six_letter_word):
    substrs = ["".join(combination) for combination in combinations(six_letter_word, 4)]
    # Unique the substrings (for example, 'fallen' + 'fale' can make '___l_n'
    # and '__l__n') and that's no fun
    return list(set(substrs))


# The hamming distance is the number of characters that are different between
# two words. For example, the hamming distance between
# 'fallen' and
# 'feline' is
# 4, because 'f_l___' are the same, but the rest of the characters are different.
def hamming_distance(word1, word2):
    return sum(1 for a, b in zip(word1, word2) if a != b)


def is_valid_puzzle(answer, word_list):
    # Only accept puzzles with 3 to 5 words
    if not 3 <= len(word_list) <= 5:
        return False

    # Make sure the hamming distance between each wordpair is at least 2. This
    # will prevent 'facial' and 'racial' from being in the same puzzle.
    for word_pair in combinations(word_list, 2):
        if hamming_distance(*word_pair) < 2:
            return False

    # You could add additional checks here - this is where it will take an
    # artists/expert's touch to turn this bland program into something more
    # beautiful and interesting, a brain tickler!:
    #
    # Some example filters would include:
    # * the answer is a valid four letter word
    # * the answer is not a bad four letter word :)
    # * the answer is all vowels or all consonants
    # * the words are sufficiently different from each other
    #  * The 'blanks' should be in sufficiently different places
    #  * The 'non-blanks' should be sufficiently different
    return True


def print_puzzle(args, answer, words):
    print(f"Puzzle #{args.puzzle_number}:")
    if args.answer:
        print(f"{answer=}")

    for word in words:
        # Replace the answer letters with underscores, but do not replace the
        # same letter twice
        tmp_answer = answer
        puzzle_word = word
        for letter in answer:
            puzzle_word = puzzle_word.replace(letter, "_", 1)
            tmp_answer = tmp_answer.replace(letter, "_", 1)

        # Print the word
        if args.answer:
            print(f"{puzzle_word} - {word}")
        else:
            print(f"{puzzle_word}")


def find_all_answers():
    # Get a dictionary of english words. Download it from the internet if necessary
    english_dictionary = ensure_dictionary()

    # Filter it to only 6 letter words.
    six_letter_words = [word for word in generate_six_letter_words(english_dictionary)]

    # Then expand the 6 letter words into all possible pairs of (word,
    # substring). The "4 letter substring" will be the answer to the puzzle.
    #
    # When I ran an example of this, I of course got many results :) Just to
    # give an illustrative sample, the 1st, 2nd, and 26th entries are:
    #
    #     ('search', 'sear')
    #     ('search', 'seac')
    #     ('online', 'nlin')
    #
    # After iterating through the WHOLE dictionary, I will be able to group
    # these by the answer, and then if an answer has at least 3 entries, I will
    # be able to generate a puzzle from it
    puzzle_component = [
        (word, answer)
        for word in six_letter_words
        for answer in generate_four_letter_substrings(word)
    ]

    # Group the puzzle components by the answer
    all_answers = {}
    for word, answer in puzzle_component:
        if answer not in all_answers:
            all_answers[answer] = []
        all_answers[answer].append(word)

    # Filter all_answers to only include valid puzzles
    for answer, word_list in list(all_answers.items()):
        if not is_valid_puzzle(answer, word_list):
            del all_answers[answer]

    return all_answers


def handle_args(all_answers):
    # Parse arguments. We accept a '--answer' flag as well as a '--puzzle_number' flag
    parser = argparse.ArgumentParser(
        description="Generate a brain tickler puzzle in the style of the Nov. 29th 2023 puzzle."
    )
    parser.add_argument(
        "--answer", action="store_true", help="Print the answer to the puzzle"
    )

    parser.add_argument(
        "-p",
        "--puzzle_number",
        type=int,
        help=f"The puzzle index. Must be between 0 and {len(all_answers)}. If this is not included then a random index will be selected",
    )
    args = parser.parse_args()

    # Massage and validate 'args.puzzle_number' into an index into the list of puzzles
    if args.puzzle_number is None:
        print("No '--puzzle_number' given. Picking a random puzzle")
        args.puzzle_number = random.randint(0, len(all_answers))
    # Bounds check
    if args.puzzle_number >= len(all_answers):
        print(
            f"Invalid index: {args.puzzle_number} - we only found puzzles 0-{len(all_answers)-1}"
        )
        exit(1)

    return args


if __name__ == "__main__":
    all_answers = find_all_answers()
    args = handle_args(all_answers)

    # Print out the puzzle
    answer = list(all_answers.keys())[args.puzzle_number]
    word_list = all_answers[answer]
    print_puzzle(args, answer, word_list)
