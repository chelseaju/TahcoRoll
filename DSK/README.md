## Description

[DSK](https://github.com/GATB/dsk)[1] is a disk-based hashing method, which divides *k*-mers into bins using a specific hash function based on the targeted memory and disk space. Since the experiments of DSK are only peformed on a small range of *k*-mers, we set *-DKSIZE_LIST* to 32 during compilation. 
 
Given a list of *k*-mers, we first load them to memory and determine the range of their sizes. We index reads with different *k's* using the main program, and dump all *k*-mer frequencies into a human readable format. The final frequencies of the representative *k*-mers are retrieved through the output from the dump function. 

The binary code of DSK is located in /bin

```
bin/dsk_wide/dsk -verbose 0 -file readfile -kmer-size k -abundance-min 0 -out tmpdir/kmers.h5 -out-tmp tmpdir -out-compress 9
bin/dsk_wide/dsk2ascii -verbose -file tmpdir/kmers.h5 -out tmpdir/kmers.txt
```

## To run:
```
python2.7 dsk.py signatures readfile outfile tmpdir
	signature = list of kmers
	readfile = fasta or fastq
	outfile = name of outfile
	tmpdir = temporary directory to store files, and will be delted by the end of the program
```

## To record the memory footprint:
```
mprof run -C  python2.7 dsk.py signatures readfile outfile tmpdir
```

### Reference:
[1]: G.  Rizk,  D.  Lavenier,  and  R.  Chikhi.   DSK:  K-mer  counting  with  very  low  memory  usage.Bioinformatics,29(5):652–653, 2013.
