import pandas as pd
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import string
import sys

df = pd.read_csv('preprocessed.csv')

translation_table = str.maketrans(string.punctuation+'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                                     " "*len(string.punctuation)+'abcdefghijklmnopqrstuvwxyz')


def get_words_from_text(text):
    text = str(text)
    text = text.translate(translation_table)
    word_list = text.split()
    return word_list

def count_frequency(word_list):
    """
    Return a dictionary mapping words to frequency.
    """
    D = {}
    for new_word in word_list:
        if new_word in D:
            D[new_word] = D[new_word]+1
        else:
            D[new_word] = 1
    return D

def word_frequencies_for_text(text):
    """
    Return dictionary of (word,frequency) pairs for the given file.
    """
    word_list = get_words_from_text(text)
    freq_mapping = count_frequency(word_list)
    return freq_mapping

def inner_product(D1,D2):
    """
    Inner product between two vectors, where vectors
    are represented as dictionaries of (word,freq) pairs.

    Example: inner_product({"and":3,"of":2,"the":5},
                           {"and":4,"in":1,"of":1,"this":2}) = 14.0 
    """
    sum = 0.0
    for key in D1:
        if key in D2:
            sum += D1[key] * D2[key]
    return sum

def vector_angle(D1,D2):
    """
    The input is a list of (word,freq) pairs, sorted alphabetically.

    Return the angle between these two vectors.
    """
    numerator = inner_product(D1,D2)
    denominator = math.sqrt(inner_product(D1,D1)*inner_product(D2,D2))
    try:  
      return (numerator/denominator)
    except:
      return 0
      pass


text_1 = df['Summary'][0]
a = ""
sorted_word_list_1 = word_frequencies_for_text(text_1)
for text_2 in df['Summary']:
  sorted_word_list_2 = word_frequencies_for_text(text_2)
  distance = vector_angle(sorted_word_list_1,sorted_word_list_2)
  a = a + str(distance) + " "
