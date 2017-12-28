## Description
As one of the baseline comparisons, we compare to the plain version of the Aho-Corasick algorithm. We use one of the finest and fastest Aho-Corasick libraries in Python, [*pyahocorasick1*](https://pypi.python.org/pypi/pyahocorasick/1.1.3), as our benchmark to access the speed and memory usage. This approach scans through reads in linear time, but the memory footprint is expected to be large as we increase the number and size of the representative *k*-mers. 


## To run:
```
python plainAC_v1.py
	-s --signatures selected_kmers
	-i --reads read_file
	-o --outfile output_file
```

## To record the memory footprint:
```
mprof run -C python plainAC_v1.py
	-s --signatures selected_kmers
	-i --reads read_file
	-o --outfile output_file
```
