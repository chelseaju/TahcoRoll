#include "acdat.hpp"

#include <iostream>

void ACDAT::resize(int new_size){
    // printf("resize %d!!\n", new_size);
    if(new_size > alloc_size){
        check.resize(new_size);
        base.resize(new_size);
        used.resize(new_size);
        alloc_size = new_size;
    }
}

void ACDAT::build(StringVector &keys){


    progress = 0;
    Node root(-1, 0, 0, static_cast<int>(keys.size()));

    //resize(64);
    resize(65536);

    base[0] = 1;
    next_check_pos = 0;

    fetch(root, keys);
    insert(0, keys);
}


int ACDAT::fetch(Node &parent, StringVector &keys){
    if(static_cast<int>(siblings.size()) <= parent.depth){
        siblings.push_back(NodeVector());
    }else{
        siblings[parent.depth].clear();
    }

    printf("(ch, dp, L, R) = %d %d %d %d\n", parent.ch, parent.depth, parent.left, parent.right);

    int prev = 0, L;
    for(int i = parent.left; i < parent.right; ++i){
        // std::cerr << i << " " << *keys[i] << std::endl;; 
        L = static_cast<int>(keys[i]->length());
        if(L < parent.depth){
            continue;
        }
        int cur = 0;
        if(L != parent.depth){
            cur = CHAR2IDX(keys[i]->at(parent.depth));
        }
        if(prev > cur){
            return 0;
        }

        L = static_cast<int>(siblings[parent.depth].size());
        if(cur != prev || L == 0){
            if(L > 0){
                siblings[parent.depth][L - 1].right = i;
            }
            siblings[parent.depth].push_back(Node(cur, parent.depth + 1, i, -1));
        }
        prev = cur;
    }

    L = static_cast<int>(siblings[parent.depth].size());
    if(L > 0){
        siblings[parent.depth][L - 1]. right = parent.right;
    }

    return static_cast<int>(siblings[parent.depth].size());
}



int ACDAT::insert(int depth, StringVector &keys){
    double key_size = static_cast<double>(keys.size());
    assert(depth < siblings.size());
    int siblings_size = static_cast<int>(siblings[depth].size());
    int begin = 0;
    int pos = next_check_pos;
    if(siblings[depth][0].ch >= pos){
        pos = siblings[depth][0].ch;        
    }
        
    int nz_sum = 0;
    bool first = true;
    
    bool flag = true;
    while(flag){
        ++pos;
        if(alloc_size <= pos){
            resize(2 * alloc_size);
        }

        if(check[pos] != 0){
            ++nz_sum;
            continue;
        }else if(first){
            next_check_pos = pos;
            first = false;
        }
        begin = pos - siblings[depth][0].ch;
        if(alloc_size < begin + 4){
            resize(2 * alloc_size);
        }
        if(used[begin]){
            continue;
        }
        flag = false;
        for(int i = 1; i < siblings_size; ++i){
            if(alloc_size < begin + siblings[depth][i].ch && check[begin + siblings[depth][i].ch] != 0){
                flag = true;
                break;
            }
        }
    }
    

    if(1.0 * nz_sum >= 0.95 * (pos - next_check_pos + 1)){
        next_check_pos = pos;
    }

    used[begin] = true;
    
    for(int i = 0; i < siblings_size; ++i){
        assert(begin + siblings[depth][i].ch < alloc_size);
        check[begin + siblings[depth][i].ch] = begin;
    }

    for(int i = 0;i < siblings_size; ++i){
        if(fetch(siblings[depth][i], keys) == 0){
            // printf("OAQ!!\n");
            base[begin + siblings[depth][i].ch] = -siblings[depth][i].left - 1;
            ++progress;
        }else{
            assert(siblings_size == siblings[depth].size());
            // printf("keep inserting\n");
            assert(begin + siblings[depth][i].ch > 0);
            base[begin + siblings[depth][i].ch] = insert(depth + 1, keys);
        }
    }

    return begin;
}

int ACDAT::exact_match(std::string text){
    int len = static_cast<int>(text.length());
    int result = -1;
    int b = base[0], p;

    for(int i = 0; i < len; ++i){
        p = b + CHAR2IDX(text[i]);
        if(b == check[p]){
            b = base[p];
        }else{
            printf("!!\n");
            return -1;
        }
    }
    p = b;
    int now = base[p];
    if(b == check[p] && now < 0){
        result = -now - 1;
    }
    return result;
}
