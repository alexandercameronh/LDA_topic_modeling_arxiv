# LDA on some arxiv data


## Titles go here


Incase you want to run entire notebook:

```bash
wget https://www.dropbox.com/s/h7u8thivlly8a2k/Arxiv_text_data.zip

unzip Arxiv_text_data.zip
```

```bash
python join_files.py --load_directory {directory_of_jsonfiles} --save_as {result_file_name}

python join_files.py --load_directory /home/ubuntu/Arxiv_text_data/data --save_as text_data.csv
```

Now feel free to run the Jupyter Notebook, just make sure to change the file path of the csv file
