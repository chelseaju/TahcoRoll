## Description
As one of the baseline comparisons, the naive implementation is to scan through the read sequence multiple times with different window sizes. A list of representative *k*-mers is loaded into memory using a hash table, where the key stores a *k*-mer and the value stores its occurrence. Each read is scanned *d* times where *d* is the number of different sizes we observed in the list. Theoretically, the naive implementation is light in memory since we only store the representative k-mers, but requires an extensive running time.

The Naive method is implemented in C++11.

## Installation
```
cd src
make
```

## To run:
```
python naive.py signatures readfile outfile tmpdir
	signature = list of kmers
	readfile = fasta or fastq
	outfile = name of outfile
	tmpdir = temporary directory to store files, and will be delted by the end of the program
```

## To record the memory footprint:
```
mprof run -C python naive.py signatures readfile outfile tmpdir 
```
