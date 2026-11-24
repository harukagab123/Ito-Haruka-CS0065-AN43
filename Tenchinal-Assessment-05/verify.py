"""Reproduce the submitted examples and check required behavior."""

import subprocess
import sys
from pathlib import Path

from challenge import analyze, number_happy, number_sad
from sentiment_analysis import classify


ROOT = Path(__file__).resolve().parent
SENTENCES = [
    "I love this wonderful day.",
    "This is an excellent result.",
    "I am happy with the great service.",
    "The food is delicious.",
    "I hate this terrible experience.",
    "The service was awful.",
    "This is a bad and disappointing product.",
    "The book is on the table.",
    "The meeting starts at ten.",
    "There are three chairs in the room.",
]


def run_program(filename, inputs):
    result = subprocess.run(
        [sys.executable, str(ROOT / filename)],
        input="\n".join(inputs) + "\n", text=True,
        capture_output=True, check=True, cwd=ROOT.parent,
    )
    # Piped stdin is not echoed by input(); add it back for a readable transcript.
    output = result.stdout
    for sentence in inputs:
        start = output.index(": ") + 2 if filename == "challenge.py" else -1
        if start != -1:
            output = output[:start] + sentence + "\n" + output[start:]
    if filename == "sentiment_analysis.py":
        for index, sentence in enumerate(inputs, 1):
            prompt = f"Enter sentence {index}/10: "
            output = output.replace(prompt, prompt + sentence + "\n", 1)
    return output


def main():
    assert [classify(p) for p in [-1, -0.01, 0, 0.01, 1]] == [
        "Negative", "Negative", "Neutral", "Positive", "Positive"
    ]
    assert number_happy("HAPPY, happy! GREAT.") == 3
    assert number_sad("SAD, sad! TERRIBLE.") == 3
    assert number_happy("unhappiness") == 0
    assert analyze("happy sad") == (1, 1, "Neutral")
    assert analyze("The book is on the table.") == (0, 0, "Neutral")
    assert analyze("sad terrible bad") == (0, 3, "Negative (sad)")
    assert analyze("") == (0, 0, "Neutral")
    output_dir = ROOT / "evidence"
    output_dir.mkdir(exist_ok=True)
    output = run_program("sentiment_analysis.py", SENTENCES)
    assert "Positive: 4\nNeutral: 3\nNegative: 3\nTotal: 10" in output
    (output_dir / "activity-output.txt").write_text(output, encoding="utf-8")
    examples = [
        "I am happy and delighted, but sad.",
        "This is a bad, terrible and sad day.",
        "I am happy and sad.",
        "The book is on the table.",
    ]
    output = "\n".join(run_program("challenge.py", [s]) for s in examples)
    (output_dir / "challenge-output.txt").write_text(output, encoding="utf-8")
    blank = subprocess.run(
        [sys.executable, str(ROOT / "sentiment_analysis.py")],
        input="\n" + "\n".join(SENTENCES) + "\n", text=True,
        capture_output=True, check=True,
    ).stdout
    assert "Please enter a non-empty sentence" in blank
    assert "Total: 10" in blank
    print("All checks passed: polarity boundaries, 10-sentence summary,")
    print("case, punctuation, repeats, whole words, ties, no matches,")
    print("positive/negative tones, blank input and alternate working directory.")


if __name__ == "__main__":
    main()
