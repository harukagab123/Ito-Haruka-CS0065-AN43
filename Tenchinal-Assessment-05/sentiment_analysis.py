"""Laboratory Activity 2 - Haruka Gabrielle Ito, AN43, Ms. Tan."""

from textblob import TextBlob


def classify(polarity):
    if polarity < 0:
        return "Negative"
    if polarity == 0:
        return "Neutral"
    return "Positive"


def main():
    counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    print("Sentiment Analysis - 10 Sentences")
    for index in range(1, 11):
        sentence = input(f"Enter sentence {index}/10: ").strip()
        while not sentence:
            sentence = input("Please enter a non-empty sentence: ").strip()
        polarity = TextBlob(sentence).sentiment.polarity
        sentiment = classify(polarity)
        counts[sentiment] += 1
        print(f"{sentiment} (polarity: {polarity:.4f})")

    print("\nSUMMARY")
    for sentiment, count in counts.items():
        print(f"{sentiment}: {count}")
    print(f"Total: {sum(counts.values())}")


if __name__ == "__main__":
    main()
