"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	v3: use different dsk complilation
	v2: separate kmer into different buckets, check for complementary sequence (DSK2 does not output canonical kmers)
	v1: separate kmer into different files based on their sizes, load kmers into memory, scan through each kmer to get count
	To Run:	
		python dsk_v1.py signatures readfile outfile tmpdir 
	Author: Chelsea Ju
	Date: 2017-07-05
"""		
import sys, re, os, argparse, datetime, time
#from memory_profiler import memory_usage
#from time import sleep

DSK_SMALL="bin/dsk_small/"
DSK_MID="bin/dsk_mid/"
DSK_LARGE="bin/dsk_large/"
DSK_WIDE="bin/dsk_wide/"

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

"""
	Index and Query kmers
"""
def index_query_kmers_reads(kmer_hash, tmpdir, readfile, outfile):

	outfh = open(outfile, 'wb')

	min_k = min(kmer_hash.keys())
	max_k = max(kmer_hash.keys())

	if(max_k < 32):
		DSK = DSK_SMALL
	elif(max_k < 96):
		DSK = DSK_MID
	elif(min_k > 96):
		DSK = DSK_LARGE
	else:
		DSK = DSK_WIDE


	for k in kmer_hash.keys():
		current_kmer = kmer_hash[k]

		echo("Indexing %smers" %(str(k)))
		## CMD: ./bin/dsk -verbose 0 -file readfile -kmer-size k -abundance-min 0 -out tmpdir/kmers.h5 -out-tmp tmpdir -out-compress 9
		os.system("%s/dsk -verbose 0 -file %s -kmer-size %d -abundance-min 0 -out %s/%dmers.h5 -out-tmp %s -out-compress 9" %(DSK, readfile,k, tmpdir, k, tmpdir))

		echo("Dumping %smers" %(str(k)))
		## CMD: ./bin/dsk2ascii -verbose -file tmpdir/kmers.h5 -out tmpdir/kmers.txt
		os.system("%s/dsk2ascii -verbose 0 -file %s/%dmers.h5 -out %s/%dmers.txt" %(DSK, tmpdir, k, tmpdir, k))

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

		echo("Cleaning tmp files")
		os.system("rm %s/%dmers.*" %(tmpdir, k))


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

	echo("Indexing Kmers and Reads")
	index_query_kmers_reads(kmer_hash, tmpdir, readfile, outfile)

	echo("Removing Temp Files")
	os.system("rm -rf %s" %(tmpdir))	

	echo("Done")	

	print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":

	parser = argparse.ArgumentParser(prog="dsk.py")

	parser.add_argument(dest="signature", type=str, help="list of kmers")
	parser.add_argument(dest="readfile", type=str, help="read file in fasta or fastq")
	parser.add_argument(dest="outfile", type=str, help="output filename")
	parser.add_argument(dest="tmpdir", type=str, help="temporary directory")


	## these don't work with mprof 
#	parser.add_argument("-r", "--read", dest="readfile", type=str, help="sequencing read file", required = True)
#	parser.add_argument("-l", "--kmer", dest="kmer", type=str, help="list of kmers", required = True)
#	parser.add_argument("-o", "--outfile", dest="outfile", type=str, help="output filename", required = True)
#	parser.add_argument("-t", "--tmpdir", dest="tmpdir", type=str, help="temporary directory", required = True)
	main(parser)	

