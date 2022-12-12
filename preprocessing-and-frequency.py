text = input()

import string
print(string.punctuation)

spec_chars = string.punctuation + '\n\xa0«»\t—…'

def remove_chars_from_text(text, chars):
    return "".join([ch for ch in text if ch not in chars])

text = remove_chars_from_text(text, spec_chars)

print(text)

from nltk import word_tokenize
text_tokens = word_tokenize(text)
print(text_tokens)

from nltk.corpus import stopwords
russian_stopwords = stopwords.words("russian")

filtered_tokens = []

for token in text_tokens:
    if token not in russian_stopwords:
        filtered_tokens.append(token)

print(filtered_tokens)

filtered_string = ' '.join(filtered_tokens)

from pymystem3 import Mystem

m = Mystem()
def lemmatize_sentence(text):
    lemmas = m.lemmatize(text)
    return "".join(lemmas).strip()

lemmatize_tokens = lemmatize_sentence(filtered_string)
print(lemmatize_tokens)

list_tokens = lemmatize_tokens.split()

print(list_tokens)

unique_tokens = list(set(list_tokens))

print(unique_tokens)
inf_unique_tokens = [x + '_INF' for x in unique_tokens]
print(inf_unique_tokens)

inf_unique_tokens_str = ', '.join(inf_unique_tokens)
print(inf_unique_tokens_str)

import requests, matplotx
import pandas as pd
import matplotlib.pyplot as plt

params = {
    "content": inf_unique_tokens_str,
    "year_start": "1800",
    "year_end": "2019"
}

# params = {
#     "content": "Albert Einstein,Sherlock Holmes,Bear Grylls,Frankenstein,Elon Musk,Richard Branson",
#     "year_start": "1800",
#     "year_end": "2019"
# }


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

html = requests.get("https://books.google.com/ngrams/json", params=params, headers=headers, timeout=30).text
time_series = pd.read_json(html, typ="series")

year_values = list(range(int(params['year_start']), int(params['year_end']) + 1))

for series in time_series:
    plt.plot(year_values, series["timeseries"], label=series["ngram"])

plt.title("Google Books Ngram Viewer", pad=10)
matplotx.line_labels()  # https://stackoverflow.com/a/70200546/15164646

plt.xticks(list(range(int(params['year_start']), int(params['year_end']) + 1, 20)))
plt.grid(axis="y", alpha=0.3)

plt.ylabel("%", labelpad=5)
plt.xlabel(f"Year: {params['year_start']}-{params['year_end']}", labelpad=5)
plt.show()