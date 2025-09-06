# analyze

A flexible CLI tool for deep narrative and log analysis.

## Features
- Count and rank most popular words in `input.log`
- Exclude words via `exclude_words.json`
- Extract unique words (appear only once)
- Search for lines containing specific words/phrases
- Extract and count bigrams (word pairs), with filtering and sorting
- Show context for a specific line (3 lines before/after)
- Robust CLI flags for composable analysis

## Usage

Run with Python 3:

```
python analyze.py [options]
```

### Main Options
- `--top N`           : Show top N most common words
- `--list WORD`       : List all lines containing WORD (case-insensitive)
- `--unique`          : Show only unique words (appear once, not in exclude list)
- `--bigrams WORD`    : Show all bigrams starting with WORD
- `--sort asc|desc`   : Sort bigram results by count (default: desc)
- `--mincount N`      : Only show bigrams with count >= N
- `--see --line N`    : Show line N with 3 lines before and after for context

### Example

Show top 20 words:
```
python analyze.py --top 20
```

Show all lines containing "divine somatic":
```
python analyze.py --list "divine somatic"
```

Show bigrams starting with "divine" that appear at least twice, sorted ascending:
```
python analyze.py --bigrams divine --mincount 2 --sort asc
```

Show context for line 1790:
```
python analyze.py --see --line 1790
```

## Configuration
- Exclusion list: Add words to `exclude_words.json` under the `exclude` key.
- Input file: Place your text in `input.log`.

## Logging
- Only file-mangling bugs are logged to `ai-ide-github.log` per user protocol.

## License
MIT
