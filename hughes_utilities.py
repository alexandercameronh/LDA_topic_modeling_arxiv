import gc
import gensim
import nltk
from nltk.corpus import stopwords
import numpy as np
import os
import pandas as pd
import pyLDAvis.gensim
import random
import re
import string
import time
from tqdm import tqdm

def join_files(directory_path=None):
    """
    Read JSON file(s) into DataFrame
    
    Parameters
    ----------
    filepath : str
        Filepath to directory containing JSON file(s)
        
    
    Returns
    -------
    result : DataFrame
    """
    start = time.time()
    if not isinstance(directory_path, str):
        raise TypeError("Directory path must be string")
        
    list_dfs = []
    
    for item in os.listdir(directory_path):
        temp_df = pd.read_json(os.path.join(directory_path,item))
        list_dfs.append(temp_df)
        
    full_dataframe = pd.concat(list_dfs)
    full_dataframe.reset_index(drop=True, inplace=True)
    
    print('Elapsed time: {} seconds'.format(time.time()-start))
    print('Full dataframe: {} rows, {} columns'.format(full_dataframe.shape[0], full_dataframe.shape[1]))
    return full_dataframe

def cut_table(full_table, keep=0.5):
    """
	Cut the table to a percentage of its orignal length by
	shuffling indicies and dropping appropriate rows

	Parameters
	----------
	full_table, DataFrame
		DataFrame to be cut
	keep, int or real-value in (0,1)
		Number of rows or percentage of rows to be retained
	
	Returns
	-------
	Shorter DataFrame than original

	>>> df
		A B C D
              0 0 1 2 3
	      1 2 5 2 6
              2 0 9 9 9
              3 8 9 1 1
	>>> df.cut_table(df, keep=0.5)
		A B C D
              0 0 1 2 3
	      3 8 9 1 1
	"""

    indices = list(full_table.index)
    random.shuffle(indices)

    if isinstance(keep, int):
        remove = (len(indices) - keep)
        return full_table.drop(index=indices[0:remove], axis=0)
    else:
        remove = (1 - keep)
        return full_table.drop(index=indices[0:int(len(indices)*remove)], axis=0)

def trim_table(dataframe, columns_to_keep):
    """
    Removes unwanted columns from dataframe. Does not drop columns in-place.
    
    Parameters
    ----------
    dataframe : Pandas DataFrame
        Target DataFrame to be trimmed
    columns_to_keep : single label or list-like
        Column names to be dropped
        
    Returns
    -------
    result : DataFrame
    """

    cols_remove = [x for x in list(dataframe.columns) if x not in columns_to_keep]
    dataframe = dataframe.drop(cols_remove, axis=1, inplace=False)
    return dataframe


def clean_text(x, tokenized=True):
    """Removes punctuation and other unwanted characters from string.
    
    Parameters
    ----------
    x : str
    tokenized : boolean, default True
        Specify if resulting string to be tokenized
        
    Returns
    -------
    x : str
    """
    description = x.split()
    description = [x.lower() for x in description]
    description = [str(x) for x in description]
    description = [x.translate(string.punctuation) for x in description]
    remove_digits = str.maketrans('', '', string.digits)
    description = [x.translate(remove_digits) for x in description]
    description = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in description]
    description = list(filter(None, description))
    if tokenized:
        return description
    else:
        return ' '.join(description)

def remove_stopwords(description):
    """Removes stopwords found in NLTK's generic stopwords list.

    Parameters
    ----------
    description : tokenized list of string elements

    Returns
    -------
    destription : tokenize list of string elements, not including stopwords   
    """
    stoplist = stopwords.words('english')
    description = [word.lower() for word in description if word not in stoplist]
    return description
