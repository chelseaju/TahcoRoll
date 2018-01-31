"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	v1: store kmer in set, use dump to scan through kmer (query doesn't work)
	double the count for palindrome kmers
	To Run:	
		python mspkc_count_v1.py signature readfile outfile tmpdir readlen 
	Author: Chelsea Ju
	Date: 2017-09-07

"""		
import sys, re, os, argparse, datetime, random, time

## need absolute path
COUNT="/home/chelseaju/TahcoRoll/TahcoRoll/MSPKC/bin/Count32.jar"
DUMP="/home/chelseaju/TahcoRoll/TahcoRoll/MSPKC/bin/Dump64.jar"
PARTITION="/home/chelseaju/TahcoRoll/TahcoRoll/MSPKC/bin/Partition.jar"


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


def index_reads(readfile, kmer_hash, readlen):

#	for k in xrange(65,68):
	for k in kmer_hash.keys():
		echo("\t\t k = %d" %(k))
		outdir = str(k) + "mers"
		os.system("mkdir -p %s" %(outdir))
		os.chdir(outdir)

		## CDM: java -jar Partition.jar -in readfile -k k -L readlen -t 1
		os.system("java -jar %s -in %s -k %d -L %d -t 1" %(PARTITION, readfile, k, readlen))

		## CDM: java -jar Count32.jar -k k -t 1
		os.system("java -jar %s -k %d -t 1" %(COUNT, k))

		## CDM: java -jar Dump64.jar -k k
		os.system("java -jar %s -k %d -t 1" %(DUMP, k))
		os.chdir("../")



def query_kmers( kmer_hash, final_outfile):
	outfh = open(final_outfile, 'wb')

#	for k in xrange(65,68):	
	for k in kmer_hash.keys():
		current_kmer = kmer_hash[k]

		outdir = str(k) + "mers/CountDump/"
		files =  os.listdir(outdir)
		for f in files:
			print f
			fh = open( outdir + f, 'rb')
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
	kmer = option.signature
	tmpdir = option.tmpdir
	outfile = option.outfile
	readlen = option.readlen

	start_time = time.time()

	if not os.path.exists(tmpdir):
		os.makedirs(tmpdir)

	echo("Loading Kmers")
	kmer_hash = load_kmer(kmer)

	os.chdir(tmpdir)
	echo("Indexing Reads")
	index_reads(readfile, kmer_hash, readlen)

	echo("Querying Kmers")
	query_kmers(kmer_hash,  outfile)

	os.chdir("../")

	echo("Removing Temp Files")
	os.system("rm -rf %s" %(tmpdir))

	echo("Done")
	
	print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="mspkc_count_v2.py")
	parser.add_argument("signature", type=str, help="list of kmers")
	parser.add_argument("readfile", type=str, help="sequencing reads in fastq or fasta")
	parser.add_argument("outfile", type=str, help="output filename")
	parser.add_argument("tmpdir",  type=str, help="temporary directory")
	parser.add_argument("readlen", type=int, help="read length")
  	main(parser)	

