#include <iostream>
#include <cstdint>
#include <fstream>
#include <cstdlib>
#include <cstdio>
#include "file_reader.hpp"
#include "tahco.hpp"
#include "util.hpp"

#include <vector>
#include <string>

int main(int argc, const char **argv){
    if(argc < 1 + 2){
        exit_with_usage();
        exit(0);
    }
    
    Parameters params;
    int arg_idx = read_parameters(argc, argv, params);

    assert(arg_idx < argc);
    const char* pattern_file = argv[arg_idx++];
    assert(pattern_file != NULL);

    assert(arg_idx < argc);
    const char* seq_file = argv[arg_idx++];
    assert(seq_file != NULL);

    std::string result_file = std::string(seq_file) + ".results";
    if(arg_idx != argc){
        result_file = std::string(argv[arg_idx]);
    }

    std::cerr << "Num of Trees = " << params.num_trees << std::endl;
    std::cerr << "Num of Threads = " << params.num_threads << std::endl;
    std::cerr << "Pattern File = " << pattern_file << std::endl;
    std::cerr << "Seq File = " << seq_file << std::endl;
    std::cerr << "Output File = " << result_file << std::endl;



	clock_t basic_start;

    std::cerr << "Loading data with FileReader" << std::endl;
	basic_start = clock();
    FileReader fr(pattern_file);
    auto data = fr.read_data();
    std::cout << "Time: " << static_cast<double>(clock() - basic_start) / CLOCKS_PER_SEC << "s" << std::endl;
    std::cout << data.size() << " patterns" << std::endl;

    Tahco model(&data, params);
	std::cout << "Loading Time: " << static_cast<double>(clock() - basic_start) / CLOCKS_PER_SEC << "s" << std::endl;

	basic_start = clock();
    model.profile_patterns(seq_file, params);
    std::cout << "Profiling Time: " << static_cast<double>(clock() - basic_start) / CLOCKS_PER_SEC << "s" << std::endl;

    model.output_results(result_file);


    return 0;
}
