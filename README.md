# S3 Downloader

This script allows you to download multiple files from an S3 bucket using multithreading. The script reads from a file named events.txt which contains a list of all the files you want to download. The script will display a progress bar showing the number of files downloaded, the total number of files to be downloaded, and the download speed in MB/s.

Please note that before running the script, you will need to fill in the necessary variables such as your S3 access and secret key, the name of the bucket, and the path to the events.txt file.

## Getting Started
1.Clone the repository to your local machine.
2.Fill in the necessary variables in the script.
3.Run the script.

## Features
Multithreading support to speed up the download process.
Progress bar displaying download progress and speed.
Ability to specify files to download via a events.txt file.

## To Be Implemented
An option to specify a prefix instead of a txt file with all the files.
## Authors
Daniel
