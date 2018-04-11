#include <iostream>
#include <cstdint>
#include <fstream>
#include <cstdlib>
#include <cstdio>
#include "file_reader.hpp"
#include "tahco.hpp"

#include <vector>
#include <string>

int main(int argc, const char **argv){
    if(argc < 1 + 2){
        std::cerr << "--usage " << argv[0] << " pattern_file seq_file [num_trees=1] [output_file=seq_file.results]" << std::endl;
        exit(0);
    }
    
    size_t num_trees = 1;
    if(argc > 1 + 2){
        num_trees = static_cast<size_t>(atoi(argv[3]));
    }


	clock_t basic_start;

    std::cerr << "Loading data with FileReader" << std::endl;
	basic_start = clock();
    FileReader fr(argv[1]);
    auto data = fr.read_data();
    std::cout << "Time: " << static_cast<double>(clock() - basic_start) / CLOCKS_PER_SEC << "s" << std::endl;
    std::cout << data.size() << " patterns" << std::endl;

    Tahco model(&data, num_trees);
	std::cout << "Loading Time: " << static_cast<double>(clock() - basic_start) / CLOCKS_PER_SEC << "s" << std::endl;

	basic_start = clock();
    // model.verify_tree_building();
    model.profile_patterns(argv[2]);
    std::cout << "Profiling Time: " << static_cast<double>(clock() - basic_start) / CLOCKS_PER_SEC << "s" << std::endl;
    

    if(argc > 1 + 3){
        model.output_results(argv[4]);
    }else{
        model.output_results(std::string(argv[2]) + ".results");
    }


    return 0;
}
