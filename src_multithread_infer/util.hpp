#pragma once
#include <cassert>
#include <thread>
#include <getopt.h>

class Parameters{
    public:
        size_t num_trees;
        size_t num_threads;
        size_t profile_batch_size;
        bool quiet;
        Parameters(){
            num_trees = 1;
            num_threads = 4;
            profile_batch_size = 1000000;
            quiet = false;
        };
};

void exit_with_usage();
int read_parameters(int argc, const char* argv[], Parameters &params);
double get_time_diff(std::chrono::time_point<std::chrono::system_clock> start);
