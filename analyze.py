# analyze.py - Advanced text analysis for input.log

import argparse
import json
import string
from collections import Counter
from textblob import TextBlob
def analyze(filename, top_n=20, list_word=None, unique=False, bigrams=None, sort=None, mincount=1, see=None, line=None, timeline=None, chunks=4, grams=None, sentiment=None):
    with open(filename, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    # --sentiment: Sentiment analysis for all lines containing a word
    if sentiment:
        search = sentiment.lower()
        matches = []
        for i, line in enumerate(all_lines, 1):
            if search in line.lower():
                matches.append((i, line.rstrip()))
        print(f'Lines containing "{sentiment}": {len(matches)} found')
        if not matches:
            print("No lines found.")
            return
        sentiments = []
        for idx, text in matches:
            blob = TextBlob(text)
            sentiments.append((blob.sentiment.polarity, idx, text))
        avg = sum(s[0] for s in sentiments) / len(sentiments)
        most_pos = max(sentiments, key=lambda x: x[0])
        most_neg = min(sentiments, key=lambda x: x[0])
        if avg > 0:
            avg_label = 'positive'
        elif avg < 0:
            avg_label = 'negative'
        else:
            avg_label = 'neutral'
        print(f'Average sentiment: {avg:+.2f} ({avg_label})')
        print(f'Most positive: "{most_pos[2]}" ({most_pos[0]:+.2f})')
        print(f'Most negative: "{most_neg[2]}" ({most_neg[0]:+.2f})')
        return
    with open(filename, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    # --see: Print N lines before and after the given line number
    if see is not None and line is not None:
        try:
            context_n = int(see)
        except Exception:
            context_n = 3
        idx = int(line) - 1
        start = max(0, idx - context_n)
        end = min(len(all_lines), idx + context_n + 1)
        print(f"Showing context for line {line} (lines {start+1} to {end}):\n")
        for i in range(start, end):
            prefix = '>' if i == idx else ' '
            print(f"{prefix} {i+1}: {all_lines[i].rstrip()}")
        return

    # --timeline: Show word frequency across file chunks
    if timeline:
        search = timeline.lower()
        total_lines = len(all_lines)
        chunk_size = total_lines // chunks
        print(f'Timeline analysis for "{timeline}" ({chunks} chunks):')
        for i in range(chunks):
            start = i * chunk_size
            # Last chunk takes the remainder
            end = (i + 1) * chunk_size if i < chunks - 1 else total_lines
            count = 0
            for line in all_lines[start:end]:
                count += line.lower().count(search)
            print(f'Lines {start+1}-{end}: {timeline} appears {count} times')
        return

    # --list: Print all lines containing the given string (case-insensitive)
    if list_word:
        print(f'Lines containing "{list_word}":')
        search = list_word.lower()
        for i, line in enumerate(all_lines, 1):
            if search in line.lower():
                print(f"{i}: {line.rstrip()}")
        return

    # --unique: Print words that appear only once (after filtering and punctuation stripping)
    if unique:
        # argparse: args.unique is True (flag) or a string (substring)
        substring = None
        if isinstance(unique, str):
            substring = unique.lower()
        try:
            with open('exclude_words.json', 'r', encoding='utf-8') as f:
                exclude_data = json.load(f)
            exclude_words = set(exclude_data.get('exclude', []))
        except Exception:
            exclude_words = set()
        all_clean_words = []
        for line in all_lines:
            for word in line.strip().lower().split():
                clean_word = word.strip(string.punctuation)
                if clean_word and clean_word not in exclude_words:
                    all_clean_words.append(clean_word)
        word_counts = Counter(all_clean_words)
        unique_words = [word for word, count in word_counts.items() if count == 1]
        if substring:
            unique_words = [word for word in unique_words if substring in word]
            print(f"Unique words containing '{substring}' (appear only once, excluding exclude_words.json):")
        else:
            print("Unique words (appear only once, excluding exclude_words.json):")
        for word in sorted(unique_words):
            print(word)
        return


    # --grams: Print all n-grams of size N starting with the given word
    if grams:
        n, start_word = grams
        try:
            n = int(n)
        except Exception:
            print("Error: --grams requires an integer N and a start word.")
            return
        start_word = start_word.lower()
        ngram_counter = Counter()
        for line in all_lines:
            words = [w.strip(string.punctuation).lower() for w in line.strip().split()]
            for i in range(len(words) - n + 1):
                if words[i] == start_word and all(words[i+j] for j in range(n)):
                    ngram = ' '.join(words[i:i+n])
                    ngram_counter[ngram] += 1
        filtered_ngrams = {ng: count for ng, count in ngram_counter.items() if count >= mincount}
        print(f'Unique {n}-grams starting with "{start_word}" (with counts, mincount={mincount}):')
        if sort == 'asc':
            sorted_ngrams = sorted(filtered_ngrams.items(), key=lambda x: (x[1], x[0]))
        else:
            sorted_ngrams = sorted(filtered_ngrams.items(), key=lambda x: (-x[1], x[0]))
        for ng, count in sorted_ngrams:
            print(f"{ng}: {count}")
        return

    # --bigrams: (deprecated, use --grams 2 WORD)
    if bigrams:
        target = bigrams.lower()
        ngram_counter = Counter()
        for line in all_lines:
            words = [w.strip(string.punctuation).lower() for w in line.strip().split()]
            for i in range(len(words) - 1):
                if words[i] == target and words[i+1]:
                    ngram = f"{words[i]} {words[i+1]}"
                    ngram_counter[ngram] += 1
        filtered_ngrams = {ng: count for ng, count in ngram_counter.items() if count >= mincount}
        print(f'Unique bigrams starting with "{target}" (with counts, mincount={mincount}):')
        if sort == 'asc':
            sorted_ngrams = sorted(filtered_ngrams.items(), key=lambda x: (x[1], x[0]))
        else:
            sorted_ngrams = sorted(filtered_ngrams.items(), key=lambda x: (-x[1], x[0]))
        for ng, count in sorted_ngrams:
            print(f"{ng}: {count}")
        return

    # Default: Top N most popular words (excluding exclude_words.json)
    try:
        with open('exclude_words.json', 'r', encoding='utf-8') as f:
            exclude_data = json.load(f)
        exclude_words = set(exclude_data.get('exclude', []))
    except Exception:
        exclude_words = set()
    words = []
    for line in all_lines:
        words.extend(word for word in line.strip().lower().split() if word not in exclude_words)
    word_counts = Counter(words)
    top_words = word_counts.most_common(top_n)
    print(f"Top {top_n} most popular words:")
    for word, count in top_words:
        print(f"  {word}: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced analysis of input.log.")
    parser.add_argument('--top', type=int, default=20, help='Number of top popular words to display')
    parser.add_argument('--list', type=str, help='String to search for and print all lines containing it')
    parser.add_argument('--unique', nargs='?', const=True, default=False, metavar='SUBSTRING', help='Show all unique words not in exclude_words.json. Optionally filter by substring (e.g. --unique tone)')
    parser.add_argument('--bigrams', type=str, help='Show all bigrams starting with the given word (deprecated, use --grams 2 WORD)')
    parser.add_argument('--grams', nargs=2, metavar=('N', 'WORD'), help='Show all n-grams of size N starting with WORD')
    parser.add_argument('--sort', type=str, choices=['asc', 'desc'], help='Sort n-gram results by count (asc or desc, default desc)')
    parser.add_argument('--mincount', type=int, default=1, help='Minimum count for n-grams to be shown (default: 1)')
    parser.add_argument('--see', nargs='?', const=3, help='Show N lines before and after the specified line (default: 3)')
    parser.add_argument('--line', type=int, help='Line number to show context for (used with --see)')
    parser.add_argument('--timeline', type=str, help='Show word frequency across file chunks')
    parser.add_argument('--chunks', type=int, default=4, help='Number of chunks for timeline analysis (default: 4)')
    parser.add_argument('--sentiment', type=str, help='Show average sentiment for all lines containing WORD')
    args = parser.parse_args()
    analyze('input.log', top_n=args.top, list_word=args.list, unique=args.unique, bigrams=args.bigrams, sort=args.sort, mincount=args.mincount, see=args.see, line=args.line, timeline=args.timeline, chunks=args.chunks, grams=args.grams, sentiment=args.sentiment)
