"""Count happy and sad word occurrences using Hu and Liu's Opinion Lexicon."""

import re
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"


def load_words(filename):
    lines = (DATA_DIR / filename).read_text(encoding="latin-1").splitlines()
    return frozenset(
        line.strip().casefold() for line in lines
        if line.strip() and not line.lstrip().startswith(";")
    )


HAPPY_WORDS = load_words("positive-words.txt")
SAD_WORDS = load_words("negative-words.txt")


def words(sentence):
    # Keep internal hyphens/apostrophes and a+ from the original lexicon.
    return re.findall(r"[a-z0-9]+(?:[-'][a-z0-9]+)*\+?", sentence.casefold())


def number_happy(sentence):
    return sum(word in HAPPY_WORDS for word in words(sentence))


def number_sad(sentence):
    return sum(word in SAD_WORDS for word in words(sentence))


def analyze(sentence):
    happy = number_happy(sentence)
    sad = number_sad(sentence)
    if happy > sad:
        tone = "Positive (happy)"
    elif sad > happy:
        tone = "Negative (sad)"
    else:
        tone = "Neutral"
    return happy, sad, tone


def main():
    sentence = input("Enter a sentence: ").strip()
    while not sentence:
        sentence = input("Please enter a non-empty sentence: ").strip()
    happy, sad, tone = analyze(sentence)
    print(f"Happy words: {happy}")
    print(f"Sad words: {sad}")
    print(f"Analysis: {tone}")


if __name__ == "__main__":
    main()
