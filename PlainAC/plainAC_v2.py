"""
	Function: Plain Aho-Corasick implementation to count the kmer occurrences - C++ version
	To Run: python plainAC_v2.py signatures readfile outfile
        Author: Chelsea Ju
"""

import sys, re, os, argparse, datetime, random, time

PLAINAC="bin/plainAC"


def echo(msg):
        print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))

def main(parser):
		option = parser.parse_args()
		signature = option.signatures
		readfile = option.readfile
		outfile = option.outfile

		start_time = time.time()

		## CMD: bin/plainAC signature readfile outfile
		os.system("%s %s %s %s" %(PLAINAC, signature, readfile, outfile))

		print('Total runtime: %s seconds' %( time.time() - start_time))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="plainAC_v2.py")
	parser.add_argument(dest="signatures", type=str, help="selected kmers")
	parser.add_argument(dest="readfile", type=str, help="read file")
	parser.add_argument(dest="outfile", type=str, help="output file")

	## the following code does not work with certain installation of mprof 
#	parser.add_argument("-s", "--signatures", dest="signatures", required = True, type=str, help="selected kmers")
#	parser.add_argument("-i", "--reads", dest="readfile", required = True, type=str, help="read file")
#	parser.add_argument("-o", "--outfile", dest="outfile", required = True, type=str, help="output file")
	main(parser)
