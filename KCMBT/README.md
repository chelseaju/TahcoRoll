## Description
[KCMBT](https://github.com/abdullah009/kcmbt_mt)[1] uses a cache efficient burst trie to store compact *k*-mers. The trie structure stores *k*-mers that share the same prefix in the same container, when a container is full, *k*-mers are sorted and burst. It is however limited to process *k*-mers with *k* less than 32. 

We first load the list of *k*-mers into memory. KCMBT generates binary files containing *k*-mers and their counts. We use *kcmbt_dump* to convert the binary data into human readable files. We scan through each *k*-mer in the output files to extract the frequency of our representative *k*-mers. 

The binary code of KCMBT is located in /bin

```
bin/kcmbt -k k -i readfile -t 1
bin/kcmbt_dump 1
```


## To run:
```
python kmcbt_v1.py
	-i --read fastq
	-s --kmer list of kmers
	-o --outfile
	-t --tmpdir directory to store temporary files, which is required for kcmbt_dump
```

## To record the memory footprint:
```
mprof run -C python kmcbt_v1.py
    -i --read fastq
    -s --kmer list of kmers
    -o --outfile
    -t --tmpdir directory to store temporary files, which is required for kcmbt_dump
```

### Reference:
[1]: A. A. Mamun, S. Pal, and S. Rajasekaran. KCMBT: A k-mer Counter based on Multiple Burst Trees.Bioinfor-matics, 32(18):2783–2790, sep 2016
