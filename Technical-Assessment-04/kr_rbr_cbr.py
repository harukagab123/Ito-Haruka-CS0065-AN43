"""TA4: Knowledge Representation, RBR, and CBR.
Haruka Gabrielle Ito | CS0065 AN43 | Individual submission.
Run python kr_rbr_cbr.py --demo, or omit --demo to revise.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
from textwrap import fill

# KR: six facts organized into three meaningful categories.
KNOWLEDGE_BASE = {
    "environment": {"temperature": 32, "humidity": 85},
    "weather": {"is_raining": True, "wind_speed": 25},
    "context": {"is_outdoor": True, "is_daytime": True},
}
FEATURES = ("temperature", "humidity", "is_raining",
            "wind_speed", "is_outdoor", "is_daytime")
SCALES = {"temperature": 40, "humidity": 100, "wind_speed": 50}


# Each IF-THEN rule is an independent Python function.
def rule_hot(facts):
    if facts["temperature"] > 30 and facts["is_outdoor"]:
        return "Drink water and rest in shade."


def rule_rain(facts):
    if (facts["is_raining"] and facts["is_outdoor"]
            and facts["wind_speed"] < 40):
        return "Bring an umbrella."


def rule_humid(facts):
    if facts["humidity"] >= 80 and facts["is_outdoor"]:
        return "Wear light, breathable clothing."


def rule_wind(facts):
    if facts["wind_speed"] >= 40 and facts["is_outdoor"]:
        return "Move to a sheltered area."


RULES = [("R1 heat", rule_hot), ("R2 rain", rule_rain),
         ("R3 humidity", rule_humid), ("R4 wind", rule_wind)]


def infer(knowledge_base):
    """Copy facts to working memory and check every rule once."""
    memory = {key: value for group in knowledge_base.values()
              for key, value in group.items()}
    memory = deepcopy(memory)
    actions, trace = [], []
    for name, rule in RULES:
        action = rule(memory)
        trace.append((name, bool(action)))
        if action and action not in actions:
            actions.append(action)
    return memory, trace, actions


def seed_cases():
    """Three illustrative past weather problems and solutions."""
    examples = [
        ("C001", (31, 80, False, 10, True, True),
         "Drink water, rest in shade, and wear light clothing."),
        ("C002", (27, 90, True, 20, True, True),
         "Bring an umbrella and use a covered route."),
        ("C003", (22, 60, True, 45, True, False),
         "Postpone outdoor activity and wait in a sheltered area."),
    ]
    return [{"id": label, "problem": dict(zip(FEATURES, values)),
             "solution": solution}
            for label, values, solution in examples]


def similarity(new, past):
    """Average six equally weighted feature similarities."""
    scores = []
    for key in FEATURES:
        if key in SCALES:
            gap = abs(new[key] - past[key]) / SCALES[key]
            scores.append(max(0, 1 - gap))
        else:
            scores.append(float(new[key] == past[key]))
    return sum(scores) / len(scores)


def retrieve(problem, cases):
    ranked = [(similarity(problem, c["problem"]), c) for c in cases]
    return sorted(ranked, key=lambda item: (-item[0], item[1]["id"]))


def revise(solution, demo=False):
    """Permit manual adjustment or keep the retrieved solution."""
    if demo:
        extra = ("Also drink water, rest in shade, "
                 "and wear light, breathable clothing.")
        if extra in solution:
            print("Demo revision: keep the existing reviewed advice.")
            return solution
        print("Demo manual revision: add heat and humidity advice.")
        return solution + " " + extra
    replacement = input("Revised solution (Enter keeps it): ").strip()
    return replacement or solution


def retain(problem, solution, cases, path):
    """Keep new experience in memory and JSON across program runs."""
    for case in cases:
        if (case["problem"] == problem
                and case["solution"] == solution):
            return case["id"], False
    number = max(int(c["id"][1:]) for c in cases) + 1
    label = f"C{number:03d}"
    cases.append({"id": label, "problem": deepcopy(problem),
                  "solution": solution})
    path.write_text(json.dumps(cases, indent=2) + "\n",
                    encoding="utf-8")
    return label, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    default_file = Path(__file__).with_name("cases.json")
    parser.add_argument("--case-file", type=Path, default=default_file)
    args = parser.parse_args()
    print("TA4 - OUTDOOR WEATHER ADVISORY")
    print("Illustrative facts and past cases for classroom use.")
    print("\nPART 1 - KNOWLEDGE REPRESENTATION / INPUT")
    for category, values in KNOWLEDGE_BASE.items():
        print(f"{category}: {values}")
    print("Units: temperature C; humidity %; wind speed km/h")
    memory, trace, actions = infer(KNOWLEDGE_BASE)
    print("\nPART 2 - RULE-BASED REASONING")
    print("Process: check all rules against working memory.")
    for name, fired in trace:
        print(f"{name}: {'FIRED' if fired else 'not fired'}")
    print("Rule-Based Reasoning Actions:")
    for action in actions:
        print(f"- {action}")
    if not actions:
        print("- No rule matched.")

    cases = (json.loads(args.case_file.read_text(encoding="utf-8"))
             if args.case_file.exists() else seed_cases())
    print("\nPART 3 - CASE-BASED REASONING")
    print(f"Case base loaded: {len(cases)} cases")
    print("Retrieve - ranked similarity:")
    ranked = retrieve(memory, cases)
    for score, case in ranked:
        print(f"{case['id']}: {score:.2%}")
    best = ranked[0][1]
    print(f"Retrieved case: {best['id']}")
    solution = best["solution"]
    print(fill("Reuse: " + solution, width=66))
    solution = revise(solution, args.demo)
    print(fill("Revise - final solution: " + solution, width=66))
    label, saved = retain(memory, solution, cases, args.case_file)
    print(f"Retain: {'new case saved' if saved else 'already saved'} "
          f"({label})")
    print(f"Updated case base: {len(cases)} cases")
    for case in cases:
        print(fill(f"{case['id']}: {case['solution']}", width=66))
    score, case = retrieve(memory, cases)[0]
    print(f"Learning check: {case['id']} now matches at {score:.2%}")


if __name__ == "__main__":
    main()
