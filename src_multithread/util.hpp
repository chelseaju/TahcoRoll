#pragma once
#include <cassert>
#include <thread>
#include <getopt.h>

class Parameters{
    public:
        size_t num_trees;
        size_t num_threads;
        bool quiet;
        Parameters(){
            num_trees = 1;
            num_threads = 4;
            quiet = false;
        };
};

void exit_with_usage();
int read_parameters(int argc, const char* argv[], Parameters &params);
