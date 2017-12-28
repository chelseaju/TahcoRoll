## Description
As one of the baseline comparison, the naive implementation is to scan through reads multiple times with different window sizes. A list of representative k-mers is loaded into memory using a hash table, where the key stores a k-mer and the value stores its occurrence. Each read is scanned d times where d is the number of different sizes we observed in the list. Theoretically, the naive implementation is light in memory since we only store the representative k-mers, but requires an extensive running time.


## To Run:
```
 python naive_v1.py 
	-s --signatures selected_kmers
        -i --reads read_file
        -o --outfile output_file
```

