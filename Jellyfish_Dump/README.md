## Description

[Jellyfish](http://www.genome.umd.edu/jellyfish.html)[1] exploits the CAS (compare-and-swap) assembly instruction to update a memory location in a multi-threaded environment, and uses the 'quotienting technique' and bit-packed data structure to reduce wasted memory. It provides an efficient function to count a list of representative *k*-mers and dump the results to a human readable format. 

We first split the *k*-mers into different files based on their size *k*. We then repeate the counting step for different *k*'s.

The binary code of Jellyfish is located in /bin

```
bin/jellyfish count -m k -t 1 -s 100M -C --if=kmerfile readfile -o countfile
bin/jellyfish dump -c countfile >> countresult
```

## To run:
```
python jellyfish.py signatures readfile outfile tmpdir
	signature = list of kmers
	readfile = fasta or fastq
	outfile = name of outfile
	tmpdir = temporary directory to store files, and will be delted by the end of the program
```

## To record the memory footprint:
```
mprof run -C  python2.7 jellyfish.py signatures readfile outfile tmpdir
```

### Reference:
[1]: G. Mar ̧cais and C. Kingsford.  A fast, lock-free approach for efficient parallel counting of occurrences of k-mers.Bioinformatics, 27(6):764–770, 2011.
