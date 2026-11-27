"""Exercise 4: Haruka Gabrielle Ito, AN43, Ms. Tan."""
import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import STOPWORDS, WordCloud

ROOT = Path(__file__).resolve().parent
STOP_WORDS = set(STOPWORDS) | {"subject"}


def clean_tokens(text):
    text = html.unescape(str(text)).lower()
    text = re.sub(r"<[^>]*>", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z]", " ", text)
    return [w for w in text.split() if len(w) > 1 and w not in STOP_WORDS]


def summarize(frame, name, output_dir):
    original_rows = len(frame)
    frame = frame.dropna(subset=["text"]).copy()
    frame = frame[frame["text"].str.strip().ne("")]
    valid_rows = len(frame)
    # Email duplicates use the complete row; SQuAD frames have only text.
    frame = frame.drop_duplicates().reset_index(drop=True)
    counts = Counter()
    for text in frame["text"]:
        counts.update(clean_tokens(text))
    if not counts:
        raise ValueError(f"{name}: no words remain after cleaning")
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    pd.DataFrame(ordered, columns=["word", "count"]).to_csv(
        output_dir / f"{name}_frequencies.csv", index=False)
    cloud = WordCloud(width=1400, height=800, background_color="white",
                      max_words=100, min_font_size=12, random_state=43,
                      collocations=False, normalize_plurals=False,
                      colormap="viridis").generate_from_frequencies(dict(ordered))
    cloud.to_file(str(output_dir / f"{name}_wordcloud.png"))
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.imshow(cloud, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(name.replace("_", " ").title())
    fig.savefig(output_dir / f"{name}_figure.png", dpi=160,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    result = {"input_rows": original_rows,
              "missing_or_blank_removed": original_rows - valid_rows,
              "duplicate_rows_removed": valid_rows - len(frame),
              "retained_rows": len(frame), "tokens": sum(counts.values()),
              "unique_words": len(counts), "top_10": ordered[:10]}
    if "spam" in frame:
        result["class_counts"] = {
            "spam": int(frame["spam"].eq(1).sum()),
            "not_spam": int(frame["spam"].eq(0).sum())}
    print(f"\n{name}")
    for key, value in result.items():
        print(f"{key}: {value}")
    return result, counts


def run_lab(data_dir, output_dir):
    frame = pd.read_csv(data_dir / "emails.csv")
    if not {"text", "spam"}.issubset(frame.columns):
        raise ValueError("emails.csv must contain text and spam columns")
    frame = frame[["text", "spam"]]
    if not frame["spam"].isin([0, 1]).all():
        raise ValueError("Email labels must be 0 (not spam) or 1 (spam)")
    return summarize(frame, "emails", output_dir)[0]


def run_challenge(data_dir, output_dir):
    dataset = json.loads((data_dir / "squad-dev-v1.1.json").read_text("utf-8"))
    contexts, questions = [], []
    for article in dataset["data"]:
        for paragraph in article["paragraphs"]:
            # Count each paragraph once, rather than once per question.
            contexts.append(paragraph["context"])
            questions.extend(qa["question"] for qa in paragraph["qas"])
    pd.DataFrame({"text": contexts}).to_csv(
        output_dir / "squad_contexts.csv", index=False)
    pd.DataFrame({"text": questions}).to_csv(
        output_dir / "squad_questions.csv", index=False)
    context_stats, context_counts = summarize(
        pd.read_csv(output_dir / "squad_contexts.csv"),
        "squad_contexts", output_dir)
    question_stats, question_counts = summarize(
        pd.read_csv(output_dir / "squad_questions.csv"),
        "squad_questions", output_dir)
    a = {word for word, _ in context_stats["top_10"]}
    b = {word for word, _ in question_stats["top_10"]}
    comparison = {"article_count": len(dataset["data"]),
                  "shared_top_10": sorted(a & b),
                  "top_10_jaccard": len(a & b) / len(a | b)}
    for name, counts in [("contexts", context_counts),
                         ("questions", question_counts)]:
        total = sum(counts.values())
        comparison[f"{name}_per_10000"] = {
            word: round(counts[word] / total * 10000, 2)
            for word in sorted(a | b)}
    print("\ncomparison:", json.dumps(comparison, indent=2))
    return {"squad_contexts": context_stats,
            "squad_questions": question_stats, "comparison": comparison}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--part", choices=["lab", "challenge", "all"], default="all")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "output")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    if args.part in ["lab", "all"]:
        results["emails"] = run_lab(args.data_dir, args.output_dir)
    if args.part in ["challenge", "all"]:
        results.update(run_challenge(args.data_dir, args.output_dir))
    results["settings"] = {"seed": 43, "max_words": 100,
                           "stop_words": sorted(STOP_WORDS),
                           "token_rule": "lowercase ASCII words, length > 1"}
    filename = "summary.json" if args.part == "all" else f"{args.part}_summary.json"
    (args.output_dir / filename).write_text(json.dumps(results, indent=2), "utf-8")


if __name__ == "__main__":
    main()
