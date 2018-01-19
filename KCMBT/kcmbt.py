"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	v2: separate the kmer into different buckets, check complimentary kmer for palindrome only 
	To Run:	
		python kcmbt.py signature readfile outfile tmpdir 
	Author: Chelsea Ju
	Date: 2017-07-10
"""		
import sys, re, os, argparse, datetime, random, time
#from memory_profiler import memory_usage
#from time import sleep

KCMBT="/home/chelseaju/TahcoRoll/TahcoRoll/KCMBT/bin/kcmbt"
KCMBT_DUMP="/home/chelseaju/TahcoRoll/TahcoRoll/KCMBT/bin/kcmbt_dump"

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
			kmer_hash[k] = {}
		kmer_hash[k][line] = 0
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
			rc_mer = reverse_complimentary(mer)

			if(current_kmer.has_key(mer) and current_kmer.has_key(rc_mer)):
				current_kmer[mer] += int(count)*2
			elif(current_kmer.has_key(mer)):
				current_kmer[mer] += int(count)
			elif(current_kmer.has_key(rc_mer)):
				current_kmer[rc_mer] += int(count)
		fh.close()

		for mer in current_kmer.keys():
			outfh.write("%s\t%d\n" %(mer, current_kmer[mer]))

	outfh.close()


def main(parser):
	option = parser.parse_args()
	readfile = option.readfile
	kmer = option.signature
	outfile = option.outfile
	tmpdir = option.tmpdir
	

	start_time = time.time()
	if not os.path.exists(tmpdir):
		os.makedirs(tmpdir)

	echo("Loading Kmers")
	kmer_hash = load_kmer(kmer)

	echo("Indexing Reads")
	index_query_reads(readfile, outfile, kmer_hash, tmpdir)

#	echo("Removing Temp Files")
#	os.system("rm -rf %s" %(tmpdir))

	echo("Done")	

	print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="kcmbt.py")
	parser.add_argument("signature", type=str, help="list of kmers")
	parser.add_argument("readfile", type=str, help="reads in fasta or fastq")
	parser.add_argument("outfile", type=str, help="output filename")
	parser.add_argument("tmpdir", type=str, help="temporary directory")

#   	parser.add_argument("-r", "--read", dest="readfile", type=str, help="sequencing read file", required = True)
#	parser.add_argument("-l", "--kmer", dest="kmer", type=str, help="list of kmers", required = True)
#	parser.add_argument("-o", "--outfile", dest="outfile", type=str, help="output filename", required = True)
#	parser.add_argument("-t", "--tmpdir", dest="tmpdir", type=str, help="temporary directory", required = True)

	main(parser)	

