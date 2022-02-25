import datapreprocessing
import pandas as pd
import numpy as np
import argparse


def textpreprocess_pipeline(input_df, lemmatizationFlag, ngramsFlag):
    preprocesstext = datapreprocessing.PreprocessText()
    input_df['tags_removed'] = input_df['Text'].apply(lambda x: preprocesstext.remove_tags(x))
    input_df['urlremoved'] = input_df['tags_removed'].apply(lambda x: preprocesstext.remove_url(x))
    input_df['lowercase'] = input_df['urlremoved'].apply(lambda x: preprocesstext.to_lowercase(x))
    input_df['accented_to_ascii'] = input_df['lowercase'].apply(lambda x: preprocesstext.accented_to_ascii(x))
    input_df['remove_emojis'] = input_df['accented_to_ascii'].apply(lambda x: preprocesstext.remove_emojis(x))
    input_df['contracted'] = input_df['remove_emojis'].apply(lambda x: preprocesstext.remove_contractions(x))
    input_df['dir_removed'] = input_df['contracted'].apply(lambda x: preprocesstext.remove_directories(x))
    input_df['puncts_removed'] = input_df['dir_removed'].apply(lambda x: preprocesstext.remove_punctuation(x))
    input_df['remove_number'] = input_df['puncts_removed'].apply(lambda x: preprocesstext.remove_number(x))
    input_df['whitespace_removed'] = input_df['remove_number'].apply(lambda x: preprocesstext.remove_whitespace(x))
    input_df['tokenized_text'] = input_df['whitespace_removed'].apply(lambda x: preprocesstext.tokenization(x))
    input_df['Location']='United States'
    department = ['HR', 'Finance', 'Procurement', 'Operations']
    input_df["Department"] = np.random.choice(department, size=len(input_df))
    if lemmatizationFlag:
        input_df['lemmatized_text'] = input_df['whitespace_removed'].apply(lambda x: preprocesstext.lemmatize_sentence(x))
        input_df['smallwords_removed'] = input_df['lemmatized_text'].apply(lambda x: preprocesstext.remove_smallwords(str(x)))
        if ngramsFlag:
            input_df['ngrams'] = input_df['lemmatized_text'].apply(lambda x: preprocesstext.ngram_generator(x, 2))
    else:
        input_df['stemmed_text'] = input_df['whitespace_removed'].apply(lambda x: preprocesstext.stemming(x))
        input_df['smallwords_removed'] = input_df['stemmed_text'].apply(lambda x: preprocesstext.remove_smallwords(str(x)))
        if ngramsFlag:
            input_df['ngrams'] = input_df['stemmed_text'].apply(lambda x: preprocesstext.ngram_generator(x, 2))
    return input_df

#if __name__ == '__main__':
 #   parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
  #  parser.add_argument('--input_path',
          #              default=r"Email_Data.csv",
           #             type=str)
   # parser.add_argument('--lemmatizationFlag', default=True, type=str)
    #parser.add_argument('--ngramsFlag', default=False, type=str)
    # parser.add_argument('--n', default=2, type=int)

    #FLAGS = parser.parse_args()
    #inp_path = FLAGS.input_path
    #lemmatization_flag = FLAGS.lemmatizationFlag
    #ngrams_flag = FLAGS.ngramsFlag
    # n=FLAGS.n

    #input_df = pd.read_csv(inp_path)
    #output_df = textpreprocess_pipeline(input_df, lemmatization_flag, ngrams_flag)
    #print(output_df.head())
    #if lemmatization_flag:
     #   output_df.to_csv('Results/PreprocessResult_Lemmatized.csv')
    #else:
     #   output_df.to_csv('Results/PreprocessResult_Stemmed.csv')
