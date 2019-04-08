#pragma once
#include <iostream>
#include <chrono>
#include <fstream>
#include <algorithm>
#include <vector>
#include <queue>
#include <string>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <memory>
#include <string>
#include <unordered_map>
#include <map>
#include <mutex>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include "defs.hpp"
#include "util.hpp"

// typedef std::unordered_multimap<int64_t, size_t> Hashmap;
// typedef std::unordered_map<int64_t, std::vector<size_t> > Hashmap;
// typedef std::map<int64_t, std::vector<size_t> > Hashmap;
typedef std::unordered_map<int64_t, size_t> Hashmap;
//typedef std::map<int64_t, size_t> Hashmap;

//#define MOD 36028797018963913LL
//#define MOD 461168601ULL
#define MOD 2147483647LL

class Node{
    public:
        size_t fail;
        size_t next[2];
        size_t depth;
        void reset(size_t _depth);
        Hashmap *hashmap;
};



class Tahco{
    private:
        StringVector* patterns_ptr;
        size_t num_patterns;
        size_t max_len;
        size_t min_len;
        size_t max_text_len;
        std::vector<uint32_t> pattern_cnt;
        std::vector<int64_t> hash_base;
        size_t num_nodes;
        std::vector<Node> nodes;
        std::mutex* mtx;

    public:
        Tahco(StringVector* _patterns_ptr);
        void initialize();
        void profile_patterns(const std::string &fp, const Parameters &params);
        void profile_patterns_in_pool(std::vector<std::string> &pool);
        double profile_patterns_with_tahco(const std::string &fp, const Parameters &params);
        void output_results(const std::string &fp);


        // AC methods
        size_t get_next(size_t now, int8_t c);
        size_t estimate_node_num(size_t L, size_t R, size_t step);
        void add_pattern(std::string &pattern, size_t pattern_idx);
        void build_tahco();
        void match(std::string &text, std::vector<int64_t> &hash, std::vector<int64_t> &hashr);
        inline int64_t compute_range_hash(std::vector<int64_t> &hash, size_t L, size_t R);

};

