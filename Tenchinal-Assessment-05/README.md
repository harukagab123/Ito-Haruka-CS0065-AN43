# Laboratory Activity 2 - Sentiment Analysis

**Name:** Haruka Gabrielle Ito

**Section:** AN43

**Professor:** Ms. Tan

**Course on activity sheet:** CS054 Intelligent Systems

The folder name `Tenchinal-Assessment-05` follows the requested spelling.

## Run

Use Python 3.9 or later. Open a terminal in this folder:

```sh
python -m pip install -r requirements.txt
python sentiment_analysis.py
python challenge.py
```

- `sentiment_analysis.py` accepts 10 non-empty sentences, analyzes each with TextBlob, and prints positive, neutral and negative totals. Classification uses the unrounded polarity; only displayed scores are rounded.
- `challenge.py` provides the required `number_happy(sentence)` and `number_sad(sentence)` functions. It counts whole-word occurrences in separate positive and negative word lists. Matching ignores case and surrounding punctuation, preserves internal hyphens/apostrophes, and counts repeated words separately. Equal counts, including zero matches, produce Neutral.
- `Ito_Haruka_Laboratory_Activity_2.pdf` contains the report, complete source, output transcripts, code screenshots and references.

The challenge requires only the Python standard library and the included `data` files. Its paths are resolved relative to the script, so it works from other working directories. No runtime download is required. No extra NLTK corpus download was needed for the TextBlob sentiment property used here.

## Reproduce the examples

```sh
python verify.py
```

This checks polarity boundaries, the 10-sentence loop and summary, blank-input retry, word matching, repetitions, case, punctuation, tied counts, unmatched words, and execution from a different directory. It also regenerates `evidence/activity-output.txt` and `evidence/challenge-output.txt`. Input sentences are inserted beside prompts in the saved transcripts because piped standard input does not echo them. Program outputs are captured directly.

The activity example returns **4 positive, 3 neutral and 3 negative**, total **10**. Challenge examples cover positive, negative, a 1-1 tie, and a 0-0 tie. PNGs in `evidence` are browser screenshots of the submitted source displayed as local HTML.

## Word datasets and attribution

The challenge uses the separate **positive-words.txt** and **negative-words.txt** lists from the **Hu and Liu Opinion Lexicon**, maintained by Bing Liu. Positive words serve as the happy vocabulary and negative words as the sad vocabulary. Original headers and attribution have been preserved.

- Dataset author page: https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
- Public download mirror: https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/tree/master/data/opinion-lexicon-English
- Retrieved: 24 November 2026.
- Citation: Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." Proceedings of ACM SIGKDD, 2004.
- TextBlob documentation: https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

This is a basic lexical counting approach. It does not interpret negation, sarcasm, or context. Opinion polarity is a proxy for the challenge's happy/sad categories, not an emotional intensity measurement. For example, `not happy` still counts one happy word.
