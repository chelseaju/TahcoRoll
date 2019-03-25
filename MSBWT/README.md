## Description

[MSBWT](https://github.com/holtjma/msbwt)[1] is designed to compress raw reads via a multi-string variant of Burrows-Wheeler Transform (BWT). The compressed and searchable representation allows counting the occurrences of any *k*-mers. Instead of concatenating all reads and sorting, MSBWT builds a BWT on each string and merges these multi-string BWTs through a small interleave array. The final structure allows a fast query of *k*-mers of arbitrary *k*. 

We build the multi-string BWTs on all reads. This compressed representation is stored in files, and later loaded in memory for frequency retrieval. It is one of the implementations that does not require scanning through reads one *k* at a time.

The binary code of MSBWT is located in /bin

### for short reads
```
bin/msbwt cffq --uniform --compressed -p 1 tmpdir readfile
bin/msbwt massquery --rev-comp tmpdir signature tmpfile
```
### for long reads
```
bin/msbwt cffq -p 1 tmpdir readfile 
bin/msbwt massquery --rev-comp tmpdir signature tmpfile
```

## To run:
```
python2.7 msbwt.py signatures readfile outfile tmpdir
	signature = list of kmers
	readfile = fasta or fastq
	outfile = name of outfile
	tmpdir = temporary directory to store files, and will be delted by the end of the program
```

## To record the memory footprint:
```
mprof run -C  python2.7 msbwt.py signatures readfile outfile tmpdir
```

### Reference:
[1]: J. Holt and L. McMillan.  Merging of multi-string BWTs with applications.Bioinformatics, 30(24):3524–31, 2014.
