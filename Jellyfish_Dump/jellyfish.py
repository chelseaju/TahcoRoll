"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	    v2: separate kmer into different files, and use --if to count their frequency

	To Run:	
		python jellyfish_dump_v2.py signature readfile outfile tmpdir
	Author: Chelsea Ju
	Date: 2017-06-08
	Last Modify: 2017-12-31
"""		
import sys, re, os, argparse, datetime, random, time

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
	Split k-mers into different files based on their k
"""
def load_kmer(kmerfile, tmpdir):
	kmer_hash = {} 
	fh = open(kmerfile, 'rb')
	for line in fh:
		line = line.rstrip()
		k = len(line)
		if(not kmer_hash.has_key(k)):
			kmer_hash[k] = open(tmpdir + "/" + str(k) + "mers.fa", 'wb')

		kmer_hash[k].write(">1\n%s\n" %(line))
	fh.close()

	for v in kmer_hash.values():
		v.close()

	return kmer_hash.keys()

def index_query_reads(readfile, tmpdir, kmer_k, outfile):

	tmpfile = tmpdir + "/total_count.txt"

	for k in kmer_k:
		echo("\t\t k = %d" %(k))
		countfile = tmpdir + "/" + str(k) + "mers.jf"
		kmerfile = tmpdir + "/" + str(k) + "mers.fa"

		os.system("jellyfish count -m %d -t 1 -s 100M -C --if=%s %s -o %s" %(k, kmerfile, readfile, countfile))
		os.system("jellyfish dump -c %s >> %s" %(countfile, tmpfile))

	infh = open(tmpfile, 'rb')
	outfh = open(outfile, 'wb')

	for line in infh:
		(mer, count) = line.rstrip().split()
		if(mer == reverse_complimentary(mer)):
			outfh.write("%s\t%d\n" %(mer, int(count)*2))
		else:
			outfh.write("%s\t%d\n" %(mer, int(count)))

	outfh.close()	
	infh.close()
	

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
	kmer_k = load_kmer(kmer, tmpdir)

	echo("Indexing and Querying Reads")
	index_query_reads(readfile, tmpdir, kmer_k, outfile)

	echo("Removing Temp Files")
	os.system("rm -rf %s" %(tmpdir))

	echo("Done")
	
	print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="jellyfish_dump_v2.py")
	parser.add_argument(dest="signature", type=str, help="list of kmers")
	parser.add_argument(dest="readfile", type=str, help="sequencing read file")
	parser.add_argument(dest="outfile", type=str, help="output file")
	parser.add_argument(dest="tmpdir", type=str, help="temporary directory")

	## doesn't work for mprof
	#parser.add_argument("-i", "--read", dest="readfile", type=str, help="sequencing read file", required = True)
	#parser.add_argument("-s", "--kmer", dest="kmer", type=str, help="list of kmers", required = True)
	#parser.add_argument("-t", "--tmpdir", dest="tmpdir", type=str, help="temporary directory", required = True)
	#parser.add_argument("-o", "--outfile", dest="outfile", type=str, help="output file", required = True)

	main(parser)	

