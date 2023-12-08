import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import openpyxl
import syllapy
from nltk.corpus import stopwords
import string

nltk.download('stopwords') 
nltk.download('punkt')


dictionary = {}
positive_words = []
negative_words = []

# Function to filter stopwords from the text 

def load_filtering_words_from_files():
    filtering_words = set()
    directory = "C:/Users/majeed/Desktop/blackCoffer_assignment/stopWords"
    for filename in os.listdir(directory):
        file_path = os.path.join(directory,filename)
        with open(file_path,"r") as file:
            words = [line.strip() for line in file]
            filtering_words.update(words)
    return filtering_words

def clean_text(text, filtering_words):
    words = text.split()
    cleaned_words = [word for word in words if word.lower() not in filtering_words]
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text

# Function to create a dictionary of positive and negative words excluding the words that are present in the StopWords
def load_words(file_path,word_list):
     with open(file_path,"r") as file:
        words = file.readlines()
        for word in words:
            if not check_if_exists_in_stopwords(word):
                final_word = word.replace("\n","")
                word_list.append(final_word)                       

def check_if_exists_in_stopwords(value):
    directory = "C:/Users/majeed/Desktop/blackCoffer_assignment/stopWords"
    for filename in os.listdir(directory):
        file_path = os.path.join(directory,filename)
        with open(file_path,"r") as file:
            if value in file.readlines():
                return True
                
    return False

def create_dictionary():

    directory = 'C:/Users/majeed/Desktop/blackCoffer_assignment/MasterDictionary'

    for file_name in os.listdir(directory):
    
        file_path = os.path.join(directory,file_name)
        if "positive" in file_name:
            load_words(file_path,positive_words)
        else:
            load_words(file_path,negative_words)

    dictionary['positive_words'] = positive_words
    dictionary['negative_words'] = negative_words

# count syllable in a given word
# this function is not used instead syllapy library has been used
# def syllable_count(word):
#     count = 0
#     vowels = "aeiouy"
#     # Check if the first character is a vowel
#     if word[0] in vowels:
#         count += 1
#     # Iterate through the characters in the word, starting from the second character
#     for index in range(1, len(word)):
#         # If the current character is a vowel and the previous character is not a vowel, increment the count
#         if word[index] in vowels and word[index - 1] not in vowels:
#             count += 1
#     # Handle exceptions for words ending with "ed" or "es" by decrementing the count
#     if word.endswith("ed") or word.endswith("es"):
#         count -= 1
#     # Ensure that there's at least one syllable
#     if count == 0:
#         count += 1
#     return count

# Function to perform sentiment analysis
def perform_sentiment_analysis(text):
   
    # Tokenize the text into words
    words = word_tokenize(text.lower())

    # Initialize scores
    positive_score = 0
    negative_score = 0

    # Calculate positive and negative scores
    for word in words:
        if word in dictionary["positive_words"]:
            positive_score += 1
        elif word in dictionary["negative_words"]:
            negative_score -= 1

    # Multiplying the negative score with -1 to get a positive number as instructed in text_analysis.txt file
    negative_score = negative_score * (-1)
    # Calculate Polarity Score and Subjectivity Score
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)

    return positive_score, negative_score, polarity_score, subjectivity_score

# Function to calculate readability based on Gunning Fox index
def calculate_readability(text):

    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    try:
        avg_sentence_length = len(words) / len(sentences)
        complex_word_count = sum(1 for word in words if syllapy.count(word) > 2)
        percentage_complex_word = (complex_word_count / len(words)) * 100
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_word)
    except ZeroDivisionError as e:
        avg_sentence_length = 0
        complex_word_count = 0
        percentage_complex_word = 0
        fog_index = 0
        print("empty file processed")
    
    return avg_sentence_length, percentage_complex_word, fog_index, complex_word_count

# Function to count personal pronouns
def count_personal_pronouns(text):

    personal_pronoun_count = len(re.findall(r'\b(I|we|my|ours|us)\b', text, flags=re.IGNORECASE))
    return personal_pronoun_count

# Function to get word count 
def get_word_count(text):
    
    # Tokenize the text into words
    words = text.split()

    # Remove punctuation from each word
    words = [word.strip(string.punctuation) for word in words]

    # Filter out stop words
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word.lower() not in stop_words]

    # Count the remaining words
    word_count = len(words)
    
    return word_count

# Function to calculate average word length
def calculate_average_word_length(text):
    words = word_tokenize(text)
    try:
        total_characters = sum(len(word) for word in words)
        average_word_length = total_characters / len(words)
        return average_word_length
    except ZeroDivisionError as e:
        return 0
    

