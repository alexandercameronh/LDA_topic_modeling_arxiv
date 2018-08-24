import os
import pandas as pd
import sys
import time
import argparse


def join_files(directory_path=None, save_as='full_dataset.csv'):
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
    full_dataframe.to_csv(save_as, index=False)

def main(load_directory, save_as):
	join_files(load_directory, save_as)
	print('Dataset saved: {}'.format(save_as))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser for column name to be passed.')

    parser.add_argument('--load_directory', dest='load_directory', type=str, required=True)
    parser.add_argument('--save_as', dest='save_as', type=str, required=True)

    args = parser.parse_args()

    main(args.load_directory, args.save_as)
