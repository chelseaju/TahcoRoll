#include "tahco.hpp"


size_t Tahco::get_next(size_t now, int8_t c){
   if(nodes[now].next[c] == 0){
       if(num_nodes == nodes.size()){
           nodes.emplace_back(Node());
       }
       nodes[num_nodes].reset(nodes[now].depth + 1);
       nodes[now].next[c] = num_nodes++;
   }
   return nodes[now].next[c];
}


Tahco::Tahco(StringVector* _patterns_ptr){
    patterns_ptr = _patterns_ptr;
    num_nodes = 0;
    mtx = new std::mutex();
    initialize();
}


void Node::reset(size_t _depth){
    depth = _depth;
    fail = 0;
    next[0] = 0;
    next[1] = 0;
    if(hashmap != NULL){
        delete hashmap;
    }
    hashmap = NULL;
}


void Tahco::initialize(){
    // Patterns
    StringVector &patterns = (*patterns_ptr);
    num_patterns = patterns.size();
    max_len = 0;
    for(size_t i = 0; i < num_patterns; ++i){
        max_len = std::max(max_len, patterns[i]->length());
    }
    
    // allocate pattern_cnt buffers
    pattern_cnt.resize(num_patterns);
    
    // precompute hase bases
    hash_base.resize(max_len + 2);
    hash_base[0] = 1LL;
    for(size_t i = 1; i <= max_len + 1; ++i){
        hash_base[i] = hash_base[i - 1] * 5;
        if(hash_base[i] >= MOD){
            hash_base[i] %= MOD;
        }
    }

}

size_t Tahco::estimate_node_num(size_t L, size_t R, size_t step){
    if(L == R){
        return 0;
    }
    StringVector &patterns = (*patterns_ptr);
    size_t st = L;
    size_t total = 0;
    while(st < R && step >= patterns[st]->length()){
        ++st;
    }
    if(st >= R){
        return 0;
    }

    int8_t cur_bit = char2binary(patterns[st]->at(step));
    for(size_t ed = st + 1; st < R && step < patterns[st]->length(); ed = st + 1){
        while(ed < R && step < patterns[ed]->length() && cur_bit == char2binary(patterns[ed]->at(step))){
            ++ed;
        }
        
        total += estimate_node_num(st, ed, step + 1) + 1;
        st = ed;
        while(st < R && step >= patterns[st]->length()){
            ++st;
        }
    }

    return total;
}


void Tahco::profile_patterns(const std::string &fp, const Parameters &params){
    StringVector &patterns = (*patterns_ptr);

    size_t num_patterns_per_tree = (num_patterns + params.num_trees - 1) / params.num_trees;

	double time_construction = 0.0;
	double time_query = 0.0;
    for(size_t iter = 0; iter < params.num_trees; ++iter){
        std::cerr << "Tree " << iter << std::endl;
        auto st = iter * num_patterns_per_tree;
        auto ed = std::min(st + num_patterns_per_tree, num_patterns);

        // construct a trie        
        size_t estimated_node_num = estimate_node_num(st, ed, 0);
        std::cerr << estimated_node_num << " estimated nodes." << std::endl;
        nodes.reserve(estimated_node_num + 2);
        std::cerr << "reserved memory" << std::endl;
        while(nodes.size() < 2){
            nodes.emplace_back(Node());
        }
        nodes[1].reset(0);
        num_nodes = 2;

        auto basic_start = std::chrono::system_clock::now();
        // add patterns
        max_len = 0;
        min_len = SIZE_MAX;
        for(auto i = st; i < ed; ++i){
            add_pattern(*patterns[i], i);
            max_len = std::max(max_len, patterns[i]->length());
            min_len = std::min(min_len, patterns[i]->length());
        }
        std::cerr << "Added patterns." << std::endl;

        // build tahco
        build_tahco();
		time_construction += get_time_diff(basic_start);
        std::cerr << "Built tacho." << std::endl;
        
        time_query += profile_patterns_with_tahco(fp, params);

        for(size_t i = 0; i < num_nodes; ++i){
            nodes[i].reset(0);
        }
    }

	std::cerr << "Total construction time: " << time_construction << std::endl;
	std::cerr << "Total query time: " << time_query << std::endl;

}


void Tahco::profile_patterns_in_pool(std::vector<std::string> &pool){
    std::vector<int64_t> hash;
    std::vector<int64_t> hashr;
    for(auto& cur : pool) {
        match(cur, hash, hashr);
    }
}


