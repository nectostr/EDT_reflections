import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def clear_all(text):
    text = text.lower()
    
    for simb in (".", ",", "!", "?", ";", ":", "(", ")", "\n"):
        text = text.replace(simb, " ")
    text = " " + text + " "
    for word in stopwords.words('english'):
        if word not in ["no","not", "nor", "only"]:
            word = " " + word + " "
            text = text.replace(word, " ")
    
    text = text.replace("   ", " ")
    text = text.replace("  ", " ")
    return text.strip()

def clear_some(text, some):
    text = text.lower()
    
    for word in some:
        word = " " + word + " "
        text = text.replace(word, " ")
    
    text = text.replace("   ", " ")
    text = text.replace("  ", " ")
    return text.strip()

def get_n_grams(answers, include_one=False):
    only_text_answer = pd.DataFrame(answers)
    only_text_answer.columns = ["initial"]
    sample = only_text_answer["initial"][0]
    only_text_answer[only_text_answer["initial"] == None] = ""
    only_text_answer[only_text_answer["initial"].isna()] = ""
    only_text_answer["no_stop"] = only_text_answer["initial"].apply(clear_all)
    only_text_answer["list"] = only_text_answer["no_stop"].apply(lambda x: x.split())
    
    freq = dict()
    for size in range(1 + int(not include_one),4):
        for line in only_text_answer["list"]:
            for k in range(len(line)-size):
                if len(line) >= size:
                    key = tuple(line[k:k+size])
                    freq[key] = freq.get(key, 0) + 1
                    
    freq = [(key, val) for key, val in freq.items()]
    return sorted(freq, key=lambda x: x[1], reverse=True)

def get_words_cloud(series, stopwords=None):
    series = series.apply(str.lower)
    textt = " ".join(series)    
    if stopwords is None:
        stopwords=["none", "nope", "no", "i", "the", "would", "a", "in", "it", "of", "my", "and", "also"]
    wordcloud = WordCloud(
        #The idea here is not to use corpus english stop words, since there are some that is very important for us
        stopwords=stopwords,
        collocation_threshold=4).generate(textt)
    return wordcloud

def get_santiment_result(series):
    analyzer = SentimentIntensityAnalyzer()
    results = series.apply(analyzer.polarity_scores)
    return results