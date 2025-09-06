# Text Analytics CLI Tool
**Python CLI for pattern detection in large unstructured datasets**

## Technical Overview
- **Dataset:** 1,938 lines of unstructured text data
- **Solution:** Custom Python CLI with modular analysis capabilities
- **Tech Stack:** Python, argparse, TextBlob, statistical analysis, n-gram processing

## Core Features
```bash
python analyze.py --top 20                    # Frequency analysis
python analyze.py --grams 3 divine --mincount 2   # N-gram pattern detection  
python analyze.py --sentiment divine          # NLP sentiment analysis
python analyze.py --see 5 --line 900           # Contextual line viewing
```

## Key Results
**Word frequency analysis:**
- Processed 1,938 lines with statistical ranking
- Identified semantic clusters via bigram analysis
- Tracked narrative progression across chronological data

**Sentiment analysis discovery:**
```
python analyze.py --sentiment divine
Lines containing "divine": 48 found
Average sentiment: -0.02 (demonstrates NLP limitations on metaphorical content)
```

**Voice separation algorithm:**
- Detected distinct narrative voices using pattern matching
- Mapped identity transformation across 815 lines (line 123 → 1938)
- Applied computational linguistics to subjective content

## Technical Skills Demonstrated
- **CLI architecture:** Modular design with composable flags
- **Text processing:** Large-scale data parsing with efficient algorithms  
- **NLP integration:** TextBlob library implementation
- **Pattern recognition:** Custom search and classification methods
- **Data analysis:** Statistical text processing and temporal analysis

## Innovation
Applied traditional data science methods to unconventional dataset (personal narrative), demonstrating adaptability and creative problem-solving in ML/analytics contexts.

**Repository:** Custom Python tool for exploratory text analysis