def extract_data(df):
   
    # Load filtering words in a set to clean the extracted text
    filtering_words = load_filtering_words_from_files()
    
    # Loop through each row in the Excel file
    for index, row in df.iterrows():
        url = row['URL']
        url_id = row['URL_ID']

        # Extract article title and text
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # p_tags = soup.find('div', class_='td-post-content tagdiv-type, tdb-block-inner td-fix-index').find_all("p")
            p_tags = soup.select('div.td-post-content.tagdiv-type, div.tdb-block-inner.td-fix-index p')

            article_text = " ".join([p_tag.get_text() for p_tag in p_tags])

            cleaned_text = clean_text(article_text, filtering_words)
            # Save the extracted content in a text file
            output_file = f'output/{url_id}.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f'Title: {soup.title.string}\n\n')
                f.write(cleaned_text)

            print(f"Extracted {url_id}.txt")
        except AttributeError as e:
            print(f"Attribute Error for {url}: {e}")
        except Exception as e:
            print(f"Error extracting from {url}: {e}")
            output_file = f'output/{url_id}.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(" ")

def get_syllables_per_word(text):
    words = text.split()
    try:
        total_syllables = sum(syllapy.count(word) for word in words)
        return total_syllables / len(words)
    except ZeroDivisionError as e:
        return 0

def main():

    # create a dictionary of positive and negative words   
    create_dictionary()

    # Loading the Excel file
    input_file = 'input.xlsx'
    df = pd.read_excel(input_file)

    # Create a directory to save the text files
    if not os.path.exists('output'):
        os.makedirs('output')
        extract_data(df)

    directory = 'C:/Users/majeed/Desktop/blackCoffer_assignment/output'

    # Initializing lists to store the computed variables
    word_counts = []
    avg_word_lengths = []
    avg_sentence_lengths = []
    percentage_complex_words = []
    fog_indices = []
    personal_pronoun_counts = []
    average_word_lengths = []
    syllable_per_word = []
    complex_word_counts = []
    positive_scores = []
    negative_scores = []
    polarity_scores = []
    subjectivity_scores = []

    # Initializig a varible for the purpose of indicating progress
    i = 1

    for file_name in os.listdir(directory):

        file_path = os.path.join(directory,file_name)
        
        with open(file_path,"r", encoding="utf-8", errors="ignore") as file:
            article_text = " ".join(line.strip() for line in file)

            positive_score, negative_score, polarity_score, subjectivity_score = perform_sentiment_analysis(article_text)
            avg_sentence_length, percentage_complex_word, fog_index, complex_word_count = calculate_readability(article_text)
            personal_pronoun_count = count_personal_pronouns(article_text)
            average_word_length = calculate_average_word_length(article_text)

            # Append the computed variables to the respective lists
            word_counts.append(get_word_count(article_text))
            avg_word_lengths.append(average_word_length)
            syllable_per_word.append(get_syllables_per_word(article_text))
            positive_scores.append(positive_score)
            negative_scores.append(negative_score)
            polarity_scores.append(polarity_score)
            subjectivity_scores.append(subjectivity_score)
            avg_sentence_lengths.append(avg_sentence_length)
            percentage_complex_words.append(percentage_complex_word)
            fog_indices.append(fog_index)
            complex_word_counts.append(complex_word_count)
            personal_pronoun_counts.append(personal_pronoun_count)
            average_word_lengths.append(average_word_length)

        # Indicating the progress 
        print(f"{i} file done")
        i += 1

 # Adding the computed variables to the DataFrame
    df["positive_score"] = positive_scores
    df["negative_score"] = negative_scores
    df["polarity_score"] = polarity_scores
    df["subjectivity_score"] = subjectivity_scores
    df['Avg Sentence Length'] = avg_sentence_lengths
    df['Percentage of Complex Words'] = percentage_complex_words
    df['Fog Index'] = fog_indices
    df['Avg Word Length'] = avg_word_lengths
    df["Complex Word Count"] = complex_word_counts
    df['Word Count'] = word_counts
    df["Syllable Per Word"] = syllable_per_word
    df['Personal Pronoun Count'] = personal_pronoun_counts
    df['Average Word Length'] = average_word_lengths

    # Saving the updated DataFrame to a new Excel file
    output_file = 'output_structure.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"Analysis completed. Output saved to {output_file}")   

if __name__ == "__main__":
    main()