double Tahco::profile_patterns_with_tahco(const std::string &fp, const Parameters& params){

    const auto BUFFER_SIZE = 6400 * 1024;

    auto fd = ::open(fp.c_str(), O_RDONLY);
    if(fd == -1){
        std::cerr << "Cannot open " << fp << std::endl;
        exit(0);
    }

    char buf[BUFFER_SIZE + 1];
    auto cur = std::string("");
    int line_no = 0;

    std::vector<int64_t> hash;
    std::vector<int64_t> hashr;

    double total_time = 0.0;
    size_t pool_size = 0;
    size_t cur_candidate_thread = 0;
    std::vector<std::string> pool[params.num_threads];

    while(auto bytes_read = ::read(fd, buf, BUFFER_SIZE)) {
        if(bytes_read < -1){
            std::cerr << "Failed while reading " << fp << std::endl;
            exit(0);
        }else if(!bytes_read){
            break;
        }
        char* st = buf;
        for(char *p = buf; (p = static_cast<char*>(std::memchr(p, '\n', static_cast<size_t>((buf + bytes_read) - p)))); ++p){            
            *p = '\0';
            if(line_no == 1){
                /*
                cur += st;
                start_time = clock();
                match(cur, hash, hashr);
                total_time += static_cast<double>(clock() - start_time);
                cur.clear();
                */
                cur += st;
                pool[cur_candidate_thread++].emplace_back(cur);
                ++pool_size;
                if(cur_candidate_thread == params.num_threads) {
                    cur_candidate_thread = 0;
                }
                cur.clear();
                
                if(pool_size == params.profile_batch_size) {
                    ThreadVector threads;
                    auto basic_start = std::chrono::system_clock::now();
                    for(size_t thread_i = 0; thread_i < params.num_threads; ++thread_i) {
                        threads.emplace_back(std::thread(&Tahco::profile_patterns_in_pool, this, std::ref(pool[thread_i])));
                    }
                    for(auto& th : threads) {
                        th.join();
                    }
                    total_time += get_time_diff(basic_start);
                    for(size_t thread_i = 0; thread_i < params.num_threads; ++thread_i) {
                        pool[thread_i].clear();
                    }
                    pool_size = 0;
                }
            }
            st = p + 1;
            ++line_no;
            if(line_no == 4){
                line_no = 0;
            }
        }
        if(line_no == 1){
            cur.append(st, static_cast<size_t>((buf + bytes_read) - st));
        }
    }

    if(pool_size > 0) {
        ThreadVector threads;
        auto basic_start = std::chrono::system_clock::now();
        for(size_t thread_i = 0; thread_i < params.num_threads; ++thread_i) {
            threads.emplace_back(std::thread(&Tahco::profile_patterns_in_pool, this, std::ref(pool[thread_i])));
        }
        for(auto& th : threads) {
            th.join();
        }
        total_time += get_time_diff(basic_start);
        for(size_t thread_i = 0; thread_i < params.num_threads; ++thread_i) {
            pool[thread_i].clear();
        }
        pool_size = 0;
    }
    return total_time;
}


void Tahco::add_pattern(std::string &pattern, size_t pattern_idx){
    
    size_t cur_node = 1;
    int64_t cur_hash = 0;
    for(auto it = pattern.begin(); it != pattern.end(); ++it){
        cur_hash = cur_hash * 5 + char2idx(*it);
        if(cur_hash >= MOD){
            cur_hash %= MOD;
        }
        cur_node = get_next(cur_node, char2binary(*it));
    }
    if(nodes[cur_node].hashmap == NULL){
        nodes[cur_node].hashmap = new Hashmap();
    }

    assert(nodes[cur_node].hashmap->count(cur_hash) == 0);
    (*nodes[cur_node].hashmap)[cur_hash] = pattern_idx;
}


void Tahco::build_tahco(){
    std::queue<size_t> q;
    size_t cur, p;

    q.push(1);
    while(!q.empty()){
        cur = q.front();
        q.pop();
        // 0
        if(nodes[cur].next[0] > 0){
            for(p = nodes[cur].fail; p > 0 && nodes[p].next[0] == 0; p = nodes[p].fail);
            nodes[nodes[cur].next[0]].fail = (p)?(nodes[p].next[0]):(1);
            q.push(nodes[cur].next[0]);
        }
        // 1
        if(nodes[cur].next[1] > 0){
            for(p = nodes[cur].fail; p > 0 && nodes[p].next[1] == 0; p = nodes[p].fail);
            nodes[nodes[cur].next[1]].fail = (p)?(nodes[p].next[1]):(1);
            q.push(nodes[cur].next[1]);
        }
    }
}

#define LB 100000000
inline int64_t MUL(int64_t a, int64_t b){
    int64_t a_u = a / LB;
    int64_t a_l = a % LB;
    int64_t b_u = b / LB;
    int64_t b_l = b % LB;
    int64_t res = (a_l * b_l) % MOD;
    res = (res + ((((a_u * b_l) % MOD) * LB) % MOD)) % MOD;
    res = (res + ((((b_u * a_l) % MOD) * LB) % MOD)) % MOD;
    res = (res + ((((((b_u * a_u) % MOD) * LB) % MOD) * LB) % MOD)) % MOD;
    return res;
}

inline int64_t mymod(const int64_t &a){
    return (a>=MOD)?(a%MOD):(a);
}


