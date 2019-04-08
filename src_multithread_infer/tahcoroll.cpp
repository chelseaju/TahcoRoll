#include <iostream>
#include <chrono>
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
    std::cerr << "Batch Profiling Size = " << params.profile_batch_size << std::endl;
    std::cerr << "Pattern File = " << pattern_file << std::endl;
    std::cerr << "Seq File = " << seq_file << std::endl;
    std::cerr << "Output File = " << result_file << std::endl;


	std::chrono::time_point<std::chrono::system_clock> basic_start;

    std::cerr << "Loading data with FileReader" << std::endl;
    FileReader fr(pattern_file);
    basic_start = std::chrono::system_clock::now();
    auto data = fr.read_data();
    std::cout << "Time: " << get_time_diff(basic_start) << "s" << std::endl;
    std::cout << data.size() << " patterns" << std::endl;

    basic_start = std::chrono::system_clock::now();
    Tahco model(&data);
	std::cout << "Loading Time: " << get_time_diff(basic_start) << "s" << std::endl;

    basic_start = std::chrono::system_clock::now();
    model.profile_patterns(seq_file, params);
    std::cout << "Profiling Time (incl. IO): " << get_time_diff(basic_start) << "s" << std::endl;
    
    model.output_results(result_file);

    return 0;
}
