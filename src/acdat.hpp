#pragma once
#include <vector>
#include <memory>
#include <string>
#include <algorithm>
#include "defs.hpp"

class ACDAT {
    private:
        std::vector<int> check;
        std::vector<int> base;
        std::vector<bool> used;
        int size;
        int alloc_size;
        int next_check_pos;
        int progress;
        
        struct Node {
            int ch;
            int depth;
            int left;
            int right;
            Node(int _ch, int _depth, int _left, int _right):
                ch(_ch), depth(_depth), left(_left), right(_right){};
        };
        typedef std::vector<Node> NodeVector;
            
        std::vector<NodeVector> siblings;


    public:
        void resize(int new_size);
        void build(StringVector &keys);
        int fetch(Node &parent, StringVector &keys);
        int insert(int depth, StringVector &keys);
        int exact_match(std::string text);
        ACDAT(): size(0), alloc_size(0){};
    
};

