#!/usr/bin/env python3
import argparse
from typing import List
from pathlib import Path
from requests import get as rget
from urllib.parse import urljoin
import os
import time
from minio import Minio

def create_cloud_storage_client(storageurl: str, accesskey: str, secretkey: str, region: str) -> Minio:
    return Minio(storageurl, accesskey, secretkey, secure=False)

def upload_file(filepath: str, client: Minio, bucket: str) -> str:

    filename = os.path.basename(filepath)
    
    try:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
    except Exception as e:
        raise(e)
    
    try:
        client.fput_object(bucket, filename, filepath, content_type="text/plain")
    except Exception as e:
        raise(e)

    return "{}/{}".format(bucket, filename)


# Store results in file
def store_results(respath: str, res: str):
    with open(respath, 'w+') as f:
        f.write(res)

if __name__ == "__main__":

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='Upload local file to MinIO Cloud Storage')
    parser.add_argument('--filepath', type=str,
    help='Path to file for upload.')
    parser.add_argument('--storageurl', type=str,
    help='URL of MinIO Cloud storage.')
    parser.add_argument('--accesskey', type=str,
    help='Access key for MinIO Cloud storage.')
    parser.add_argument('--secretkey', type=str,
    help='Secret key for MinIO Cloud storage.')
    parser.add_argument('--region', type=str,
    help='MinIO Cloud storage region.')
    parser.add_argument('--bucket', type=str,
    help='MinIO Cloud storage bucket.')
    parser.add_argument('--respath', type=str,
    help='Path to file to save results to. Result is bucket/filename.')

    args = parser.parse_args()

    print("filepath: {}".format(args.filepath))
    print("storageurl: {}".format(args.storageurl))
    print("accesskey: {}".format(args.accesskey))
    print("secretkey: {}".format(args.secretkey))
    print("region: {}".format(args.region))
    print("bucket: {}".format(args.region))
    print("respath: {}".format(args.respath))

    # Creating the directory where the output file is created (the directory
    # may or may not exist).
    Path(args.respath).parent.mkdir(parents=True, exist_ok=True)

    cloud_client = create_cloud_storage_client(args.storageurl, args.accesskey, args.secretkey, args.region)
    res = upload_file(args.filepath, cloud_client, args.bucket)
    store_results(args.respath, res)

    time.sleep(10) 


# python3 file-upload/file-upload.py --filepath "/tmp/test-file-1.txt" --storageurl "18.132.68.212:8082" --accesskey "admin" --secretkey "admin1234" --bucket "test" --region "" --respath "/tmp/results"