#!/usr/bin/env python3
import argparse
from typing import List
from pathlib import Path
from bs4 import BeautifulSoup
from requests import get as rget
import urllib.request
import re
from urllib.parse import urljoin
import os
import time
import json

# Find all files from a remote GitHub repository
def find_file_paths(user: str, repo: str, branch: str, subfolder: str)  -> List[str]:

    dir_url = "https://github.com/{}/{}/tree/{}/{}".format(user, repo, branch, subfolder)
    raw_dir_url = "https://raw.githubusercontent.com/{}/{}/{}/{}".format(user, repo, branch, subfolder)

    result = rget(dir_url)

    soup = BeautifulSoup(result.text, 'html.parser')
    files = soup.find_all(title=re.compile("\.txt$"))

    filepaths = []
    for i in files:
        url = urljoin(raw_dir_url + "/", i.extract().get_text())
        filepaths.append(url)

    return filepaths

# Download files from url path and write to local directory
def download_files(url_paths: List[str], out_dir: str) -> List[str]: 

    filepaths = []

    for url in url_paths:
        filename = os.path.basename(url)
        filepath = os.path.join(out_dir, filename)

        with urllib.request.urlopen(url) as f:
            response = f.read().decode('utf-8').rstrip()

            file = open(filepath, 'w+')
            file.write(response)
            file.close()
        
        filepaths.append(filepath)
    
    return filepaths

# Store results in file
def store_results(respath: str, results: List[str]):
    with open(respath, 'w+') as f:
        f.write(json.dumps(results))
        print("result: ", f.read())
        # for res in results:
        #     f.write("{}\n".format(res))

if __name__ == "__main__":

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='Download files from GitHub directory')
    parser.add_argument('--user', type=str,
    help='Github username.')
    parser.add_argument('--repo', type=str,
    help='Github repository name.')
    parser.add_argument('--branch', type=str,
    help='Github branch name.')
    parser.add_argument('--subdirectory', type=str,
    help='Github sub-directory name.')
    parser.add_argument('--outdir', type=str,
    help='Path to local directory to save files to.')
    parser.add_argument('--respath', type=str,
    help='Path to file to save results to. Results are paths to each downloaded file.')
    args = parser.parse_args()

    print("user: {}".format(args.user))
    print("repo: {}".format(args.repo))
    print("branch: {}".format(args.branch))
    print("subdirectory: {}".format(args.subdirectory))
    print("outdir: {}".format(args.outdir))
    print("respath: {}".format(args.respath))

    # Creating the directory where the output file is created (the directory
    # may or may not exist).
    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    Path(args.respath).parent.mkdir(parents=True, exist_ok=True)

    url_paths = find_file_paths(args.user, args.repo, args.branch, args.subdirectory)
    results = download_files(url_paths, args.outdir)
    store_results(args.respath, results)

    time.sleep(15) 


# python3 file-collect/file-collect.py --user "DanielSCrouch" --repo "safe-intel" --branch "main" --subdirectory "files" --outdir "/tmp/tmp" --respath "/tmp/results"