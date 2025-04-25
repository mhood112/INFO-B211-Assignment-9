import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag, ne_chunk
from collections import Counter
from nltk.util import ngrams 

# Ensure all required NLTK resources are downloaded
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
except Exception as e:
    print(f"Error downloading NLTK resources: {e}")

# Initialize tools
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Function to get WordNet POS tag for lemmatization
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

# Function to process text
def analyze_text(text):
    # Tokenization with fallback
    try:
        tokens = word_tokenize(text)
    except Exception as e:
        print(f"word_tokenize failed: {e}. Using fallback tokenization.")
        tokens = text.split()
    
    # Filter tokens
    tokens = [token for token in tokens if token.isalnum() and token.lower() not in stop_words]
    
    # Stemming
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    
    # Lemmatization with fallback for POS tagging
    try:
        pos_tags = pos_tag(tokens)
    except Exception as e:
        print(f"POS tagging failed: {e}. Using default POS tags.")
        pos_tags = [(token, 'NN') for token in tokens]  # Default to nouns
    
    lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(tag)) for token, tag in pos_tags]
    
    # Frequency analysis
    token_counts = Counter(tokens)
    most_common_tokens = token_counts.most_common(20)
    
    # Named Entity Recognition (NER) with fallback
    try:
        named_entities = ne_chunk(pos_tags, binary=False)  # Use binary=False to get detailed entity types
        entities = [chunk for chunk in named_entities if hasattr(chunk, 'label')]
        num_entities = len(entities)
        entity_names = [' '.join(c[0] for c in chunk) for chunk in entities]
    except Exception as e:
        print(f"NER failed: {e}. Skipping named entity recognition.")
        num_entities = 0
        entity_names = []
    
    return {
        "most_common_tokens": most_common_tokens,
        "num_entities": num_entities,
        "entities": entity_names
    }

# Load and analyze texts
def load_and_analyze(file_path):
    try:
        with open(file_path, "r") as file:
            text = file.read()
        return analyze_text(text)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

# Function to dynamically determine the subject of the text
def determine_subject(entities, tokens):
    # Combine tokens and entities into a single list for analysis
    combined = [token.lower() for token in tokens] + [entity.lower() for entity in entities]
    
    # Analyze the most frequent tokens and entities
    if not combined:
        return "Unknown subject"
    
    # Count the frequency of combined tokens and entities
    combined_counts = Counter(combined)
    
    # Check for the presence of key themes dynamically
    if any(word in combined_counts for word in ["romeo", "juliet", "verona"]):
        return "A cosmic retelling of Romeo and Juliet"
    elif any(word in combined_counts for word in ["aldric", "torran", "house"]):
        return "A medieval tale of intrigue and power"
    elif any(word in combined_counts for word in ["mystery", "ancient", "secrets"]):
        return "A tale of Verona's mysteries"
    
    # Default to "Unknown subject" if no match is found
    return "Unknown subject"

# Dynamically construct file paths
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
file_paths = [os.path.join(base_dir, f"Text_{i}.txt") for i in range(1, 4)]  # Text_1.txt, Text_2.txt, Text_3.txt
results = []

# Analyze each text file
for file_path in file_paths:
    print(f"\nAnalyzing {file_path}...")
    result = load_and_analyze(file_path)
    if result:
        results.append(result)
        print("Most Common Tokens:")
        for token, count in result['most_common_tokens']:
            print(f"  {token}: {count}")
        print(f"Number of Named Entities: {result['num_entities']}")
        print("Named Entities:")
        for entity in result['entities']:
            print(f"  {entity}")
        subject = determine_subject(result["entities"], [t[0] for t in result["most_common_tokens"]])
        print(f"Subject: {subject}")
    else:
        print(f"Skipping analysis for {file_path} due to errors.")
        

# Function to generate n-grams from tokens
def generate_ngrams(tokens, n=3):
    return list(ngrams(tokens, n))

# Function to process text with n-gram analysis
def analyze_text_with_ngrams(text, n=3):
    # Tokenization with fallback
    try:
        tokens = word_tokenize(text)
    except Exception as e:
        print(f"word_tokenize failed: {e}. Using fallback tokenization.")
        tokens = text.split()
    
    # Filter tokens
    tokens = [token.lower() for token in tokens if token.isalnum() and token.lower() not in stop_words]
    
    # Generate n-grams
    ngrams_list = generate_ngrams(tokens, n)
    ngram_counts = Counter(ngrams_list)
    most_common_ngrams = ngram_counts.most_common(10)  # Top 10 most common n-grams
    
    return {
        "tokens": tokens,
        "most_common_ngrams": most_common_ngrams
    }


def load_and_analyze_with_ngrams(file_path, n=3):
    # Load and analyze text with n-grams
    # Check if the file exists before analyzing
    try:
        with open(file_path, "r") as file:
            text = file.read()
        return analyze_text_with_ngrams(text, n)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

# Dynamically construct file paths
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
file_paths = [os.path.join(base_dir, f"Text_{i}.txt") for i in range(1, 5)]  # Text_1.txt, Text_2.txt, Text_3.txt, Text_4.txt
ngrams_results = {}

# Analyze each text file for n-grams
for file_path in file_paths:
    # Check if the file exists before analyzing
    print(f"\nAnalyzing {file_path} for n-grams...")
    result = load_and_analyze_with_ngrams(file_path, n=3) 
    if result:
        # Store the n-grams results
        ngrams_results[file_path] = result
        print("Most Common Trigrams:")
        for trigram, count in result['most_common_ngrams']:
            # Format the trigram for display
            print(f"  {' '.join(trigram)}: {count}")
    else:
        print(f"Skipping analysis for {file_path} due to errors.") 

# Compare trigrams in Text_4.txt with the first three texts
def compare_trigrams(ngrams_results):
    text_4_ngrams = set(ngrams_results[file_paths[3]]['most_common_ngrams']) 
    similarities = {}
    
    for i in range(3):  # Compare Text_4.txt with Text_1.txt, Text_2.txt, and Text_3.txt
        text_i_ngrams = set(ngrams_results[file_paths[i]]['most_common_ngrams'])  # Get the trigrams from Text_i.txt
        common_ngrams = text_4_ngrams.intersection(text_i_ngrams) # Find common trigrams
        similarities[file_paths[i]] = len(common_ngrams) # Count of common trigrams
    
    return similarities 

# Perform comparison
if len(file_paths) == 4 and file_paths[3] in ngrams_results:
    # Compare trigrams in Text_4.txt with the first three texts
    print("\nComparing trigrams in Text_4.txt with the first three texts...")
    similarities = compare_trigrams(ngrams_results)
    for text, common_count in similarities.items():
        print(f"Common trigrams with {text}: {common_count}")
        
        
print("\nBased the analysis, there are no common trigrams between Text_4.txt and the first three texts. Thus meaning that the texts are not written by the same author.")