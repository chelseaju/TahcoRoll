"""
	Function: Naive implementation to count the ground truth of kmer occurrences
	To Run: python naive_v1.py
		-s --signatures selected_kmers
		-i --reads read_file
		-o --outfile output_file 
        Author: Chelsea Ju
"""

import sys, re, os, argparse, datetime, random, time
#from memory_profiler import memory_usage
#from time import sleep
SIGNATURE = {}

def echo(msg):
        print "[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(msg))

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

def load_signature(signature):
	ksize = set()
	fh = open(signature, 'rb')
	for line in fh:
		seq = line.rstrip()
		rev_seq = reverse_complimentary(seq)
		ksize.add(len(seq))
		
		if(seq <= rev_seq):
			SIGNATURE[seq] = 0
		else:
			SIGNATURE[rev_seq] = 0
	fh.close()

	return ksize

def get_read_type(readfile):
	fh = open(readfile, 'rb')
	line = fh.readline()
	fh.close()
	if(line[0] == ">"):
		return 2
	elif(line[0] == "@"):
		return 4


def count_signature(krange, readfile):
	read_type = get_read_type(readfile)

	line_count = 0
	fh = open(readfile, 'rb')
	for line in fh:
		if(line_count % read_type == 1):
			if(line_count % 100000 == 0):
				echo("\tProcess %d" %(line_count))
			seq = line.rstrip()
			rev_seq = reverse_complimentary(seq)
	
			## iterate through different k
			for k in krange:
				for i in xrange(len(seq)-k+1):
					subseq = seq[i:i+k]
					rev_subseq = rev_seq[i:i+k]

					if(SIGNATURE.has_key(subseq)):
						SIGNATURE[subseq] += 1
				
					if(SIGNATURE.has_key(rev_subseq)):
						SIGNATURE[rev_subseq] += 1
		line_count += 1
	fh.close()

def export_signature(outfile):
	fh = open(outfile, 'wb')
	for kmer in SIGNATURE.keys():
		fh.write("%s\t%d\n" %(kmer, SIGNATURE[kmer]))
	fh.close()

def main(parser):
        option = parser.parse_args()
	signature = option.signatures
	readfile = option.readfile
	outfile = option.outfile

	start_time = time.time()
	echo("Loading Signatures")
	krange = load_signature(signature)


	echo("Scanning Reads")
	count_signature(krange, readfile)

	echo("Exporting Kmer Occurrence")
	export_signature(outfile)
        echo("Done")

	print('Total runtime: %s seconds' %( time.time() - start_time))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="naive_v1.py")
	parser.add_argument("-s", "--signatures", dest="signatures", required = True, type=str, help="selected kmers")
	parser.add_argument("-i", "--reads", dest="readfile", required = True, type=str, help="read file")
	parser.add_argument("-o", "--outfile", dest="outfile", required = True, type=str, help="output file")
	main(parser)
