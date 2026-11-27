"""Check the submitted outputs against complete source data and known cases."""
import hashlib
import json
import re

import pandas as pd
from PIL import Image
from nlp_wordclouds import ROOT, STOP_WORDS, clean_tokens


def main():
    assert clean_tokens("<b>The CAT</b> &amp; dogs! 123 https://example.com") == ["cat", "dogs"]
    assert clean_tokens("Subject: HELLO, hello!") == ["hello", "hello"]
    assert clean_tokens("") == []
    data = ROOT / "data"
    out = ROOT / "output"
    for name, info in json.loads((data / "manifest.json").read_text()).items():
        assert hashlib.sha256((data / name).read_bytes()).hexdigest() == info["sha256"]
    summary = json.loads((out / "summary.json").read_text())
    email_rows = pd.read_csv(data / "emails.csv").drop_duplicates()
    assert len(email_rows) == summary["emails"]["retained_rows"] == 5695
    assert summary["emails"]["class_counts"] == {"spam": 1368, "not_spam": 4327}
    dataset = json.loads((data / "squad-dev-v1.1.json").read_text("utf-8"))
    paragraphs = [p for a in dataset["data"] for p in a["paragraphs"]]
    assert len(paragraphs) == summary["squad_contexts"]["retained_rows"] == 2067
    questions = {q["question"] for p in paragraphs for q in p["qas"]}
    assert len(questions) == summary["squad_questions"]["retained_rows"] == 10539
    for name in ["emails", "squad_contexts", "squad_questions"]:
        frequencies = pd.read_csv(out / f"{name}_frequencies.csv", keep_default_na=False)
        assert frequencies["count"].sum() == summary[name]["tokens"]
        assert len(frequencies) == summary[name]["unique_words"]
        assert all(re.fullmatch(r"[a-z]{2,}", w) for w in frequencies["word"])
        assert not (set(frequencies["word"]) & STOP_WORDS)
        Image.open(out / f"{name}_wordcloud.png").verify()
    # Independent full-file token count guards against a truncated Series display.
    whole = " ".join(email_rows["text"].str.lower())
    expected_enron = len(re.findall(r"\benron\b", whole))
    counts = pd.read_csv(out / "emails_frequencies.csv", keep_default_na=False).set_index("word")["count"]
    assert counts["enron"] == expected_enron == 13329
    comparison = summary["comparison"]
    assert comparison["shared_top_10"] == ["abc", "first", "many"]
    assert abs(comparison["top_10_jaccard"] - 3 / 17) < 1e-12
    print("All checks passed: source hashes, full-corpus counts, duplicates,")
    print("labels, cleaning, stop words, PNG validity and comparison metrics.")


if __name__ == "__main__":
    main()
