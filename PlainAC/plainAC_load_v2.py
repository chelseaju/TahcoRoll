"""
	Function: Plain Aho-Corasick implementation to count the kmer occurrences - C++ version
	To Run: python plainAC_load_v2.py signatures readfile outfile
        Author: Chelsea Ju
"""

import sys, re, os, argparse, datetime, random, time

PLAINACLOAD="bin/plainAC_load"


def echo(msg):
        print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))

def main(parser):
		option = parser.parse_args()
		signature = option.signatures

		start_time = time.time()

		## CMD: bin/plainAC_load signature
		os.system("%s %s" %(PLAINACLOAD, signature))

		print('Total runtime: %s seconds' %( time.time() - start_time))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="plainAC_load_v2.py")
	parser.add_argument(dest="signatures", type=str, help="selected kmers")

	## the following code does not work with certain installation of mprof 
#	parser.add_argument("-s", "--signatures", dest="signatures", required = True, type=str, help="selected kmers")
#	parser.add_argument("-i", "--reads", dest="readfile", required = True, type=str, help="read file")
#	parser.add_argument("-o", "--outfile", dest="outfile", required = True, type=str, help="output file")
	main(parser)
