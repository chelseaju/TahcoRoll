## Description
KMC scan reads one block at a time, and use a number of splitter threads to process these blocks. [KMC3](http://sun.aei.polsl.pl/REFRESH/index.php?page=projects&project=kmc&subpage=about)[1] improves upon KMC and KMC2, which accelerates the running time and optimizes the memory usage by taking a larger part of the input data and better balancing the bin sizes.

We use its main program to count the *k*-mer of all sizes seen in the list, with one *k* at a time. We set the *-cs* parameter to be 4294967295 to ensure all of the frequently occurred *k*-mers are included. 

```
bin/kmc -t1 -sr1 -kK -ci0 -cs4294967295 -sf1 -sp1 readfile sampe_db tmpdir
```

KMC provides an C++ API to load the compressed *k*-mer occurrences into memory, and to retrieve the frequency of a specific *k*-mer. We develop a C++ module to utilize this API (see src/api_call_query.cpp)


## Installation
The binary source code of KMC is located in /bin.
The source code for KMC API and the code that utilizes this API is located in /src. To compile from scratch, run

```
cd src
make
```

## To run:
```
python kmc3.py signatures readfile outfile tmpdir
	signature = list of kmers
	readfile = fasta or fastq
	outfile = name of outfile
	tmpdir = temporary directory to store files, and will be delted by the end of the program
```

## To record the memory footprint:
```
mprof run -C  python2.7 kmc3.py signatures readfile outfile tmpdir
```

### Reference:
[1]: M. Kokot, M. D lugosz, and S. Deorowicz.  KMC 3: counting and manipulating k-mer statistics.Bioinformatics,3(May):1–3, may 2017
