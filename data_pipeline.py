import numpy as np
import pandas as pd
from transformers import AutoTokenizer
import re
import string
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk import word_tokenize

# utility functions

def text_normalization(data):
    data['text'] = data['text'].apply(lambda x: x.lower())
    data['text'] = data['text'].apply((lambda x: re.sub('[%s]' % re.escape(string.punctuation), '', x)))

def remove_stop_words(data, language, get_tokenize):
    stopwords = nltk.corpus.stopwords.words(language)
    if get_tokenize:
        for i in range(data.shape[0]):
            data.at[i, 'text'] = [word for word in nltk.word_tokenize(data.at[i, 'text']) if word not in stopwords]
    else:
        for i in range(data.shape[0]):
            data.at[i, 'text'] = [word for word in nltk.word_tokenize(data.at[i, 'text']) if word not in stopwords]
            data.at[i, 'text'] = ' '.join(data.at[i, 'text'])

# set tokenizer

def get_tokenizer(model, max_length_sequence):
    if model == 'beto':
        path = 'models/BETO_RNN/bert_beto/vocab.txt'
    elif model == 'bert':
        path = 'models/BERT_CNN/bert_beto/vocab.txt'
        
    tokenizer = AutoTokenizer.from_pretrained(path, do_lower_case=True, add_special_tokens=True,
                                          max_length=max_length_sequence, pad_to_max_length=True)
    return tokenizer

# prepare data

def get_ids(tokens, tokenizer, max_seq_length):
    """Token ids from Tokenizer vocab"""
    token_ids = tokenizer.encode(tokens)
    input_ids = token_ids + [0] * (max_seq_length-len(token_ids))
    return input_ids

def get_masks(tokens, max_seq_length):
    """Mask for padding"""
    if len(tokens)>max_seq_length:
        raise IndexError("Token length more than max seq length!")
    return [1]*len(tokens) + [0] * (max_seq_length - len(tokens))

def get_segments(tokens, max_seq_length):
    """Segments: 0 for the first sequence, 1 for the second"""
    if len(tokens)>max_seq_length:
        raise IndexError("Token length more than max seq length!")
    segments = []
    current_segment_id = 0
    for token in tokens:
        segments.append(current_segment_id)
        if token == "[SEP]":
            current_segment_id = 1
    return segments + [0] * (max_seq_length - len(tokens))

def normalize_and_tokenize_data(df, max_length_sequence, tokenizer, language):
    
    text_normalization(df) # Normalize text
    remove_stop_words(df, language = language, get_tokenize = False) # Remove stop words [and Tokenize texts]
    
    all_sentences = df['text'].values
    all_words = []
    for sent in all_sentences:
        temp = []
        temp.append('[CLS]')
        i = 0
        for w in tokenizer.tokenize(sent):
            i+=1
            if i == (max_length_sequence - 1): break
            temp.append(w)
        temp.append('[SEP]')
        all_words.append(temp)

    return all_words

# callable methods

def get_inputs(text, model): # model: string
    
    df = pd.DataFrame({'text': [text]}) # transform text input into a simple pandas dataframe
     
    # set variables
    if model == 'beto':
        language = 'spanish'
        max_length_sequence = 150
    elif model == 'bert':
        language = 'english'
        max_length_sequence = 50
    
    tokenizer = get_tokenizer(model, max_length_sequence)
    
    all_words = normalize_and_tokenize_data(df, max_length_sequence, tokenizer, language)

    input_ids = np.zeros((len(all_words), max_length_sequence))
    input_masks = np.zeros((len(all_words), max_length_sequence))
    input_segments = np.zeros((len(all_words), max_length_sequence))

    for i in range(len(all_words)):
        input_ids[i,:] = np.array(get_ids(all_words[i], tokenizer, max_length_sequence)).reshape(1,-1)
        input_masks[i,:] = np.array(get_masks(all_words[i], max_length_sequence)).reshape(1,-1)
        input_segments[i,:] = np.array(get_segments(all_words[i], max_length_sequence)).reshape(1,-1)

    input_ids = input_ids.astype(int)
    
    return input_ids, input_masks, input_segments

def get_pred(input_ids, input_masks, input_segments, model): # model: instance
    y_pred = model.predict([input_ids, input_masks, input_segments])
    value = y_pred[0][0]
    label = value > 0.5
    return label, value
