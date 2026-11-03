"""TA3: Case-Based Reasoning Intelligent Tutoring System.
Haruka Gabrielle Ito | CS0065 AN43 | Individual submission.
Run: python cbr_tutor.py --demo (or omit --demo for input).
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path

CASE_FILE = Path(__file__).with_name("cases.json")


def make_case(number, topic, error, grade, repeats,
              feedback, examples, practice):
    """Represent a problem, successful lesson, and quiz outcome."""
    return {
        "id": f"C{number:03d}",
        "problem": {"topic": topic, "error": error,
                    "grade": grade, "repeats": repeats},
        "solution": {"feedback": feedback, "grade": grade,
                     "examples": examples, "practice": practice},
        "outcome": {"quiz_correct": 8, "quiz_total": 10},
    }


def seed_cases():
    """Five illustrative profiles with successful interventions."""
    return [
        make_case(1, "algebra", "sign", 8, 2,
                  "Subtract the same value from both sides.", 2, 4),
        make_case(2, "algebra", "division", 9, 2,
                  "Divide both sides by the coefficient.", 2, 5),
        make_case(3, "fractions", "denominator", 7, 3,
                  "Use a common denominator before adding.", 3, 6),
        make_case(4, "geometry", "formula", 8, 2,
                  "Choose the correct area formula.", 2, 5),
        make_case(5, "algebra", "sign", 8, 4,
                  "Use balance steps to correct sign errors.",
                  3, 6),
    ]


def similarity(new, past):
    """Weighted score in [0, 1]; compare problem attributes only."""
    topic = float(new["topic"] == past["topic"])
    error = float(new["error"] == past["error"])
    grade = max(0, 1 - abs(new["grade"] - past["grade"]) / 5)
    repeats = max(0, 1 - abs(new["repeats"] - past["repeats"]) / 4)
    return .30 * topic + .40 * error + .10 * grade + .20 * repeats


def retrieve(problem, cases):
    """Rank successful cases; use ID to break equal-score ties."""
    ranked = [(similarity(problem, c["problem"]), c) for c in cases
              if c["outcome"]["quiz_correct"] >= 8]
    order = lambda item: (-item[0], item[1]["id"])
    return sorted(ranked, key=order)


def adapt(problem, past):
    """Reuse the lesson; add support for more repeated errors."""
    lesson = deepcopy(past["solution"])
    extra = max(0, problem["repeats"]
                - past["problem"]["repeats"])
    lesson["examples"] += extra
    lesson["practice"] += 2 * extra
    lesson["grade"] = problem["grade"]
    return lesson


def ask_number(prompt, low, high):
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
        except ValueError:
            pass
        print(f"Enter a whole number from {low} to {high}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true",
                        help="run the illustrated algebra scenario")
    parser.add_argument("--case-file", type=Path, default=CASE_FILE,
                        help="JSON file for persistent learning")
    args = parser.parse_args()
    cases = (json.loads(args.case_file.read_text(encoding="utf-8"))
             if args.case_file.exists() else seed_cases())
    print("INTELLIGENT TUTORING SYSTEM - CBR")
    print(f"Case base loaded: {len(cases)} cases")
    if args.demo:
        problem = {"topic": "algebra", "error": "sign",
                   "grade": 8, "repeats": 5}
        print("Demo uses illustrative student data and quiz results."
              )
    else:
        options = [("algebra", "sign"), ("algebra", "division"),
                   ("fractions", "denominator"),
                   ("geometry", "formula")]
        for number, option in enumerate(options, 1):
            print(f"{number}. {option[0]} / {option[1]} error")
        choice = ask_number("Choose error (1-4): ", 1, 4)
        topic, error = options[choice - 1]
        problem = {"topic": topic, "error": error,
                   "grade": ask_number("Grade (7-12): ", 7, 12),
                   "repeats": ask_number("Errors (1-5): ", 1, 5)}

    print("\nINPUT - NEW PROBLEM")
    print(f"Grade {problem['grade']}; topic: {problem['topic']}")
    print(f"Error: {problem['error']}; "
          f"repeats: {problem['repeats']}")
    if (problem["topic"], problem["error"]) == ("algebra", "sign"):
        print("Example: 3x + 5 = 20; student writes 3x = 25.")
    ranked = retrieve(problem, cases)
    if not ranked:
        print("No successful case. Teacher review needed.")
        return
    print("\nPROCESS - SIMILARITY RANKING")
    for position, (score, case) in enumerate(ranked, 1):
        print(f"{position}. {case['id']}: {score:.2%}")
    best = ranked[0][1]
    print(f"Retrieved case: {best['id']}")
    p = best["problem"]
    print(f"Past problem: grade {p['grade']}; topic: {p['topic']}")
    print(f"Past error: {p['error']}; repeats: {p['repeats']}")
    old = best["solution"]
    print(f"Past lesson: {old['examples']} examples, "
          f"{old['practice']} practice questions")
    lesson = adapt(problem, best)
    print("\nOUTPUT - ADAPTED SOLUTION")
    print(f"{lesson['feedback']} "
          f"Use Grade {lesson['grade']} exercises.")
    if (problem["topic"], problem["error"]) == ("algebra", "sign"):
        print("Worked correction: 3x = 20 - 5 = 15; x = 5.")
    print(f"Worked examples: {lesson['examples']}")
    print(f"Practice questions: {lesson['practice']}")

    # Revise after a follow-up quiz; retain only reviewed successes.
    correct = (8 if args.demo
               else ask_number("Quiz correct (0-10): ", 0, 10))
    print(f"\nREVIEW - Follow-up quiz: {correct}/10; target: 8/10")
    while correct < 8:
        lesson["examples"] += 1
        lesson["practice"] += 2
        print("Revision: add 1 example and 2 practice questions.")
        print(f"Revised examples: {lesson['examples']}")
        print(f"Revised practice: {lesson['practice']}")
        print("Not retained yet; use the revised lesson.")
        correct = ask_number("Recheck quiz (0-10): ", 0, 10)
        print(f"Revised quiz: {correct}/10; target: 8/10")
    print("Target met. Lesson accepted for retention.")
    duplicate = any(c["problem"] == problem
                    and c["solution"] == lesson
                    for c in cases)
    if duplicate:
        print("\nLEARNING - This solved case is already saved.")
    else:
        next_id = max(int(c["id"][1:]) for c in cases) + 1
        cases.append({"id": f"C{next_id:03d}", "problem": problem,
                      "solution": lesson,
                      "outcome": {"quiz_correct": correct,
                                  "quiz_total": 10}})
        print(f"\nLEARNING - New case saved: C{next_id:03d}")
    args.case_file.write_text(json.dumps(cases, indent=2) + "\n",
                              encoding="utf-8")
    print(f"Updated case base: {len(cases)} cases (saved to JSON)")
    for case in cases:
        p = case["problem"]
        print(f"{case['id']}: {p['topic']}/{p['error']}; "
              f"grade {p['grade']}; repeats {p['repeats']}")
    print("\nLEARNING CHECK - Retrieve the same problem again")
    score, case = retrieve(problem, cases)[0]
    print(f"Best match: {case['id']} ({score:.2%})")


if __name__ == "__main__":
    main()
