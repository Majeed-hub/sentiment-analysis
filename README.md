# Web Scraping and Text Analysis

This is a Python script that performs web scraping and text analysis on a list of URLs.
It extracts article content, cleans the text, and computes various metrics, such as word count, readability score, sentiment score, and personal pronouns. 
The results are saved in an Excel file for further analysis.

## Requirements

To run this script, you need to have the following libraries installed:

- Pandas
- requests
- BeautifulSoup
- NLTK
- Openpyxl
- Syllapy

You can install them using pip or conda commands.

## Input

The input file for this script is "input.xlsx", which contains a list of URLs and URL IDs. 
The URLs should point to web pages that contain article content. The URL IDs are unique identifiers for each URL.

## Output

The output file for this script is "output_structure.xlsx", which contains the following columns:

- URL ID: The unique identifier for each URL
- URL: The web page address
- Word Count: The number of words in the article content
- Average Word Length: The average length of words in the article content
- Syllables per Word: The average number of syllables per word in the article content
- Average Sentence Length: The average number of words per sentence in the article content
- Percentage of Complex Words: The percentage of words with three or more syllables in the article content
- Fog Index: A measure of readability that estimates the years of formal education needed to understand the text
- Positive Score: The number of positive words in the article content
- Negative Score: The number of negative words in the article content
- Polarity Score: The difference between positive and negative scores, normalized by word count
- Subjectivity Score: The ratio of opinion words to factual words in the article content
- Personal Pronouns: The number of personal pronouns (e.g., I, we, my) in the article content

## Usage

To run this script, follow these steps:

1. Ensure you have the required libraries installed and the input file ready
2. Open a terminal or command prompt and navigate to the directory where the script is located
3. Run the command `python web_scraping_and_text_analysis.py`
4. Wait for the script to finish and check the output file

## Notes

This script is designed for educational and demonstration purposes and may require customization for production.
It may not work for all types of web pages and may encounter errors or exceptions. 
It is recommended to test the script on a small sample of URLs before running it on a large dataset.
