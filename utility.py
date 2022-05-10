#!/usr/bin/env python3

import time, urllib.request, random

legacy_download_source="https://files.rcsb.org/download"
legacy_http_source="https://files.rcsb.org/pub/pdb"
cloud_http_source="https://s3.rcsb.org/pub/pdb"

test_files = {
    "4hhb": { # 107 KB
        "http": "data/structures/divided/pdb/hh/pdb4hhb.ent.gz",
        "download": "4hhb.pdb.gz",
    },
    "5hhf": { # 673 KB
        "http": "data/structures/divided/pdb/hh/pdb5hhf.ent.gz",
        "download": "5hhf.pdb.gz",
    },
    "1d8w": { # 295 KB
        "http": "data/biounit/coordinates/divided/d8/1d8w.pdb1.gz",
        "download": "1d8w.pdb1.gz",
    },
    "ls-lR": { #399 MB
        "http": "ls-lR",
    },
    "current_file_holdings": { # 11 MB
        "http":  "holdings/current_file_holdings.json.gz",
    }
}

output_file = "results.csv"

def init_output_file():
    """
    Initializes the output file to store the results of the tests
    """
    with open(output_file, 'w') as outfile:
        outfile.write("FILENAME,METHOD,TRIAL,URL,START TIME (sec),END TIME (sec),TOTAL TIME (sec)\n")

def download_file(url):
    """
    Downloads a file from the remote URL, and return a dictionary containing timing metrics around the request
    
    Arguments:
        url - URL string to the remote resource

    Returns:
        A dictionary object with the start and end time (in fractional seconds) of the request, along with the original url requested.
    """
    starttime = time.perf_counter()    
    response = urllib.request.urlopen(url)
    response.read()
    endtime = time.perf_counter()

    time.sleep(random.uniform(2,5))

    return {
        'url': url,
        'starttime': starttime,
        'endtime': endtime,
    }

def write_out_results(file_name, method, trial, result):
    """
    Writes out the results of the request to the output file.

    Arguments:
        file_name - An identifier of the file requested
        method - An identifier from which location the file was requested (either 'http' or 'download')
        trial - The attempt account downloading this file
        result - A dictionary object returned from the download_file function
    """
    with open(output_file, 'a') as outfile:
        outfile.write(f"{file_name},{method},{trial},{result['url']},{result['starttime']},{result['endtime']},{result['endtime'] - result['starttime']}\n")

def download_and_write(file_name, source, method, iterations):
    """
    Starts the test for a file.

    Arguments:
        file_name - An identifier of the file requested
        source - The root of the URL for the file
        method - An identifier from which location the file was requested (either 'http' or 'download')
        iterations - The number of times to download the file
    """
    print(f"Downloading from {source}")
    for i in range(iterations):
        url = f"{source}/{file[method]}"
        result = download_file(url)
        write_out_results(file_name, method, i, result)

if __name__ == "__main__":
    random.seed()
    init_output_file()

    for filename in test_files:
        file = test_files[filename]
        print(f"Testing downloads of {filename}")
        if "download" in file.keys():
            download_and_write(filename, legacy_http_source, "http", 5)
            download_and_write(filename, cloud_http_source, "http", 5)
            download_and_write(filename, legacy_download_source, "download", 5)
        else:
            download_and_write(filename, legacy_http_source, "http", 2)
            download_and_write(filename, cloud_http_source, "http", 2)