"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	v1: separate kmer into different files based on their sizes, and use mkindex and search to query
	To Run:	
		python2.7 tallymer.py signature readfile outfile tmpdir
	Author: Chelsea Ju
	Date: 2017-12-30
"""		
import sys, re, os, argparse, datetime, time
#from memory_profiler import memory_usage
#from time import sleep


### change it to the absolute path of Tallymer source code
GT="/home/chelseaju/TahcoRoll/TahcoRoll/Tallymer/bin/gt"

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
			filename = tmpdir + "/" + "kmer_" + str(k) + ".fa"
			kmer_hash[k] = open(filename, "wb")
		
		kmer_hash[k].write(">1\n%s\n" %(line))	
	fh.close()

	for k in kmer_hash.keys():
		kmer_hash[k].close()

	return kmer_hash.keys()

"""
	Index kmer using KMC
"""
def index_kmers_reads(kmer_size, tmpdir, readfile):

	## construct suffix array
	#CMD: ./gt suffixerator -dna -pl -tis -suf -lcp -v -parts 4 -db readfile -indexname tmpdir/reads
	os.system("%s suffixerator -dna -pl -tis -suf -lcp -v -parts 4 -db %s -indexname %s/reads" %(GT, readfile, tmpdir)) 

	for k in kmer_size:
		kmer_index = tmpdir + "/" + "kmer_" + str(k)
		#CMD ./gt tallymer mkindex -mersize k -minocc 1 -indexname kmer_index -counts -pl -esa reads
		os.system("%s tallymer mkindex -mersize %s -minocc 1 -indexname %s -counts -pl -esa %s/reads" %(GT, str(k), kmer_index, tmpdir))

"""
	Query kmer and output results
"""
def query_kmers(kmer_size, tmpdir, outfile):
	for k in kmer_size:
		kmer_file = tmpdir + "/" + "kmer_" + str(k) + ".fa"
		kmer_index = tmpdir + "/" + "kmer_" + str(k)
		sample_kmer_file_tmp = tmpdir + "/" + "sample_kmer_" + str(k) +"_tmp" + ".txt"
		sample_kmer_file = tmpdir + "/" + "sample_kmer_" + str(k) + ".txt"

		#CMD: ./gt tallymer search -output sequence counts -strand fp -tyr kmer_index -q kmer_file > sample_kmer_file"
		os.system("%s tallymer search -output sequence counts -strand fp -tyr %s -q %s > %s" %(GT, kmer_index, kmer_file, sample_kmer_file_tmp))

		#CMD: awk '{a[$2] +=$1} END {for(i in a) print toupper(i)"\t"a[i]}' sample_kmer_file_tmp > sample_kmer_file 
		os.system("awk '{a[$2] += $1} END {for(i in a) print toupper(i)\"\\t\"a[i]}' %s > %s" %(sample_kmer_file_tmp, sample_kmer_file))

		## merging results
		os.system("cat %s >> %s " %(sample_kmer_file, outfile)) 


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
	parser = argparse.ArgumentParser(prog="tallymer.py")
#	parser.add_argument("-i", "--read", dest="readfile", type=str, help="sequencing read file", required = True)
#	parser.add_argument("-s", "--kmer", dest="kmer", type=str, help="list of kmers", required = True)
#	parser.add_argument("-o", "--outfile", dest="outfile", type=str, help="output filename", required = True)
#	parser.add_argument("-t", "--tmpdir", dest="tmpdir", type=str, help="temporary directory", required = True)


	parser.add_argument(dest="signature", type=str, help="list of kmers")
	parser.add_argument(dest="readfile", type=str, help="sequencing read file")
	parser.add_argument(dest="outfile", type=str, help="output filename")
	parser.add_argument(dest="tmpdir", type=str, help="temporary directory")

	main(parser)	

