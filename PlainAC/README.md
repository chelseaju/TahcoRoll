## Description
As one of the baseline comparisons, we compare to the plain version of the Aho-Corasick algorithm. We tested the implementation in both Python and C++. In Python, we use one of the finest and fastest Aho-Corasick libraries, [*pyahocorasick1*](https://pypi.python.org/pypi/pyahocorasick/1.1.3). In C++, we use the public available source code implemented by Christopher Gilbert (https://github.com/cjgdev/aho_corasick). The Aho-Corasick algorithm scans through reads in linear time, but the memory footprint is expected to be large as we increase the number and size of the representative *k*-mers.

The C++ implementation uses features from C++11, and can be run directly:
```
bin/plainAC signatures reads outfile
```

plainAC_v1.py uses the python Aho-Corasick libraries; plainAC_v2.py is a wrapper function that calls the C++ implementation. 
Two scripts are used to evaluate the loading time of the automaton: plainAC_load_v1.py and plainAC_load_v2.py


## Installation
The binary code for the C++ implementation is located in /bin.
The source code is located in /src. To compile from scratch, run

```
cd src
make
```

## To run:
```
python2.7 plainAC_vX.py
	-s --signatures selected_kmers
	-i --reads read_file
	-o --outfile output_file
```

## To record the memory footprint:
```
mprof run -C python2.7 plainAC_vX.py
	-s --signatures selected_kmers
	-i --reads read_file
	-o --outfile output_file
```
