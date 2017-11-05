#pragma once
#include <map>
#include <utility>
#include <vector>
#include <string>


class AC{
    public:
        AC(): num_patterns(0), root(new Node){};

        void add_pattern(const std::string &p, int v);
        void construct();
    
        std::vector<MatchPair> query(const std::string &text);
        int get_num_patterns();

    private:
        int num_patterns;
        Node *root;
};
