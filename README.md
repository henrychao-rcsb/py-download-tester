# py-download-tester
Simple utility to test the time to download files from various RCSB sources.

## Requirements
* Python 3 (>= 3.3)

# Running this script

Clone a copy of this repository to your local environment:

```bash
# Clone over SSH
git clone git@github.com:henrychao-rcsb/py-download-tester.git

# or clone over HTTPS
git clone https://github.com/henrychao-rcsb/py-download-tester.git
```

Then run the python script to generate an output file:

```bash
cd py-download-tester
chmod +x utility.py
./utility.py
```

After some time, there should be a `results.csv` file within the same directory as the script.
