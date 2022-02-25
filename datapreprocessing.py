#import libraries
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.util import ngrams
import contractions
import unidecode
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
# uncomment the following line if you face issues with NLTK lemmatization
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

class PreprocessText:
    # def __init__(self, inputdf):
    #     self.inputdf = inputdf

    def remove_url(self, message):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        message = re.sub(regex, '', message)
        return message

    def remove_tags(self, raw_text):
        tags_removed = re.sub('<.*?>', '', raw_text)
        return tags_removed

    def to_lowercase(self, x):
        y = x.lower()
        return y

    def remove_contractions(self, x):
        # using contractions.fix to expand the shortened words
        expanded_words = []
        for word in x.split():
            expanded_words.append(contractions.fix(word))
        expanded_text = ' '.join(expanded_words)
        return expanded_text

    def accented_to_ascii(self, text):
        text = unidecode.unidecode(text)
        return text

    def remove_whitespace(self, text):
        space_pattern = r'\s+'
        whitespace_removed = re.sub(pattern=space_pattern, repl=" ", string=text)
        # whitespace_removed = text.strip()
        return whitespace_removed

    def remove_punctuation(self, x):
        return re.sub(r'[^a-z0-9A-Z]',' ',x)

    def remove_number(self, x):
        # return ''.join([i for i in x if not i.isdigit()])
        return re.sub(r'\d+','',x)

    def remove_emojis(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        rem = emoji_pattern.sub(r'', text)
        return rem

    def tokenization(self, message):
        tokens = word_tokenize(message)
        return tokens

    def remove_stopwords(self, text):
        stop_words = set(stopwords.words('english'))
        # stop_words.add('subject')
        # stop_words.add('http')
        return " ".join([w for w in text.split() if not w in stop_words])

    def nltk_pos_tagger(self, nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    def lemmatize_sentence(self, sentence):
        lemmatizer = WordNetLemmatizer()
        stopwords_removed = self.remove_stopwords(sentence)
        nltk_tagged = nltk.pos_tag(nltk.word_tokenize(stopwords_removed))
        wordnet_tagged = map(lambda x: (x[0], self.nltk_pos_tagger(x[1])), nltk_tagged)
        lemmatized_sentence = []
        for word, tag in wordnet_tagged:
            if tag is None:
                lemmatized_sentence.append(word)
            else:
                lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
        return " ".join(lemmatized_sentence)

    def stemming(self, text):
        porter_stemmer = PorterStemmer()
        stopwords_removed = self.remove_stopwords(text)
        stem_text = " ".join([porter_stemmer.stem(word) for word in stopwords_removed.split()])
        return stem_text

    def remove_smallwords(self, text):
        # pattern = re.compile('\w{1,3}')
        # smallwords_removed = re.sub(pattern, '', text)
        smallwords_removed = re.sub(r'\b\w{,2}\b', '', text)
        return " ".join([w for w in smallwords_removed.split()])
    
    def remove_directories(self, text):
        dir_removed = re.sub(r'\w{2,}\/\w{2,}(\/\w{2,})+', "", text)
        return " ".join([w for w in dir_removed.split()])
    
    def ngram_generator(self, sentence, n=3):
        ngram = []
        ngrams_sentence = ngrams(str(sentence).split(), n)
        for item in ngrams_sentence:
            ngram.append(item)
        return ngram

