"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	v1: separate kmer into different files based on their sizes, load kmers into memory, scan through each kmer to get count
	To Run:	
		python bfcounter.py signature readfile outfile tmpdir 
	Author: Chelsea Ju
	Date: 2017-08-09
	Last Modify: 2018-01-03
"""		
import sys, re, os, argparse, datetime, time
#from memory_profiler import memory_usage
#from time import sleep

BFCOUNTER_SMALL="/home/chelseaju/TahcoRoll/TahcoRoll/BFCounter/bin/BFCounter_SMALL/BFCounter"  ## compiled with MAX_KMER_SIZE=32
BFCOUNTER_MID="/home/chelseaju/TahcoRoll/TahcoRoll/BFCounter/bin/BFCounter_MID/BFCounter"      ## compiled with MAX_KMER_SIZE=96
BFCOUNTER_LARGE="/home/chelseaju/TahcoRoll/TahcoRoll/BFCounter/bin/BFCounter_LARGE/BFCounter"  ## compiled with MAX_KMER_SIZE=160
KMERSTREAM="/home/chelseaju/TahcoRoll/TahcoRoll/BFCounter/bin/KmerStream/KmerStream"


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


"""
	seperate kmers into different files based on kmer size
"""
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

def kmer_estimation(kmer_sizes, readfile, tmpdir):
	
	kmer_count = {}

	echo("Calling KmerStream")
	## CMD ./KmerStream/KmerStream -k [list of k] -o kmer_estimation.txt -t 1 readfile --tsv
	os.system("%s -k %s -o %s/%s -t 1 %s --tsv" %(KMERSTREAM, ",".join([str(k) for k in kmer_sizes]), tmpdir, "nKmers.tsv", readfile))

	fh = open(os.path.join(tmpdir, "nKmers.tsv"), "r")
	line = fh.readline()
	for line in fh:
		(Q, k, F0, f1, F1) = line.rstrip().split()
		kmer_count[int(k)] = F0		
	fh.close()

	return kmer_count



"""
	Index and Query kmers
"""
def index_query_kmers_reads(kmer_hash, kmer_count, tmpdir, readfile, outfile):

	outfh = open(outfile, 'wb')

	for k in kmer_hash.keys():
		current_kmer = kmer_hash[k]
		echo("Indexing %smers" %(str(k)))

		if(k < 32):
			BFCOUNTER = BFCOUNTER_SMALL
		elif (k < 84):
			BFCOUNTER = BFCOUNTER_MID
		elif (k < 152):
			BFCOUNTER = BFCOUNTER_LARGE

		## CMD: ./BFCounter count -k k -n numK -t 1 -o outfile readfile
		os.system("%s count -k %d -n %s -t 1 -o %s/%dmers.compress %s" %(BFCOUNTER, k, kmer_count[k], tmpdir,k, readfile))

		echo("Dumping %smers" %(str(k)))
		## CMD: ./BFCounter dump -k k -i kmers.compress -o kmers.txt
		os.system("%s dump -k %d -i %s/%dmers.compress -o %s/%dmers.txt" %(BFCOUNTER, k, tmpdir, k, tmpdir, k))

		echo("Querying %smers" %(str(k)))
		fh = open(tmpdir + "/" + str(k) + "mers.txt", 'rb')
		for line in fh:
			(mer, count) = line.rstrip().split()
			
			rc_mer = reverse_complimentary(mer)
				
			if(mer in current_kmer):
				if(mer == rc_mer):
					count = int(count) * 2
				outfh.write("%s\t%d\n" %(mer, int(count)))
		
			elif(rc_mer in current_kmer):
				outfh.write("%s\t%s\n" %(rc_mer, count))
		fh.close()

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

	echo("Total Kmer Estimation")
	kmer_count = kmer_estimation(kmer_hash.keys(), readfile, tmpdir)

	
	echo("Indexing Kmers and Reads")
	index_query_kmers_reads(kmer_hash, kmer_count, tmpdir, readfile, outfile)


	#echo("Removing Temp Files")
	#os.system("rm -rf %s" %(tmpdir))	

	echo("Done")	

	print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="bfcounter.py")

	parser.add_argument("signature", type=str, help="list of kmers")
	parser.add_argument("readfile", type=str, help="reads in fastq or fasta")
	parser.add_argument("outfile", type=str, help="output filename")
	parser.add_argument("tmpdir", type=str, help="temporary directory")

#	parser.add_argument("-i", "--read", dest="readfile", type=str, help="sequencing read file", required = True)
#	parser.add_argument("-s", "--kmer", dest="kmer", type=str, help="list of kmers", required = True)
#	parser.add_argument("-o", "--outfile", dest="outfile", type=str, help="output filename", required = True)
#	parser.add_argument("-t", "--tmpdir", dest="tmpdir", type=str, help="temporary directory", required = True)

	main(parser)	

