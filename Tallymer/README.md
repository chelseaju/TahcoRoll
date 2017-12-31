## Description
[Tallymer](http://genometools.org/tools/gt_tallymer_occratio.html)[1] is tailored to detect *de novo* repetitive elements with sizes ranging from 10 to 500bp in the genome. The algorithm first constructs an enhanced suffix-array, and indexes *k*-mers for a fixed value of *k*. The indexing step needs to be repeated for different *k*'s.

We first separate a list of *k*-mers into different files based on their sizes. Tallymer builds an enhanced suffix-array on read data through the function *gt suffixerator*. Since it provides a function to query the count of a set of *k*-mers, we first separate the representative *k*-mers into different files based on their sizes. For each *k*, we use *gt tallymer mindex* to extract the *k*-mer index and count from the enhanced suffix-array, and use *gt tallymer search* to retrieve their counts. 

```
bin/gt suffixerator -dna -pl -tis -suf -lcp -v -parts 4 -db readfile -indexname tmpdir/reads
bin/gt tallymer mkindex -mersize k -minocc 1 -indexname kmer_index -counts -pl -esa reads
bin/gt tallymer search -output sequence counts -strand fp -tyr kmer_index -q kmer_file > sample_kmer_file
```

## To run:
```
python tallymer.py signatures readfile outfile tmpdir
	signature = list of kmers
	readfile = fasta or fastq
	outfile = name of outfile
	tmpdir = temporary directory to store files, and will be delted by the end of the program
```

## To record the memory footprint:
```
mprof run -C  python tallymer.py  signatures readfile outfile tmpdir
```

### Reference:
[1]: S.  Kurtz,  A.  Narechania,  J.  C.  Stein,  and  D.  Ware.   A  new  method  to  compute  K-mer  frequencies  and  itsapplication to annotate large repetitive plant genomes.BMC genomics, 9(9):517, 2008
