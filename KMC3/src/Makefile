## Makefile

CC=g++
PARAM=-std=c++11

query_each:
	$(CC) $(PARAM) api_call_query.cpp kmc_api/kmc_file.cpp kmc_api/kmer_api.cpp kmc_api/mmer.cpp -Ofast -o query_each

clean:
	rm -rf *.o query_each

