import nltk
import difflib
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.metrics import jaccard_distance
import re

# Ensure that NLTK's tokenizers and stopwords are downloaded
nltk.download('punkt')
nltk.download('stopwords')

def preprocess(text):
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters, except whitespace, %, #, and ()
    text = re.sub(r'[^a-zA-Z0-9\s%#()/]', '', text, re.UNICODE)
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('norwegian'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def calculate_jaccard_similarity(text1, text2):
    # Preprocess and convert to sets
    set1, set2 = set(preprocess(text1)), set(preprocess(text2))
    # Calculate Jaccard Distance and convert to similarity
    return 1 - jaccard_distance(set1, set2)

def calculate_difflib_similarity(text1, text2):
    # Use difflib to compare sequences
    return difflib.SequenceMatcher(None, text1, text2).ratio()


# Read text from file text_plain_conf.txt
with open('app/text/mint_example/text_plain_conf', 'r') as file:
    text_plain_conf = file.read()

# Read text from file expected_output.txt
with open('app/text/mint_example/expected_output', 'r') as file:
    expected_output = file.read()

# Calculate similarities
jaccard_similarity = calculate_jaccard_similarity(text_plain_conf, expected_output)
difflib_similarity = calculate_difflib_similarity(text_plain_conf, expected_output)

print(f"Jaccard Similarity: {jaccard_similarity:.3f}")
print(f"Difflib Similarity: {difflib_similarity:.3f}")
