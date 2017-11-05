#pragma once
#include <cassert>

/*
typedef std::shared_ptr<std::string> String;
#define make_string(X) std::make_shared<std::string>(X)
*/

typedef std::string* String;
typedef std::vector<String> StringVector;
#define make_string(X) (new std::string(X))



inline char char2comp(char __ch){
    if(__ch == 'A' || __ch == 'a') return 'T';
    else if(__ch == 'C' || __ch == 'c') return 'G';
    else if(__ch == 'G' || __ch == 'g') return 'C';
    else if(__ch == 'T' || __ch == 't') return 'A';
    else{
        assert(false);
        return -1;
    }
}



inline int8_t char2binary(char __ch){
    if(__ch == 'A' || __ch == 'a') return 0;
    else if(__ch == 'C' || __ch == 'c') return 0;
    else if(__ch == 'G' || __ch == 'g') return 1;
    else if(__ch == 'T' || __ch == 't') return 1;
    else{
        assert(false);
        return -1;
    }
}


inline int64_t char2idx(char __ch){
    if(__ch == 'A' || __ch == 'a') return 1;
    else if(__ch == 'C' || __ch == 'c') return 2;
    else if(__ch == 'G' || __ch == 'g') return 3;
    else if(__ch == 'T' || __ch == 't') return 4;
    else{
        std::cerr << ">" << __ch << "<" << std::endl;
        assert(false);
    }
}
