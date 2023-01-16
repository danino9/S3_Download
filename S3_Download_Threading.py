import concurrent.futures
import os
import boto3
import tqdm
import csv
from functools import partial
import time

def download_one_file(bucket: str, output: str, client: boto3.client, s3_file: str):
    """
    Download a single file from S3
    Args:
        bucket (str): S3 bucket where images are hosted
        output (str): Dir to store the images
        client (boto3.client): S3 client
        s3_file (str): S3 object name
    """
    client.download_file(
        Bucket=bucket, Key=s3_file, Filename=os.path.join(output,  s3_file.split("/")[-1])
    )

def txt_to_list(filename): #tranlating the txt file into list of files to download
            lst=[]
            while (line := filename.readline().rstrip()):
                lst.append(line)
            return lst

f=open("events.txt",'r')
AWS_BUCKET = "your_bucket_name"
OUTPUT_DIR = "path/to/output/directory"

files_to_download=txt_to_list(f)
# Creating only one session and one client
session = boto3.Session(aws_access_key_id='your_access_key',
              aws_secret_access_key='your_secret_key')
s3 = session.resource('s3')
client = boto3.client('s3',aws_access_key_id='your_access_key',
              aws_secret_access_key='your_secret_key')
# The client is shared between threads
func = partial(download_one_file, AWS_BUCKET, OUTPUT_DIR, client)

# List for storing possible failed downloads to retry later
failed_downloads = []

with tqdm.tqdm(desc="Downloading images from S3", total=len(files_to_download)) as pbar:
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        # Using a dict for preserving the downloaded file for each future, to store it as a failure if we need that
        futures = {
            executor.submit(func, file_to_download): file_to_download for file_to_download in files_to_download
        }
        pbar.start_t = time.time()
        for future in concurrent.futures.as_completed(futures):
            if future.exception():
                failed_downloads.append(futures[future])
            pbar.set_postfix(speed=f'{pbar.n / (time.time() - pbar.start_t):.2f}MB/s')
            pbar.update(1)
if len(failed_downloads) > 0:
    print("Some downloads have failed. Saving ids to csv")
    with open(os.path.join(OUTPUT_DIR, "failed_downloads.csv"), "w", newline="") as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(failed_downloads)
