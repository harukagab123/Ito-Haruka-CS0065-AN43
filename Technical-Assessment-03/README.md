# Technical Assessment 03

**Case study:** Intelligent Tutoring System

**Student:** Haruka Gabrielle Ito

**Course and section:** CS0065 AN43

**Submission:** Individual

This Python program demonstrates case representation, similarity assessment,
retrieval, adaptation, revision, and retention using five illustrative student
profiles. The profiles and demo quiz result are educational examples.

## Run

Use Python 3; no external packages are required. From this folder:

```text
python cbr_tutor.py --demo
```

For interactive entry of an error category, grade, repeated-error count, and
follow-up quiz score:

```text
python cbr_tutor.py
```

The script starts with five cases when `cases.json` is absent. Successful
lessons are saved to that file and loaded on later runs. To run a fresh example
without changing the default case file, supply a new file name:

```text
python cbr_tutor.py --demo --case-file fresh_demo.json
```

## CBR behavior

- Each case stores a problem, tutoring solution, and quiz outcome.
- Similarity uses topic (30%), error (40%), grade (10%), and repeats (20%).
- The new demo problem retrieves C005 at 95% similarity.
- Adaptation increases the lesson from 3 to 4 worked examples and from 6 to 8
  practice questions because the new student repeats the error one more time.
- A score below 8/10 adds support and requests another quiz result. Only a
  successful reviewed lesson is retained.
- The demo saves C006, displays all six cases, and retrieves C006 at 100% for
  the same problem. Repeating an identical solved case avoids duplicate storage.

Error categories are supplied by the user; the program does not diagnose
free-text math answers automatically. The complete source, execution screenshots,
output, documentation, and individual reflection are included in the separate
assessment document.
