# INFO-B211-Assignment-9

## Purpose

The purpose of this project is to perform natural language processing (NLP) analysis on four text files (Text_1.txt, Text_2.txt, Text_3.txt, and Text_4.txt). This project includes:
  - Tokenization, Stemming, and Lemmatization: To identify the 20 most common tokens in each text.
  - Named Entity Recognition (NER): To count and list named entities in each text.
  - Subject Determination: To infer the subject of each text dynamically based on its content.
  - N-Gram Analysis: To generate trigrams (n=3) for each text and compare the trigrams of Text_4.txt with the first three texts to determine if any of the authors of the first three texts wrote the fourth text.

---

## Class Design and Implementation

### Tokenization, Stemming, and Lemmatization
  - **Purpose**
      -  To process the text and extract the most common tokens.
  - **Functions**
      - analyze_text(text):
          - Tokenizes the text using word_tokenize.
          - Filters out stopwords and non-alphanumeric tokens.
          - Applies stemming using PorterStemmer and lemmatization using WordNetLemmatizer.
          - Performs frequency analysis to identify the 20 most common tokens.
      - **Attributes**
          - most_common_tokens: A list of the 20 most frequent tokens in the text.
          - num_entities: The number of named entities in the text.
          - entities: A list of named entities extracted from the text.

### Named Entity Recognition
  - **Purpose**
      - To identify and count named entities in the text.
  - **Implementation**
      - Uses ne_chunk from NLTK to extract named entities.
      - Filters and formats the named entities into a readable list.
  - **Attributes**
      - num_entities: The total count of named entities in the text.
      - entities: A list of named entities.

### Subject Determination
  - **Purpose**
      - To dynamically infer the subject of each text based on its content.
  - **Function**
      - determine_subject(entities, tokens):
          - Combines tokens and named entities into a single list.
          - Uses frequency analysis to identify key themes dynamically.
          - Infers the subject based on the presence of thematic words (e.g., "romeo," "juliet," "verona").
      - **Attribute**
          - subject: A string representing the inferred subject of the text.

### N-Gram Analysis
  - **Purpose**
      - To generate trigrams (n=3) for each text and compare the trigrams of Text_4.txt with the first three texts.
  - **Functions**
      - generate_ngrams(tokens, n=3):
          - Generates n-grams from a list of tokens.
      - analyze_text_with_ngrams(text, n=3):
          - Tokenizes the text, filters stopwords, and generates trigrams.
          - Identifies the 10 most common trigrams in the text.
      - compare_trigrams(ngrams_results):
          - Compares the trigrams of Text_4.txt with those of Text_1.txt, Text_2.txt, and Text_3.txt.
          - Calculates the number of common trigrams between Text_4.txt and each of the other texts.
      - **Attribute**
          - file_paths: A list of file paths for Text_1.txt, Text_2.txt, Text_3.txt, and Text_4.txt.
  ---

  ## Limitations

  **Predefined Keywords for Subject Determination:**
    - The subject determination logic relies on predefined keywords (e.g., "romeo," "juliet," "verona").      - This limits its ability to infer subjects for texts with entirely different themes.
    - Future improvements could involve machine learning models for topic modeling.

  **Error Handling**
    - The script handles missing files and tokenization errors but does not account for malformed or non-text files.

  ---

  ## Conclusion

  This project provides a comprehensive analysis of the texts provided. It utilized the following techniques above to determine the subject of each text and authorship of the others. Based on the results, text_4 was not written by any of the other authors of the other texts. Text_1, text_2, and text_3 all had overrall similar subjects of their stories. 
    



