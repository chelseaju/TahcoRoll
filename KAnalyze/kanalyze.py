"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	v2: separate kmer into different files, and use --kmerfilter to count their frequency
	To Run:	
		python kanalyze_v2.py signature readfile outfile tmpdir
	Author: Chelsea Ju
	Date: 2017-07-05
	Last Modify: 2017-12-30
"""		
import sys, re, os, argparse, datetime, time

## need absolute path
KA="bin/kanalyze.jar"

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
            kmer_hash[k] = open(tmpdir + "/" + str(k) + "mers.txt", 'wb')

        kmer_hash[k].write("%s\n" %(line))
    fh.close()

    for v in kmer_hash.values():
        v.close()

    return kmer_hash.keys()

"""
	Index and Query kmers
"""
def index_query_kmers_reads(kmer_hash, tmpdir, readfile, outfile):

	outfh = open(outfile, 'wb')

	for k in kmer_hash:

		kmer_file = tmpdir + "/" + str(k) + "mers.txt"
		kmer_out = tmpdir + "/" + str(k) + "mers.kc"

		echo("Indexing %smers" %(str(k)))
#		## CMD: ./bin/count -d 1 -f fastq -k k -l 1 -o tmpdir/kmer.kc -rcanonical --kmerfilter kmerfile:kmer_file -t 1 readfile
#		os.system("%s -d 1 -f fastq -k %d -l 1 -o %s -rcanonical --kmerfilter kmerfile:%s -t 1 %s" %(KA, k, kmer_out, kmer_file, readfile))

		## CMD: java -jar -Xmx20G ./bin/kanalyze.jar count -d 1 -f fastq -k k -l 1 -o tmpdir/kmer.kc -rcanonical --kmerfilter kmerfile:kmer_file -t 1 readfile
		os.system("java -jar -Xmx20G %s count -d 1 -f fastq -k %d -l 1 -o %s -rcanonical --kmerfilter kmerfile:%s -t 1 %s" %(KA, k, kmer_out, kmer_file, readfile))

		echo("Exporting")
		fh = open(kmer_out, 'rb')
		for line in fh:
			(mer, count) = line.rstrip().split()
			if(mer == reverse_complimentary(mer)):
				outfh.write("%s\t%d\n" %(mer, int(count)*2))
			else:
				outfh.write("%s\t%d\n" %(mer, int(count)))
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
	kmer_size = load_kmer(kmer, tmpdir)

	echo("Indexing Kmers and Reads")
	index_query_kmers_reads(kmer_size, tmpdir, readfile, outfile)

	echo("Removing Temp Files")
	os.system("rm -rf %s" %(tmpdir))	

	echo("Done")	

	print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="kanalyze_v2.py")

	parser.add_argument(dest="signature", type=str, help="list of kmers")
	parser.add_argument(dest="readfile", type=str, help="sequencing read file")
	parser.add_argument(dest="outfile", type=str, help="output filename")
	parser.add_argument(dest="tmpdir", type=str, help="temporary directory")


	#parser.add_argument("-i", "--read", dest="readfile", type=str, help="sequencing read file", required = True)
	#parser.add_argument("-s", "--kmer", dest="kmer", type=str, help="list of kmers", required = True)
	#parser.add_argument("-o", "--outfile", dest="outfile", type=str, help="output filename", required = True)
	#parser.add_argument("-t", "--tmpdir", dest="tmpdir", type=str, help="temporary directory", required = True)

	main(parser)	

