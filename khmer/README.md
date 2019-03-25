## Description

To avoid counting *k*-mers with sequencing errors, [khmer](https://khmer.readthedocs.io/en/stable/user/install.html)[1] uses a streaming-based probabilistic data structure, CountMin Sketch[2]. This algorithm is designed to perform in-memory nucleotide sequence *k*-mer counting, and cannot handle *k* larger than 32. We use its Python wrapper script, *load-into-counting*, to perform counting, which writes a *k*-mer graph for each *k* to files. We repeate this step for different *k*'s. Each *k*-mer graph is loaded back to the memory one at a time, allowing us to query the count. We set the maximum amount of memory for the data structure to be 16G as the required parameter.

To install and setup khmer environment:
```
python2.7 -m virtualenv khmerEnv
source khmerEnv/bin/activate
pip2 install khmer
source khmerEnv/bin/activate
```

We use the following khmer command:
```
khmerEnv/bin/python2.7 khmerEnv/bin/load-into-counting.py -k k -M 16G -T 1 -q kmers.graph readfile
```

## To run the wrapper function:
```
khmerEnv/bin/python2.7 khmer.py signatures readfile outfile tmpdir
	signature = list of kmers
	readfile = fasta or fastq
	outfile = name of outfile
	tmpdir = temporary directory to store files, and will be delted by the end of the program
```

## To record the memory footprint:
```
mprof run -C  khmerEnv/bin/python2.7 khmer.py signatures readfile outfile tmpdir
```

### Reference:
[1] Q. Zhang, J. Pell, R. Canino-Koning, A. C. Howe, and C. T. Brown.  These are not the K-mers you are lookingfor: Efficient online K-mer counting using a probabilistic data structure.PLoS ONE, 9(7), 2014.

[2] G. Cormode and S. Muthukrishnan.  An improved data stream summary: The count-min sketch and its applica-tions.Journal of Algorithms, 55(1):58–75, 2005.
