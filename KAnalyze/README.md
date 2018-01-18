## Description

[KAnalyze](https://sourceforge.net/projects/kanalyze/)[1] is a disk-based hasing method. It accumulates *k*-mers and writes to disk when the allocated memory is full. It allows users to count the occurrences of a list of *k*-mers instead of all possible *k*-mers. However, if the list of representative *k*-mers contains different sizes, the counting step needs to be repeated for different *k*. We first separate the representative *k*-mers into different files based on their sizes, and use its *count* mode to profile their frequencies in read data. 

The binary code of KAnalyze is located in /bin

```
bin/count -d 1 -f fastq -k k -l 1 -o tmpdir/kmer.kc -rcanonical --kmerfilter kmerfile:kmer_file -t 1 readfile
```

## To run:
```
python kanalyze.py signatures readfile outfile tmpdir
	signature = list of kmers
	readfile = fasta or fastq
	outfile = name of outfile
	tmpdir = temporary directory to store files, and will be delted by the end of the program
```

## To record the memory footprint:
```
mprof run -C  python kanalyze.py signatures readfile outfile tmpdir
```

### Reference:
[1]: P. Audano and F. Vannberg.  KAnalyze: A fast versatile pipelined K-mer toolkit.Bioinformatics, 30(14):2070–2072, jul 2014
