#pragma once

#include <vector>
#include <memory>
#include <string>
#include "defs.hpp"

#define FILE_TYPE_FASTA 0
#define FILE_TYPE_FASTQ 1
#define FILE_TYPE_TXT   2

class FileReader {
    public:
        FileReader(const std::string &fp);
        StringVector read_data();
        StringVector read_fastq();
        StringVector read_fasta();
        StringVector read_txt();
        void check_type();
        void check_size();
    private:
        std::string file_path;
        char file_type;
};
