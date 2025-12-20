import re
from collections import Counter

DEFAULT_SUMMARY_SENTENCES = 3

def clean_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', text).lower()

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)

def get_word_frequencies(text):
    words = clean_text(text).split()
    return Counter(words)

def score_sentences(sentences, word_freq):
    scores = {}
    for sentence in sentences:
        sentence_words = clean_text(sentence).split()
        score = sum(word_freq.get(word, 0) for word in sentence_words)
        scores[sentence] = score
    return scores

def summarize_text(text, summary_size=DEFAULT_SUMMARY_SENTENCES):
    sentences = split_sentences(text)
    if len(sentences) <= summary_size:
        return text

    word_freq = get_word_frequencies(text)
    sentence_scores = score_sentences(sentences, word_freq)

    top_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:summary_size]

    return " ".join(top_sentences)

if __name__ == "__main__":
    print("Simple AI Text Summarizer")
    print("-------------------------")

    user_name = input("Enter your name: ").strip() or "User"
    print(f"Welcome, {user_name}")

    print("\nEnter the text you want to summarize:")
    user_text = input("> ").strip()

    if not user_text:
        print("No text provided. Program terminated.")
    else:
        print("\nChoose summary level:")
        print("1. Short Summary")
        print("2. Detailed Summary")

        choice = input("Enter 1 or 2: ").strip()

        if choice == "2":
            summary_sentences = 5
        else:
            summary_sentences = 3

        summary = summarize_text(user_text, summary_sentences)

        print(f"\nSummary Output for {user_name}:")
        print(summary)
