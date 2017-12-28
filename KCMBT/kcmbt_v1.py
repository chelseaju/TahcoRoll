"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	v2: separate the kmer into different buckets, check complimentary kmer for palindrome only 
	To Run:	
		python kmcbt_v1.py  
			-i --read fastq
			-s --kmer list of kmers
			-o --outfile
			-t --tmpdir
	Author: Chelsea Ju
	Date: 2017-07-10
"""		
import sys, re, os, argparse, datetime, random, time

## required absolute path
## change it to the path of the source code
KCMBT="/home/chelseaju/TahcoRoll/TahcoRoll/KCMBT/kcmbt_mt/bin/kcmbt"
KCMBT_DUMP="/home/chelseaju/TahcoRoll/TahcoRoll/KCMBT/kcmbt_mt/bin/kcmbt_dump"

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
	return kmer_hash


def index_query_reads(readfile, outfile, kmer_hash, tmpdir):

	outfh = open(outfile, 'wb')

	for k in kmer_hash.keys():
		current_kmer = kmer_hash[k]

		echo("\t\t k = %d" %(k))
		outprefix = tmpdir + "/" + str(k) + "mers"

		#CMD ./bin/kcmbt -k k -i readfile -t 1 
		os.system("mkdir -p %s" %(outprefix))
		os.chdir(outprefix)
		os.system("%s -k %d -i %s -t 1" %(KCMBT, k, readfile))

		#CMD ./bin/kcmbt_dump 1
		os.system("%s 1" %(KCMBT_DUMP))
		os.chdir("../../")

		## go through each kmer in the index
		fh = open(outprefix + "/" + "kmer_list.txt", 'rb')
		for line in fh:
			(mer, count) = line.rstrip().split()
			if(mer in current_kmer):
				if(mer == reverse_complimentary(mer)):
					count = int(count) * 2
				outfh.write("%s\t%d\n" %(mer, int(count)))
		fh.close()

	outfh.close()


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
	kmer_hash = load_kmer(kmer)

	echo("Indexing Reads")
	index_query_reads(readfile, outfile, kmer_hash, tmpdir)

	echo("Removing Temp Files")
	os.system("rm -rf %s" %(tmpdir))

	echo("Done")	

	print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="kmcbt_v1.py")
	parser.add_argument("-i", "--read", dest="readfile", type=str, help="sequencing read file", required = True)
	parser.add_argument("-s", "--kmer", dest="kmer", type=str, help="list of kmers", required = True)
	parser.add_argument("-o", "--outfile", dest="outfile", type=str, help="output filename", required = True)
	parser.add_argument("-t", "--tmpdir", dest="tmpdir", type=str, help="temporary directory", required = True)
  	main(parser)	
#	mem_usage = memory_usage((main, (parser,)), "include-children")
#	print('Maximum memory usage: %s' % max(mem_usage))

