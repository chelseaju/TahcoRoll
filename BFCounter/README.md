## Description

[BFCounter](https://github.com/pmelsted/BFCounter)[1] uses Bloom filter to identify all *k*-mers that are present more frequently than a threshold with a low false positive rate. The algorithm scans read data in two passes. Since the experiments of BFCounter are only peformed on a small range of k-mers, we set MAX_KMER_SIZE=32 during compilation.

The count function of BFCounter requires an estimation of the number of *k*-mers. We use [KmerStream](https://github.com/pmelsted/KmerStream)[2] to pre-compute the *k*-mer statistics in reads.
```
bin/KmerStream/KmerStream -k [list of kmer sizes] -o kmer_estimation.txt -t 1 readfile --tsv
```

We use the *dump* function to convert the results into human readable format to extract the frequencies.
```
bin/BFCounter_SMALL/BFCounter count -k k -n numK -t 1 -o outfile readfile
bin/BFCounter_SMALL/BFCounter dump -k k -i kmers.compress -o kmers.txt
```

## To run:
```
python2.7 bfcounter.py signatures readfile outfile tmpdir
    signature = list of kmers
    readfile = fasta or fastq
    outfile = name of outfile
    tmpdir = temporary directory to store files, and will be delted by the end of the program
```

## To record the memory footprint:
```
mprof run -C  python2.7 bfcounter.py signatures readfile outfile tmpdir
```

### Reference:
[1]: P. Melsted and J.K. Pritchard. Efficient counting of k-mers in DNA sequences using a bloom filter. BMC Bioinformatics,12:333, 2011.

[2]: P. Melsted and B.J. Halldorsson. KmerStream: streaming algorithms for k-mer abundance estimation. Bioinformatics, 30(24):3541-3547, 2014.
