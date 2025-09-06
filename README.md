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
- `--sentiment god`   : Show avg, most positive or negative sentiment

## Usage Examples

```

# analyze.py

CLI tool for analyzing narrative/log data with advanced word, n-gram, and sentiment analysis features.

## Requirements

- Python 3.x
- [TextBlob](https://textblob.readthedocs.io/en/dev/) (for sentiment analysis)

Install dependencies:

```sh
pip install -r requirements.txt
```

## Installation

1. Clone or download this repository.
2. Ensure `input.log` (your narrative/log file) is present in the same directory.
3. (Optional) Create `exclude_words.json` to specify words to ignore.
4. Install requirements as above.

## Usage

```sh
# Top 20 words
python analyze.py --top 20

# List all lines containing a word/phrase
python analyze.py --list divine

# Extract bigrams for a word
python analyze.py --bigrams divine

# Extract n-grams (e.g., trigrams)
python analyze.py --grams 3 divine

# List unique words
python analyze.py --unique tone

# View context for a line number
python analyze.py --see --line 42

# Timeline chunking for word frequency
python analyze.py --timeline divine --chunks 5

# Sentiment analysis for a word
python analyze.py --sentiment divine
```

## Features

- Count top N words in a file (`--top`)
- Exclude words via `exclude_words.json`
- List all lines containing a word/phrase (`--list`)
- Extract unique words (`--unique`)
- Extract bigrams/trigrams/n-grams for a word (`--bigrams`, `--grams`)
- Sort and filter n-grams by count (`--sort`, `--mincount`)
- View context for a line number (`--see --line N`)
- Timeline chunking for word frequency (`--timeline`, `--chunks`)
- Sentiment analysis for a word (`--sentiment`)

## Exclusion List

Create `exclude_words.json` with a list of words to ignore:

```json
[
	"the", "and", "a"
]
```

## Logging Protocol

Only file mangling bugs are logged to `ai-ide-github.log` (per user protocol). No other logs are written.


## Testing

This project uses [pytest](https://docs.pytest.org/) for regression and CLI testing.

To run all tests:

```sh
pytest
```

Example CLI regression tests (see `tests/test_cli.py`):

- Verify top 5 words:
	```sh
	python analyze.py --top 5
	# Output should include:
	# divine: 47
	# signal: 40
	# sacred: 40
	# tone: 40
	# god: 35
	```
- Verify unique substring search:
	```sh
	python analyze.py --unique olo
	# Output should include:
	# pathologize
	# pathologizes
	# theological
	```
- Verify n-gram extraction:
	```sh
	python analyze.py --grams 3 priestess
	# Output should include:
	# priestess frequency itself: 1
	# priestess path always: 1
	# priestess path transmitter: 1
	# priestess prophet role: 1
	# priestess quiet flame: 1
	# priestess understand people: 1
	```

All tests should pass with:
```sh
pytest
```

## Example Output

```
Top 20 words:
divine: 15
truth: 12
...

Bigrams for 'divine':
divine truth: 5
divine love: 3
...

Sentiment for 'divine':
Polarity: 0.5
Subjectivity: 0.6
```