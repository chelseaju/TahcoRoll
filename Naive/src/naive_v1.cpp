#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <algorithm>
#include <unordered_map>
#include <set>
using namespace std;


void echo(const string msg){
		time_t now = time(0);
		struct tm *current = localtime(&now);
		printf("[%i-%i-%i %i:%i:%i] %s \n", (current->tm_year + 1900), (current->tm_mon + 1), current->tm_mday, current->tm_hour, current->tm_min, current->tm_sec, msg.c_str());
}

void upper(string &seq){
		for(int i = 0; i < seq.size(); i ++){
				seq[i] = toupper(seq[i]);
				if(!(seq[i] == 'A' || seq[i] == 'C' || seq[i] == 'G' || seq[i] == 'T'))
						seq[i] = 'N';
		}
}

void reverse_complement(string &seq){
		reverse(begin(seq), end(seq));
		for(int i = 0; i < seq.size(); i ++){
				switch (seq[i]){
						case 'A':
								seq[i] = 'T';
								break;
						case 'C':
								seq[i] = 'G';
								break;
						case 'G':
								seq[i] = 'C';
								break;
						case 'T':
								seq[i] = 'A';
								break;
						default:
								break;
				}
		}
}

/*
 * 	Load signature into a hash
 * 	Return a list of kmer sizes
 */

set<int> load_signatures(const string &signature_file, unordered_map <string, int> &signatures){

	set<int> krange;

	// read in signature
	ifstream infile(signature_file, ifstream::in);
	if(infile.is_open()){
		string line;
		while(getline(infile, line)){
			int s_size = line.size();
			krange.insert(s_size);

			signatures[line] = 0;
		}		
	}
	else{
		cerr << "Can't read signatures " << signature_file << endl;
		exit(-1);
	}
	infile.close();
	return krange;

}

/*
 *	Scan through each read with multiple window sizes
 *	Update the signature count if seen
 */
void count_signatures( unordered_map <string, int> &signatures, set<int> &krange, const string &readfile){

	// read in reads
	ifstream infile(readfile, ifstream::in);
	int line_counter = 0;
	int file_format = 4;	// default set it as fastq
	string line;
	if(infile.is_open()){
		getline(infile, line); // get the first line
		if(line[0] == '>')
			file_format = 2;	// set file format to be fasta
	
		line_counter++;

		while(getline(infile, line)){
			if(line_counter % file_format == 1){

				// scan through read with multiple k
				for(auto k:krange){
					for(int i = 0; i < line.length() - k + 1; i++){
						string substring = line.substr(i, k);
						upper(substring);

						// check forward
						if(signatures.find(substring) != signatures.end()){
							signatures[substring] += 1;
						}
	
						// check reverse complement
						reverse_complement(substring);
						if(signatures.find(substring) != signatures.end()){
							signatures[substring] += 1;
						}
					}
				}
			}
			line_counter ++;
		}
	}
	else{
		cerr << "Can't read file " << readfile << endl;
		exit(-1);
	}
	infile.close();
}

/*
 *	Export data to file
 */
void export_data(unordered_map <string, int> &signatures, const string &outfile){

	ofstream outfh;
	outfh.open(outfile, ios_base::out);	

	for(auto profile:signatures){
		outfh << profile.first << "\t" << profile.second << endl;
	}

	outfh.close();
}

int main(int argc, char* argv[]){

	if(argc < 4){
		cerr << "Usage: " << argv[0] << " SIGNATURE READFILE OUTFILE " << endl;
		return 1;
	}

	const char *signature_file = argv[1];
	const char *readfile = argv[2];
	const char *outfile = argv[3];

	unordered_map <string, int> signatures;

	echo("Loading Signatures");
	set<int> krange = load_signatures(signature_file, signatures);

	echo("Scanning Reads");
	count_signatures(signatures, krange, readfile);

	echo("Exporting Count");
	export_data(signatures, outfile);

}
