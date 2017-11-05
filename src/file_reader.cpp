#include <iostream>
#include <fstream>
#include <algorithm>
#include <string>
#include <chrono>
#include <cstring>
#include <functional>
#include <vector>
#include <memory>
#include <cassert>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "file_reader.hpp"
#include <unistd.h>

#ifndef O_BINARY
    #define O_BINARY 0
#endif

FileReader::FileReader(const std::string &fp): file_path(fp) {
    check_type();
    check_size();
};

void FileReader::check_type(){
    std::ifstream f_in(file_path);
    std::string line;
    assert(std::getline(f_in, line));
    f_in.close();
    switch(line[0]){
        case '@':
            file_type = FILE_TYPE_FASTQ;
            break;
        case '>':
            file_type = FILE_TYPE_FASTA;
            break;
        default:
            file_type = FILE_TYPE_TXT;
            break;
    }
}

void FileReader::check_size(){
    std::ifstream f_in(file_path, std::ifstream::binary);
    if(f_in){
        f_in.seekg (0, f_in.end);
    }else{
        std::cerr << "Cannot open " << file_path << std::endl;
        exit(0);
    }
}


StringVector FileReader::read_fastq(){
    auto ptr = StringVector();
    std::cerr << "FASTQ is not available yet" << std::endl;
    exit(0);
    return ptr;
}

StringVector FileReader::read_fasta(){
    auto ptr = StringVector();
    std::cerr << "FASTA is not available yet" << std::endl;
    exit(0);
    return ptr;
}

StringVector FileReader::read_txt(){
    auto vec = StringVector();

    const auto BUFFER_SIZE = 64 * 1024;

    auto fd = ::open(file_path.c_str(), O_RDONLY);
    if(fd == -1){
        std::cerr << "Cannot open " << file_path << std::endl;
        exit(0);
    }

    char buf[BUFFER_SIZE + 1];
    auto cur = make_string();

    while(auto bytes_read = ::read(fd, buf, BUFFER_SIZE)) {
        if(bytes_read < -1){
            std::cerr << "Failed while reading " << file_path << std::endl;
            exit(0);
        }else if(!bytes_read){
            break;
        }
        char* st = buf;
        for(char *p = buf; (p = static_cast<char*>(std::memchr(p, '\n', static_cast<size_t>((buf + bytes_read) - p)))); ++p){
            *p = '\0';
            cur->append(st);
            vec.emplace_back(cur);
            cur = make_string();
            st = p + 1;
        }
        cur->append(st, static_cast<size_t>((buf + bytes_read) - st));
    }
    if(cur->size() > 0){
        vec.emplace_back(cur);
    }
    return vec;
}

StringVector FileReader::read_data(){
    if(file_type == FILE_TYPE_FASTA){
        return read_fasta();
    }else if(file_type == FILE_TYPE_FASTQ){
        return read_fastq();
    }else{
        return read_txt();
    }
}
