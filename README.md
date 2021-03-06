TahcoRoll: An Efficient Approach for Signature Profiling in Genomic Data through Vairable-Length k-mers

## Download
```
git clone https://github.com/chelseaju/TahcoRoll.git
```

## Installation
TahcoRoll is implemented in C++14, and requires compiler g++ 4.9 and above. Please run the following commands to compile the executables:
```
cd src
make
```
Binary files are also provided:
```
tahcoroll, tahcoload
```

## Data
Simulated datasets can be downloaded here: https://figshare.com/s/6f02feaf89c4ff6ddc9e

Test data is provided under /test_data

## To Run:
profiling a set of variable-length k-mers:
```
./bin/tahcoroll test_data/small_01200000_sortedAlphabet.txt test_data/sample.fq
```

tahcoload is used to evaluate the loading time of different k-mer sets. To run this script:
```
./bin/tahcoload test_data/small_01200000_sortedAlphabet.txt
```

