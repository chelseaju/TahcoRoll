#include "util.hpp"
#include <unistd.h>
#include <getopt.h>

void exit_with_usage(){
    Parameters p;
	printf(
	"Usage: tahcoroll [options] pattern_file seq_file [output_file=seq_file.results]\n"
	"options:\n"
    "  -t number of trees (default %zu)\n"
	"  -s number of threads (default %zu)\n"
    "  -b batch size for profiling (default %zu)\n"
    "  -q quiet mode\n"
    , p.num_trees, p.num_threads, p.profile_batch_size
	);
    exit(1);
}


int read_parameters(const int argc, const char* argv[], Parameters &params){
    int opt;
    while( (opt = getopt(argc, (char**) argv, "t:s:q")) != -1 ){
		switch(opt) {
			case 't':
				params.num_trees = static_cast<size_t>(atoi(optarg));
				break;
            case 's':
                params.num_threads = static_cast<size_t>(atoi(optarg));
                break;
            case 'b':
                params.profile_batch_size = static_cast<size_t>(atoi(optarg));
                break;
            case 'q':
                params.quiet = true;
                break;
            case '?':
                exit_with_usage();
                break;
			default:
                exit_with_usage();
                break;
        }

    }
    return optind;
}

double get_time_diff(std::chrono::time_point<std::chrono::system_clock> start) {
    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> diff = end - start;
    return diff.count();
}
