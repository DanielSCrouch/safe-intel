#!/usr/bin/env python3
import argparse
from typing import List
from pathlib import Path
from bs4 import BeautifulSoup
from requests import get as rget
import re
from urllib.parse import urljoin

# Find all files from a remote GitHub repository
def find_file_paths(user: str, repo: str, branch: str, subfolder: str):

    dir_url = "https://raw.githubusercontent.com/{}/{}/{}/{}".format(user, repo, branch, subfolder)

    result = rget(dir_url)

    soup = BeautifulSoup(result.text, 'html.parser')
    files = soup.find_all(title=re.compile("\.txt$"))

    filepaths = []
    for i in files:
        url = urljoin(dir_url + "/", i.extract().get_text())
        filepaths.append(url)

    return filepaths

# Save files to local directory
# def safe_files


# def do_work(input1_file, output1_file, param1):
#   for x, line in enumerate(input1_file):
#     if x >= param1:
#       break
#     _ = output1_file.write(line)
  
# # Defining and parsing the command-line arguments
# parser = argparse.ArgumentParser(description='My program description')
# # Paths must be passed in, not hardcoded
# parser.add_argument('--input1-path', type=str,
#   help='Path of the local file containing the Input 1 data.')
# parser.add_argument('--output1-path', type=str,
#   help='Path of the local file where the Output 1 data should be written.')
# parser.add_argument('--param1', type=int, default=100,
#   help='The number of lines to read from the input and write to the output.')
# args = parser.parse_args()

# # Creating the directory where the output file is created (the directory
# # may or may not exist).
# Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)

# with open(args.input1_path, 'r') as input1_file:
#     with open(args.output1_path, 'w') as output1_file:
#         do_work(input1_file, output1_file, args.param1)






if __name__ == "__main__":
    print(find_file_paths("DanielSCrouch", "safe-intel", "main", "files"))