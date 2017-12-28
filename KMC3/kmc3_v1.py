"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	separate kmer into different files based on their sizes, and use kmc_api to query
	To Run:	
		python kmc3_v1.py  
			-i --read fastq
			-s --kmer list of kmers
			-o --outfile
			-t --tmpdir
	Author: Chelsea Ju
	Date: 2017-07-02
"""		
import sys, re, os, argparse, datetime, time
#from memory_profiler import memory_usage
#from time import sleep


## Note: change the absolute path to where kmc located
KMC3="/home/chelseaju/TahcoRoll/KMC3/bin/kmc"
KMC3TOOL="/home/chelseaju/TahcoRoll/KMC3/bin/kmc_tools"
KMC3DUMP="/home/chelseaju/TahcoRoll/KMC3/bin/kmc_dump"
QUERY="/home/chelseaju/TahcoRoll/KMC3/bin/query_each"

def echo(msg):
        print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))

"""
	seperate kmers into different files based on kmer size
"""
def load_kmer(kmerfile, tmpdir):
	kmer_hash = {} 
	fh = open(kmerfile, 'rb')
	for line in fh:
		line = line.rstrip()
		k = len(line)
		
		if(not kmer_hash.has_key(k)):
			filename = tmpdir + "/" + "kmer_" + str(k) + ".txt"
			kmer_hash[k] = open(filename, "wb")
			
		kmer_hash[k].write("%s\n" %(line))
	fh.close()

	for k in kmer_hash.keys():
		kmer_hash[k].close()

	return kmer_hash.keys()

"""
	Index kmer using KMC
"""
def index_kmers_reads(kmer_size, tmpdir, readfile):
	for k in kmer_size:
	
		sample_db = tmpdir + "/" + "sample_" + str(k)
		#CMD: ./kmc -t1 -sr1 -kK -ci0 -cs4294967295 -sf1 -sp1 readfile sampe_db tmpdir
		os.system("%s -k%s -t1 -sr1 -sf1 -sp1 -ci0 -cs4294967295  %s %s %s" %(KMC3, str(k), readfile, sample_db, tmpdir))

"""
	Query kmer and output results
"""
def query_kmers(kmer_size, tmpdir, outfile):
	for k in kmer_size:
		kmer_file = tmpdir + "/" + "kmer_" + str(k) + ".txt"
		sample_db = tmpdir + "/" + "sample_" + str(k)
		sample_kmer_file = tmpdir + "/" + "sample_kmer_" + str(k) + ".txt"

		#CMD: ./query_each sample_db kmer_file outfile
		os.system("%s  %s %s %s" %(QUERY, sample_db, kmer_file, sample_kmer_file))

		## merging results
		os.system("cat %s >> %s " %(sample_kmer_file, outfile)) 


def main(parser):
	option = parser.parse_args()
	readfile = option.readfile
	kmer = option.kmer
	outfile = option.outfile
	tmpdir = option.tmpdir

	start_time = time.time()

	if not os.path.exists(tmpdir):
		os.makedirs(tmpdir)

	echo("Loading Kmers")
	kmer_size = load_kmer(kmer, tmpdir)

	echo("Indexing Kmers and Reads")
	index_kmers_reads(kmer_size, tmpdir, readfile)

	echo("Querying Kmers")
	fh = open(outfile, 'wb') ## clear file
	fh.close()
	query_kmers(kmer_size, tmpdir, outfile)

	echo("Removing Temp Files")
	os.system("rm -rf %s" %(tmpdir))	

	echo("Done")	

	print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="kmc3_v1.py")
	parser.add_argument("-i", "--read", dest="readfile", type=str, help="sequencing read file", required = True)
	parser.add_argument("-s", "--kmer", dest="kmer", type=str, help="list of kmers", required = True)
	parser.add_argument("-o", "--outfile", dest="outfile", type=str, help="output filename", required = True)
	parser.add_argument("-t", "--tmpdir", dest="tmpdir", type=str, help="temporary directory", required = True)
	main(parser)	
#	mem_usage = memory_usage((main, (parser,)), "include-children")
#	print('Maximum memory usage: %s' % max(mem_usage))

