# Simple Text Summarizer

This Python program provides basic text summarization and document ranking functionalities. 

## Features

- **Text Segmentation:** Splits text into phrases based on punctuation.
- **Keyword Extraction:** Identifies the most frequent and relevant keywords in the text using a combination of term frequency and Zipf's Law.
- **Sentence Scoring:** Assigns scores to sentences based on the relevance of the keywords they contain.
- **Summary Generation:** Generates a concise summary by selecting the top-ranked sentences.
- **Document Ranking:** Ranks a list of documents based on the number of matches with a given set of keywords.

## Requirements

- Python 3.6 or higher

## Installation

**Clone the repository:**
   ```bash
   git clone https://github.com/srv328/simple-text-summarizer.git
   cd simple-text-summarizer
   ```

## Usage

1.  **Running the script:**
    ```bash
    python main.py 
    ```

2.  **How the code works:**
    - The script comes with a pre-defined list of documents (`documents`) and demonstrates the summarization and ranking capabilities.
    - The `simple_summary()` function takes the text and the desired summary percentage as input and returns the generated summary.
    - The `rank_texts_by_keywords()` function takes a list of texts and a list of keywords as input and returns a ranked list of texts based on keyword matches.

3.  **Customization:**
    - You can easily modify the `documents` list with your own text content.
    - Adjust the `summary_percentage` variable to control the length of the generated summaries.
