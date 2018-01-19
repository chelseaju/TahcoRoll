"""
	Function: Given a read file, and a list of kmer, return the kmer frequency 
	To Run:	
		python msbwt.py signatures readfile outfile tmpdir  
	Author: Chelsea Ju
	Date: 2017-12-31

"""		
import sys, os, argparse, datetime, time
MSBWT="bin/msbwt"

def echo(msg):
        print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))

def main(parser):
	option = parser.parse_args()
	readfile = option.readfile
	kmer = option.signature
	tmpdir = option.tmpdir
	outfile = option.outfile

	start_time = time.time()

	echo("Indexing Reads")
	if not os.path.exists(tmpdir):
   		os.makedirs(tmpdir)

	## for short reads
	## CMD: bin/msbwt cffq --uniform --compressed -p 1 tmpdir readfile
	## for long reads 
	## CMD: bin/msbwt cffq -p 1 tmpdir readfile 
	os.system("%s cffq --uniform --compressed -p 1 %s %s" %(MSBWT, tmpdir, readfile))

	echo("Querying Kmers")
	tmpfile = tmpdir + "/outfile.txt"
	
	## CMD: bin/msbwt massquery --rev-comp tmpdir signature tmpfile
	os.system("%s massquery --rev-comp %s %s %s" %(MSBWT, tmpdir, kmer, tmpfile))
	os.system("awk -F',' '{print $1\"\\t\"$2+$3}' %s > %s" %(tmpfile, outfile))
	
	echo("Cleaning")
	os.system("rm -rf %s" %(tmpdir))

	echo("Done")
	print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="msbwt.py")
	parser.add_argument("signature", type=str, help="list of kmers")
	parser.add_argument("readfile", type=str, help="sequencing read file")
	parser.add_argument("outfile", type=str, help="output file")
	parser.add_argument("tmpdir", type=str, help="temporary directory")

#	parser.add_argument("-i", "--read", dest="readfile", type=str, help="sequencing read file", required = True)
#	parser.add_argument("-s", "--kmer", dest="kmer", type=str, help="list of kmers", required = True)
#	parser.add_argument("-t", "--tmpdir", dest="tmpdir", type=str, help="temporary directory", required = True)
#	parser.add_argument("-o", "--outfile", dest="outfile", type=str, help="outfile", required = True)
  	main(parser)	

