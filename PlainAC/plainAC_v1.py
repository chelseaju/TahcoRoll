"""
	Function: Compute the kmer count using aho-corasick - python implementation
	To Run: python plainAC_v1.py signatures readfile outfile
	Author: Chelsea Ju
"""

import sys, re, os, argparse, datetime, random, time
import ahocorasick
#from memory_profiler import memory_usage
#from time import sleep

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


def build_automaton(sigmer_file):
	
	A = ahocorasick.Automaton()

	fh = open(sigmer_file, 'r')
	for line in fh:
		seq = line.rstrip()
		A.add_word(seq, len(seq), 0)
	
	fh.close()

	A.make_automaton()
	return A

def get_format(read_file):
	fh = open(read_file, 'rb')
	line = fh.readline()
	fh.close()
	if(line[0] == ">"):
		return 2
	elif(line[0] == "@"):
		return 4


def count_reads(ahc, read_file):

	profile = {}

	fastq = get_format(read_file)

	fh = open(read_file, 'rb')
	line_count = 0
	for line in fh:
		if(line_count % fastq == 1):	
			line = line.rstrip()
			for (end_pos, key_size) in ahc.iter(line):
				key_str = line[(end_pos - key_size + 1):end_pos+1]
				if(profile.has_key(key_str)):
					profile[key_str] += 1
				else:
					profile[key_str] = 1		

			rc_line = reverse_complimentary(line)
			for (end_pos, key_size) in ahc.iter(rc_line):
				key_str = rc_line[(end_pos - key_size + 1):end_pos+1]

				if(profile.has_key(key_str)):
					profile[key_str] += 1
				else:
					profile[key_str] = 1

		line_count += 1
	fh.close()
	return profile

def export_profile(profile, outfile):
	fh = open(outfile, 'wb')
	for k in profile.keys():
		fh.write("%s\t%d\n" %(k, profile[k]))
	fh.close()

def main(parser):
        option = parser.parse_args()
        sigmer_file = option.signature
        read_file = option.readfile
        outfile = option.outfile

	start_time = time.time()
	echo("Loading Sigmers")
	ahc = build_automaton(sigmer_file)

	echo("Counting Reads")
	profile = count_reads(ahc, read_file)	

	echo("Exporting Results")
	export_profile(profile, outfile)

	echo("Done")
        print('Total runtime: %s seconds' %(time.time() - start_time))

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(prog="plainAC_v1.py")
	parser.add_argument(dest = "signature", type=str, help="list of kmers")
	parser.add_argument(dest = "readfile", type=str, help="read data in fastq or fasta")
	parser.add_argument(dest = "outfile", type=str, help="output filename")
	main(parser)
#	mem_usage = memory_usage((main, (parser,)))
#       print('Maximum memory usage: %s' % max(mem_usage))