inline int64_t Tahco::compute_range_hash(std::vector<int64_t> &hash, size_t L, size_t R){
    // return (L==0)?(hash[R]):((MOD + hash[R] - MUL(hash[L-1], hash_base[R - L + 1])) % MOD);
    return (L==0)?(hash[R]):(
            mymod(MOD 
                - mymod((hash[L-1] * hash_base[R - L + 1]))
                + hash[R] 
            ));
}

void Tahco::match(std::string &text, std::vector<int64_t> &hash, std::vector<int64_t> &hashr){
   // std::cerr << text << std::endl;


    StringVector &patterns = (*patterns_ptr);

    size_t p, pr;
    size_t tmp;
    int8_t b;
    int64_t h;
    size_t len = text.length();

    if(hash.size() < len){
        hash.resize(len);
        hashr.resize(len);
    }
    p = 1;
    pr = 1;
    for(size_t i = 0; i < len; ++i){
		if(text[i] == 'N' || text[i] == 'n'){
			hash[i] = 0;
			p = 1;
		}else{
			// update rolling hash
			h = char2idx(text[i]);
    		if(i == 0){
				hash[i] = h;
    	    }else{
        	    hash[i] = mymod(hash[i-1] * 5 + h);
        	}
        	// match process
        	for(b = char2binary(text[i]); p && !nodes[p].next[b]; p = nodes[p].fail);
        	p = (p)?(nodes[p].next[b]):(1);

        	for(tmp = p; tmp > 0; tmp = nodes[tmp].fail){
            	if(nodes[tmp].hashmap){
                	h = compute_range_hash(hash, (i + 1) - (nodes[tmp].depth), i);
                	if(nodes[tmp].hashmap->count(h) > 0){
                    	auto hv = nodes[tmp].hashmap->at(h);
                    	if(patterns[hv]->back() == text[i] && 
                        	patterns[hv]->at(nodes[tmp].depth - 2) == text[i-1] &&
                    		patterns[hv]->at(nodes[tmp].depth - 4) == text[i-3] &&
                           patterns[hv]->at(nodes[tmp].depth - 5) == text[i-4] &&
                           patterns[hv]->at(nodes[tmp].depth - 3) == text[i-2]){
                            ++pattern_cnt[hv];
                        }
                    }
                }
            }
        }
        
        if(text[len - 1 - i] == 'N' || text[len - 1 - i] == 'n'){
            hashr[i] = 0;
            pr = 1;
        }else{
            // update rolling hash
            h = char2idx(char2comp(text[len - 1 - i]));
            if(i == 0){
                hashr[i] = h;
            }else{
                hashr[i] = mymod(hashr[i-1] * 5 + h);
            }
            // match process
            for(b = char2binary(char2comp(text[len - 1 - i])); pr && !nodes[pr].next[b]; pr = nodes[pr].fail);
            pr = (pr)?(nodes[pr].next[b]):(1);

            for(tmp = pr; tmp > 0; tmp = nodes[tmp].fail){
                if(nodes[tmp].hashmap){
                    h = compute_range_hash(hashr, (i + 1) - (nodes[tmp].depth), i);
                    if(nodes[tmp].hashmap->count(h) > 0){
                        auto hv = nodes[tmp].hashmap->at(h);
                        if(patterns[hv]->back() == char2comp(text[len - 1 - i]) &&
                           patterns[hv]->at(nodes[tmp].depth - 2) == char2comp(text[len - 1 - i + 1]) &&
                           patterns[hv]->at(nodes[tmp].depth - 4) == char2comp(text[len - 1 - i + 3]) &&
                           patterns[hv]->at(nodes[tmp].depth - 5) == char2comp(text[len - 1 - i + 4]) &&
                           patterns[hv]->at(nodes[tmp].depth - 3) == char2comp(text[len - 1 - i + 2])){
                            ++pattern_cnt[hv];
                        }
                    }
                }
            }
        }
    }
}

/*
auto &hv =  (*(nodes[tmp].hashmap))[h];
auto range_start = hv.begin();
auto range_end = hv.end();
for(auto it = range_start; it != range_end; ++it){
if(patterns[*it]->back() == text[i]){
++pattern_cnt[*it];
}
}
*/
/*
auto range = tmp->hashmap->equal_range(h);
for(auto it = range.first; it != range.second; ++it){
if(patterns[it->second]->back() == text[i]){
++pattern_cnt[it->second];
}
}
*/

void Tahco::output_results(const std::string &fp){
    StringVector &patterns = (*patterns_ptr);

    std::ofstream wp;
    wp.open(fp);
    for(size_t i = 0; i < num_patterns; ++i){
        if(pattern_cnt[i] > 0){
            wp << (*patterns[i]) << "\t" << pattern_cnt[i] << std::endl;
           // std::cerr << (*patterns[i]) << "\t" << pattern_cnt[i] << std::endl;
        }
    }
    wp.close();
}
