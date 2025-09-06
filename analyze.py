# analyze-ai.py - Advanced text analysis for input.log

import argparse
import json
import string
from collections import Counter

def analyze_ai(filename, top_n=20, list_word=None, unique=False, bigrams=None, sort=None, mincount=1, see=False, line=None):
    with open(filename, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    print(f"Sanity check: lines in file: {len(all_lines)}")


    # --see: Print 3 lines before and after the given line number
    if see and line is not None:
        idx = int(line) - 1
        start = max(0, idx - 3)
        end = min(len(all_lines), idx + 4)
        print(f"Showing context for line {line} (lines {start+1} to {end}):\n")
        for i in range(start, end):
            prefix = '>' if i == idx else ' '
            print(f"{prefix} {i+1}: {all_lines[i].rstrip()}")
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
        print("Unique words (appear only once, excluding exclude_words.json):")
        for word in sorted(unique_words):
            print(word)
        return

    # --bigrams: Print all bigrams starting with the given word
    if bigrams:
        target = bigrams.lower()
        bigram_counter = Counter()
        for line in all_lines:
            words = [w.strip(string.punctuation).lower() for w in line.strip().split()]
            for i in range(len(words) - 1):
                if words[i] == target and words[i+1]:
                    bigram = f"{words[i]} {words[i+1]}"
                    bigram_counter[bigram] += 1
        filtered_bigrams = {bg: count for bg, count in bigram_counter.items() if count >= mincount}
        print(f'Unique bigrams starting with "{target}" (with counts, mincount={mincount}):')
        if sort == 'asc':
            sorted_bigrams = sorted(filtered_bigrams.items(), key=lambda x: (x[1], x[0]))
        else:
            sorted_bigrams = sorted(filtered_bigrams.items(), key=lambda x: (-x[1], x[0]))
        for bg, count in sorted_bigrams:
            print(f"{bg}: {count}")
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
    parser.add_argument('--unique', action='store_true', help='Show all unique words not in exclude_words.json')
    parser.add_argument('--bigrams', type=str, help='Show all bigrams starting with the given word')
    parser.add_argument('--sort', type=str, choices=['asc', 'desc'], help='Sort bigram results by count (asc or desc, default desc)')
    parser.add_argument('--mincount', type=int, default=1, help='Minimum count for bigrams to be shown (default: 1)')
    parser.add_argument('--see', action='store_true', help='Show context for a specific line')
    parser.add_argument('--line', type=int, help='Line number to show context for (used with --see)')
    args = parser.parse_args()
    analyze_ai('input.log', top_n=args.top, list_word=args.list, unique=args.unique, bigrams=args.bigrams, sort=args.sort, mincount=args.mincount, see=args.see, line=args.line)
