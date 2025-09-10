# Conspiracy generation

1. Download the Reddit dump [here](https://academictorrents.com/details/1614740ac8c94505e4ecb9d88be8bed7b6afddd4/tech&filelist=1). This torrent contains data from many subreddits, so you should pick only the subreddits you want.

2. Run `python parseDumps.py <path/to/zst_dir> <path/to/output_dir>` to parse the .zst dump into a readable .csv format

3. Run `python parseCsv.py <path/to/csv_file.csv> <path/to/output_dir>` to parse a specific csv file to the .jsonl dataset.

4. Now you have the .jsonl data set with the following objects: `{title: <title>, body: <body>}`. Use this to finetune your model and generate new posts.
