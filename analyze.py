# analyze.py - Advanced text analysis for input.log (refactored)

import argparse
import json
import string
from collections import Counter
from textblob import TextBlob
from typing import List, Optional, Dict

def load_lines(filename: str) -> List[str]:
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()

def load_exclude_words(path: str = 'exclude_words.json') -> set:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return set(data.get('exclude', []))
    except Exception:
        return set()

def clean_and_filter_words(lines: List[str], exclude_words: set) -> List[str]:
    words = []
    for line in lines:
        for word in line.strip().lower().split():
            clean_word = word.strip(string.punctuation)
            if clean_word and clean_word not in exclude_words:
                words.append(clean_word)
    return words

def print_top_words(words: List[str], n: int):
    word_counts = Counter(words)
    for word, count in word_counts.most_common(n):
        print(f"{word}: {count}")

def print_unique_words(words: List[str], substring: Optional[str] = None):
    word_counts = Counter(words)
    unique_words = [w for w, c in word_counts.items() if c == 1]
    if substring:
        unique_words = [w for w in unique_words if substring in w]
        print(f"Unique words containing '{substring}':")
    else:
        print("Unique words:")
    for w in sorted(unique_words):
        print(w)

def print_lines_with_word(lines: List[str], word: str):
    search = word.lower()
    print(f'Lines containing "{word}":')
    for i, line in enumerate(lines, 1):
        if search in line.lower():
            print(f"{i}: {line.rstrip()}")

def print_ngrams(words: List[str], n: int, start_word: str, mincount: int = 1, sort: str = 'desc'):
    start_word = start_word.lower()
    ngram_counter = Counter()
    for i in range(len(words) - n + 1):
        if words[i] == start_word and all(words[i+j] for j in range(n)):
            ngram = ' '.join(words[i:i+n])
            ngram_counter[ngram] += 1
    filtered = {ng: c for ng, c in ngram_counter.items() if c >= mincount}
    if sort == 'asc':
        sorted_ngrams = sorted(filtered.items(), key=lambda x: (x[1], x[0]))
    else:
        sorted_ngrams = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))
    print(f"Unique {n}-grams starting with '{start_word}':")
    for ng, c in sorted_ngrams:
        print(f"{ng}: {c}")

def print_context(lines: List[str], line_num: int, context_n: int = 3):
    idx = line_num - 1
    start = max(0, idx - context_n)
    end = min(len(lines), idx + context_n + 1)
    print(f"Showing context for line {line_num} (lines {start+1} to {end}):\n")
    for i in range(start, end):
        prefix = '>' if i == idx else ' '
        print(f"{prefix} {i+1}: {lines[i].rstrip()}")

def print_timeline(lines: List[str], word: str, chunks: int):
    search = word.lower()
    total_lines = len(lines)
    chunk_size = total_lines // chunks
    print(f'Timeline analysis for "{word}" ({chunks} chunks):')
    for i in range(chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < chunks - 1 else total_lines
        count = 0
        for line in lines[start:end]:
            count += line.lower().count(search)
        print(f'Lines {start+1}-{end}: {word} appears {count} times')

def print_sentiment(lines: List[str], word: str):
    search = word.lower()
    matches = [(i, line.rstrip()) for i, line in enumerate(lines, 1) if search in line.lower()]
    print(f'Lines containing "{word}": {len(matches)} found')
    if not matches:
        print("No lines found.")
        return
    sentiments = [(TextBlob(text).sentiment.polarity, idx, text) for idx, text in matches]
    avg = sum(s[0] for s in sentiments) / len(sentiments)
    most_pos = max(sentiments, key=lambda x: x[0])
    most_neg = min(sentiments, key=lambda x: x[0])
    avg_label = 'positive' if avg > 0 else 'negative' if avg < 0 else 'neutral'
    print(f'Average sentiment: {avg:+.2f} ({avg_label})')
    print(f'Most positive: "{most_pos[2]}" ({most_pos[0]:+.2f})')
    print(f'Most negative: "{most_neg[2]}" ({most_neg[0]:+.2f})')

def main():
    parser = argparse.ArgumentParser(description="Refactored analysis of input.log.")
    parser.add_argument('--top', type=int, default=20, help='Number of top popular words to display')
    parser.add_argument('--list', type=str, help='String to search for and print all lines containing it')
    parser.add_argument('--unique', nargs='?', const=True, default=False, metavar='SUBSTRING', help='Show all unique words not in exclude_words.json. Optionally filter by substring (e.g. --unique tone)')
    parser.add_argument('--grams', nargs=2, metavar=('N', 'WORD'), help='Show all n-grams of size N starting with WORD')
    parser.add_argument('--sort', type=str, choices=['asc', 'desc'], default='desc', help='Sort n-gram results by count (asc or desc, default desc)')
    parser.add_argument('--mincount', type=int, default=1, help='Minimum count for n-grams to be shown (default: 1)')
    parser.add_argument('--see', nargs='?', const=3, type=int, help='Show N lines before and after the specified line (default: 3)')
    parser.add_argument('--line', type=int, help='Line number to show context for (used with --see)')
    parser.add_argument('--timeline', type=str, help='Show word frequency across file chunks')
    parser.add_argument('--chunks', type=int, default=4, help='Number of chunks for timeline analysis (default: 4)')
    parser.add_argument('--sentiment', type=str, help='Show average sentiment for all lines containing WORD')
    args = parser.parse_args()

    lines = load_lines('input.log')
    exclude_words = load_exclude_words()
    words = clean_and_filter_words(lines, exclude_words)

    if args.sentiment:
        print_sentiment(lines, args.sentiment)
        return
    if args.see is not None and args.line is not None:
        print_context(lines, args.line, args.see)
        return
    if args.timeline:
        print_timeline(lines, args.timeline, args.chunks)
        return
    if args.list:
        print_lines_with_word(lines, args.list)
        return
    if args.unique:
        substring = args.unique if isinstance(args.unique, str) else None
        print_unique_words(words, substring)
        return
    if args.grams:
        n, start_word = args.grams
        try:
            n = int(n)
        except Exception:
            print("Error: --grams requires an integer N and a start word.")
            return
        print_ngrams(words, n, start_word, args.mincount, args.sort)
        return
    # Default: Top N words
    print_top_words(words, args.top)

if __name__ == "__main__":
    main()
