"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	v1: read in kmer one by one and store in set
	use temperory folder
	double the count for palindrome kmers
	To Run:
		python khmer_v1.py signature readfile outfile tmpdir	

	Note: activate khmer environment
		python2.7 -m virtualenv khmerEnv
		source khmerEnv/bin/activate

	Author: Chelsea Ju
	Date: 2017-09-20
"""		
import sys, re, os, argparse, datetime, random, time
import khmer
#from memory_profiler import memory_usage
#from time import sleep
#import jellyfish

khmer_path="khmerEnv/bin/load-into-counting.py"

def echo(msg):
        print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))


"""
    Function : return reverse complimentary sequence
"""
def reverse_complimentary(sequence):
        sequence = sequence.upper()
        rev_seq = sequence[::-1]

        rev_seq = rev_seq.replace('A', '%')
        rev_seq = rev_seq.replace('T', 'A')
        rev_seq = rev_seq.replace('%', 'T')
        rev_seq = rev_seq.replace('C', '%')
        rev_seq = rev_seq.replace('G', 'C')
        rev_seq = rev_seq.replace('%', 'G')

        return rev_seq


def load_kmer(kmerfile):
	kmer_hash = {} 
	fh = open(kmerfile, 'rb')
	for line in fh:
		line = line.rstrip()
		k = len(line)
		if(not kmer_hash.has_key(k)):
			kmer_hash[k] = set()
		
		kmer_hash[k].add(line)
	fh.close()
	return kmer_hash

def count_query_kmers( read_file, kmer_hash, tmpdir, final_outfile):
	outfh = open(final_outfile, 'wb')

	for k in kmer_hash.keys():
		echo("k = %d" %(k))
		current_kmer = kmer_hash[k]

		## indexing CMD: python khmerEnv/bin/load-into-counting.py -k 15 -M 1e10 -T 1 -q kmers.graph readfile 
		kmer_graph = tmpdir + "/" + str(k) + "mers.graph"
		os.system("%s -k %d -M 16G -T 1 -q %s %s" %(khmer_path, k, kmer_graph, read_file))
		counts = khmer.Countgraph(k, 100000000000, 1)

		counts.load(kmer_graph)
		for mer in current_kmer:
			mer_count = counts.get(mer)

			outfh.write("%s\t%d\n" %(mer, mer_count))

	outfh.close()

def main(parser):
	option = parser.parse_args()
	readfile = option.readfile
	kmer = option.signature
	tmpdir = option.tmpdir
	outfile = option.outfile

	start_time = time.time()

	if not os.path.exists(tmpdir):
		os.makedirs(tmpdir)

	echo("Loading Kmers")
	kmer_hash = load_kmer(kmer)

	echo("Counting and Querying Kmers")
	count_query_kmers(readfile, kmer_hash, tmpdir, outfile)

	echo("Removing Temp Files")
	os.system("rm -rf %s" %(tmpdir))

	echo("Done")
	
	print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="khmer.py")
	parser.add_argument(dest="signature", type=str, help="list of kmers")
	parser.add_argument(dest="readfile", type=str, help="read file in fasta or fastq")
	parser.add_argument(dest="outfile", type=str, help="output filename")
	parser.add_argument(dest="tmpdir", type=str, help="temporary file")

  	main(parser)	
#	mem_usage = memory_usage((main, (parser,)), "include-children")
#	print('Maximum memory usage: %s' % max(mem_usage))

