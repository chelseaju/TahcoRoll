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

Test data is provided under /test_data

## To Run:
```
./bin/tahcoroll test_data/small_01200000_sortedAlphabet.txt test_data/sample.fq
```

