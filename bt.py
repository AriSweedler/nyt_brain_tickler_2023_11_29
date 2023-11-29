#!/usr/bin/env python3

import json
from pathlib import Path


def download_dictionary(file_path):
    # Download the file using a 'curl -O' command
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"
    import os
    os.system(f"curl {url} -o {file_path}")
    if file_path.exists():
        return file_path

    print(f"Failed to download file: {url}")
    exit(1)


def ensure_dictionary():
    # Define a file path right next to the script
    file_path = Path(__file__).resolve().parent / "words_dictionary.json"

    # If the file doesn't exist, download it
    if not file_path.exists():
        file_path = download_dictionary(file_path)

    # Read the file as a json dict and return that
    with file_path.open() as f:
        return json.load(f)


def generate_six_letter_words(english_dictionary):
    # Loop through the dictionary and yield words that are 6 letters long
    for word in english_dictionary:
        if len(word) != 6:
            continue
        yield word


def generate_four_letter_subsection(six_letter_word):
    from itertools import combinations
    return [''.join(combination) for combination in combinations(six_letter_word, 4)]


def main():
    english_dictionary = ensure_dictionary()
    all_answer = {}
    for six_letter_word in generate_six_letter_words(english_dictionary):
        for puzzle_answer in generate_four_letter_subsection(six_letter_word):
            if puzzle_answer not in all_answer:
                all_answer[puzzle_answer] = []
            all_answer[puzzle_answer].append(six_letter_word)

    # Print the first 3 puzzle answers and their corresponding words
    count = 0
    for puzzle_answer, six_letter_words in list(all_answer.items()):
        # There needs to be at least 3 entries for a puzzle answer to be valid
        if len(six_letter_words) < 3:
            continue
        print(puzzle_answer, six_letter_words)
        print()
        count += 1
        if count > 10:
            break


if __name__ == "__main__":
    main()
