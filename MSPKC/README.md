## Description
[MSPKmerCounter](http://www.cs.ucsb.edu/~yangli/MSPKmerCounter/download.html)[1] proposes a novel technique, Minimum Substring Partitioning, to reduce the memory usage of storing *k*-mers. However, it is recommended to index reads with an odd number less than 64. The software contains three functions to be run in sequence: *partition*, *count*, and *dump*. The partition step divides short read data using minimum substring partitioning, the count step computes the frequencies of existing *k*-mers, and the dump step converts the results into a human readable format. This sequel is repeated for each *k*.	

The java package files are located in /bin

```
	java -jar Partition.jar -in readfile -k k -L readlen -t 1
	java -jar Count32.jar -k k -t 1
	java -jar Dump64.jar -k k
```

## To run:
```
python2.7 mspkc.py signatures readfile outfile tmpdir
	signature = list of kmers
	readfile = fasta or fastq
	outfile = name of outfile
	tmpdir = temporary directory to store files, and will be delted by the end of the program
```

## To record the memory footprint:
```
mprof run -C python2.7 mspkc.py signatures readfile outfile tmpdir
```

### Reference:
[1]: Y.  Li  and  X.  Yan.   MSPKmerCounter:  A  Fast  and  Memory  Efficient  Approach  for  K-mer  Counting.arXivpreprint, 1505.06550:1–7, 2015.
