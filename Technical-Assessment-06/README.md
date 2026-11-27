# Technical Assessment 06 - Natural Language Processing

**Group Name:** Haruka Gabrielle Ito

**Members:** left blank in the answered activity sheet

**Section:** AN43

**Professor:** Ms. Tan

This completes Laboratory Activity 4 using the supplied PDF's original pages and formatting. The answered PDF includes output summaries in the blank boxes and continuation pages with actual word clouds, comparisons, full source and browser screenshots of the source.

## Run

Use Python 3.10 or later from this folder:

```sh
python -m pip install -r requirements.txt
python nlp_wordclouds.py
python verify.py
```

To run one part:

```sh
python nlp_wordclouds.py --part lab
python nlp_wordclouds.py --part challenge
```

All input datasets are included, so the analysis runs offline after installing dependencies. Paths are resolved relative to the script. Optional `--data-dir` and `--output-dir` arguments support other locations. The complete run writes `output/summary.json`; individual parts write `lab_summary.json` or `challenge_summary.json`. PNG figures are saved using matplotlib's noninteractive backend.

## Part VI

The original email dataset has 5,728 records. `pandas.read_csv()` loads it, and `drop_duplicates()` removes 33 exact duplicate rows. The 5,695 remaining emails contain 1,368 spam and 4,327 non-spam records. The word cloud includes **all** records, regardless of class.

The program decodes HTML entities, removes HTML tags and web URLs, lowercases text, replaces non-ASCII letters with spaces, removes one-letter tokens and stop words, and counts every remaining token. Stop words are `wordcloud.STOPWORDS` plus `subject`; the exact list is recorded in the summary. The frequency table contains 758,407 tokens over 33,549 unique words. `enron` is the most frequent token, with 13,329 occurrences.

Unlike the reference notebook's `str(df['text'])`, this code processes every email rather than a potentially truncated pandas display. It generates word clouds directly from the frequency counts. No classifier is trained; this activity describes word frequency.

## Part VII

The selected dataset is **Stanford Question Answering Dataset (SQuAD)**, item 6 in the article linked by the activity. This submission uses the complete **SQuAD 1.1 development split**, not the larger training set or SQuAD 2.0.

**Intention:** compare recurring vocabulary in Wikipedia passages with vocabulary in their questions using the same preprocessing and visualization settings.

The JSON is converted into two CSV tables, then loaded with pandas. Each context paragraph is counted once, preventing repeated weighting by its number of questions. Exact duplicate questions are removed. All 2,067 contexts remain; 10,570 questions become 10,539 unique questions. Word clouds use seed 43, size 1400 x 800 and at most 100 terms, with no plural merging or bigrams.

The question cloud emphasizes `many`, `bowl`, `tesla`, `super` and `luther`; the context cloud emphasizes `one`, `first`, `new`, `time` and `many`. Three of their top ten words overlap (`abc`, `first`, `many`), giving a top-ten Jaccard overlap of 3/17, or 17.65%. Because the corpora have different lengths, the summary also reports counts per 10,000 retained tokens. Word sizes are normalized separately within each cloud; font sizes across images are not absolute frequency comparisons.

**Conclusion:** the descriptive goal is achieved. The clouds and frequency tables show differences between passages and question phrasing. They do not measure comprehension, word importance, spam detection performance or sentiment.

**Limitations and improvements:** ordinary stop-word filtering leaves corpus artifacts (`ect`, `hou`, `re`), names, generic words and ordinal fragments (`th`). ASCII cleaning removes accents and numbers; splitting contractions may create fragments. A revised analysis should evaluate domain-specific stop words, preserve useful entities, normalize contractions and ordinals, and compare lemmatized tokens, phrases, document frequency or TF-IDF. Any changes should be documented and checked against the baseline rather than silently deleting prominent terms.

## Data and references

The exact URLs, retrieval date (27 November 2026), byte sizes and SHA-256 hashes are in `data/manifest.json`.

- Email dataset and source notebook by bendgame: https://github.com/bendgame/nlpBeginnerProjects/tree/e7375ddd4465964a7b8c30fc68cacaf4a5328045
- Article specified in the activity, current location: https://analyticsindiamag.com/ai-trends/10-nlp-open-source-datasets-to-start-your-first-nlp-project
- SQuAD creators' dataset page: https://rajpurkar.github.io/SQuAD-explorer/
- SQuAD 1.1 development file: https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json
- SQuAD attribution: Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev and Percy Liang (2016), *SQuAD: 100,000+ Questions for Machine Comprehension of Text*. https://arxiv.org/abs/1606.05250
- SQuAD is distributed under CC BY-SA 4.0. The two derived CSV tables retain the attribution and license of this source. https://creativecommons.org/licenses/by-sa/4.0/
- WordCloud API: https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html

`output/*_frequencies.csv` provides exact counts, `output/*_wordcloud.png` provides the generated clouds, and `output/*_figure.png` provides the matplotlib renderings. `evidence/run-output.txt` is the actual captured console output. Code screenshots show the complete `nlp_wordclouds.py` in three consecutive sections, rendered in a browser and captured as PNGs.
