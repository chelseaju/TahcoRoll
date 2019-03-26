#include "tahco.hpp"


Node::Node(size_t _depth){
    depth = _depth;
    next[0] = NULL;
    next[1] = NULL;
    fail = NULL;
    hashmap = NULL;
    mtx = new std::mutex();
}

Node::~Node(){
    if(hashmap) delete hashmap;
    if(next[0]) delete next[0];
    if(next[1]) delete next[1];
}

Node* Node::get_next(int8_t c){
    if(next[c] == NULL){
        std::lock_guard<std::mutex> guard_node(*mtx);
        if(next[c] == NULL){
            next[c] = new Node(depth + 1);
        }
    }
    return next[c];
}


Tahco::Tahco(StringVector* _patterns_ptr, const Parameters &params){
    patterns_ptr = _patterns_ptr;
    num_trees = params.num_trees;
    mtx = new std::mutex();
    initialize();
}


void Tahco::initialize(){
    // Patterns
    StringVector &patterns = (*patterns_ptr);
    num_patterns = patterns.size();
    min_len = SIZE_MAX;
    max_len = 0;
    for(size_t i = 0; i < num_patterns; ++i){
        min_len = std::min(min_len, patterns[i]->length());
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


void Tahco::add_patterns_with_range(const size_t st, const size_t ed){
    StringVector &patterns = (*patterns_ptr);
    for(auto i = st; i < ed; ++i){
        add_pattern(*patterns[i], i);
    }
}

void Tahco::profile_patterns(const std::string &fp, const Parameters &params){
    const size_t num_patterns_per_tree = (num_patterns + num_trees - 1) / num_trees;

	double time_construction = 0.0;
	double time_query = 0.0;
    for(size_t iter = 0; iter < num_trees; ++iter){
        std::cerr << "Tree " << iter << std::endl;
        auto st = iter * num_patterns_per_tree;
        auto ed = std::min(st + num_patterns_per_tree, num_patterns);

        // construct a trie
        root = new Node(0);

        // add patterns
        max_len = 0;
        min_len = SIZE_MAX;
        const size_t num_patterns_per_thread = (ed - st + params.num_threads - 1) / params.num_threads;

        ThreadVector threads;
        auto basic_start = std::chrono::system_clock::now();
        for(size_t thread_i = 0; thread_i < params.num_threads; ++thread_i) {
            auto thread_st = st;
            auto thread_ed = std::min(st + num_patterns_per_thread, ed);
            threads.emplace_back(std::thread(&Tahco::add_patterns_with_range, this, thread_st, thread_ed));
            st += num_patterns_per_thread;
        }
        for(auto& th : threads) {
            th.join();
        }
        std::cerr << "Added patterns." << std::endl;
        // build tahco
        build_tahco(params);
		time_construction += get_time_diff(basic_start);
        std::cerr << "Built tacho." << std::endl;
        
        time_query += profile_patterns_with_tahco(fp, params);
        
        delete root;
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



double Tahco::profile_patterns_with_tahco(const std::string &fp, const Parameters &params){
    
    double total_time = 0.0;
    const auto BUFFER_SIZE = 6400 * 1024;

    auto fd = ::open(fp.c_str(), O_RDONLY);
    if(fd == -1){
        std::cerr << "Cannot open " << fp << std::endl;
        exit(0);
    }

    char buf[BUFFER_SIZE + 1];
    auto cur = std::string("");
    auto line_no = 0;

    // std::vector<int64_t> hash;
    // std::vector<int64_t> hashr;
    
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
    int64_t cur_hash = 0;
    Node* cur_node = root;
    for(auto it = pattern.begin(); it != pattern.end(); ++it){
        cur_hash = cur_hash * 5 + char2idx(*it);
        if(cur_hash >= MOD){
            cur_hash %= MOD;
        }
        cur_node = cur_node->get_next(char2binary(*it));
    }

    std::lock_guard<std::mutex> guard(*cur_node->mtx);

    if(cur_node->hashmap == NULL){
        cur_node->hashmap = new Hashmap();
    }

    assert(cur_node->hashmap->count(cur_hash) == 0);
    cur_node->hashmap->insert({{cur_hash, pattern_idx}});
}

void Tahco::build_tahco_from_queue(std::queue<Node*> &q){
    Node* cur;
    Node* p;
    while(!q.empty()){
        cur = q.front();
        q.pop();
        // 0
        if(cur->next[0]){
            for(p = cur->fail; p && p->next[0] == NULL; p = p->fail);
            cur->next[0]->fail = (p)?(p->next[0]):(root);
            q.push(cur->next[0]);
        }
        // 1
        if(cur->next[1]){
            for(p = cur->fail; p && p->next[1] == NULL; p = p->fail);
            cur->next[1]->fail = (p)?(p->next[1]):(root);
            q.push(cur->next[1]);
        }
    }
}

void Tahco::build_tahco(const Parameters &params){
    std::queue<Node*> q;
    std::queue<Node*> q_threads[params.num_threads];
    Node* cur;
    Node* p;

    q.push(root);
    //while(!q.empty()){
    while(!q.empty() && q.size()){
        cur = q.front();
        q.pop();
        // 0
        if(cur->next[0]){
            for(p = cur->fail; p && p->next[0] == NULL; p = p->fail);
            cur->next[0]->fail = (p)?(p->next[0]):(root);
            q.push(cur->next[0]);
        }
        // 1
        if(cur->next[1]){
            for(p = cur->fail; p && p->next[1] == NULL; p = p->fail);
            cur->next[1]->fail = (p)?(p->next[1]):(root);
            q.push(cur->next[1]);
        }
    }

    if(!q.empty()){
        for(int i = 0; !q.empty(); ++i){
            q_threads[i % params.num_threads].push(q.front());
            q.pop();
        }
        ThreadVector threads;
        for(size_t thread_i = 0; thread_i < params.num_threads; ++thread_i) {
            threads.emplace_back(std::thread(&Tahco::build_tahco_from_queue, this, std::ref(q_threads[thread_i])));
        }
        for(auto& th : threads) {
            th.join();
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
    //std::cerr << text << std::endl;

    StringVector &patterns = (*patterns_ptr);

    Node* p;
    Node* pr;
    Node* tmp;
    int8_t b;
    int64_t h;
    size_t len = text.length();

    if(hash.size() < len){
        hash.resize(len);
        hashr.resize(len);
    }
    p = root;
    pr = root;
    for(size_t i = 0; i < len; ++i){
		if(text[i] == 'N' || text[i] == 'n'){
			hash[i] = 0;
			p = root;
		}else{
			// update rolling hash
			h = char2idx(text[i]);
    		if(i == 0){
				hash[i] = h;
    	    }else{
        	    hash[i] = mymod(hash[i-1] * 5 + h);
        	}
        	// match process
        	for(b = char2binary(text[i]); p && p->next[b] == NULL; p = p->fail);

        	p = (p)?(p->next[b]):(root);

        	for(tmp = p; tmp; tmp = tmp->fail){
            	if(tmp->hashmap){
                	h = compute_range_hash(hash, (i + 1) - (tmp->depth), i);
                	if(tmp->hashmap->count(h) > 0){
                    	auto hv = tmp->hashmap->at(h);
                        /*
                    	if(patterns[hv]->back() == text[i]){
                            ++pattern_cnt[hv];
                        }
                        */
                    	if(patterns[hv]->back() == text[i] &&
                           patterns[hv]->at(tmp->depth - 2) == text[i-1] &&
                           patterns[hv]->at(tmp->depth - 4) == text[i-3] &&
                           patterns[hv]->at(tmp->depth - 5) == text[i-4] &&
                           patterns[hv]->at(tmp->depth - 3) == text[i-2]){
                            std::lock_guard<std::mutex> guard_node(*mtx);
                            ++pattern_cnt[hv];
                        }
                    }
                }
            }
        }
        
        if(text[len - 1 - i] == 'N' || text[len - 1 - i] == 'n'){
            hashr[i] = 0;
            pr = root;
        }else{
            // update rolling hash
            h = char2idx(char2comp(text[len - 1 - i]));
            if(i == 0){
                hashr[i] = h;
            }else{
                hashr[i] = mymod(hashr[i-1] * 5 + h);
            }
            // match process
            for(b = char2binary(char2comp(text[len - 1 - i])); pr && pr->next[b] == NULL; pr = pr->fail);

            pr = (pr)?(pr->next[b]):(root);

            for(tmp = pr; tmp; tmp = tmp->fail){
                if(tmp->hashmap){
                    h = compute_range_hash(hashr, (i + 1) - (tmp->depth), i);
                    if(tmp->hashmap->count(h) > 0){
                        auto hv = tmp->hashmap->at(h);
                        /*
                        if(patterns[hv]->back() == char2comp(text[len - 1 - i])){
                            ++pattern_cnt[hv];
                        }
                        */
                        if(patterns[hv]->back() == char2comp(text[len - 1 - i]) &&
                           patterns[hv]->at(tmp->depth - 2) == char2comp(text[len - 1 - i + 1]) &&
                           patterns[hv]->at(tmp->depth - 4) == char2comp(text[len - 1 - i + 3]) &&
                           patterns[hv]->at(tmp->depth - 5) == char2comp(text[len - 1 - i + 4]) &&
                           patterns[hv]->at(tmp->depth - 3) == char2comp(text[len - 1 - i + 2])){
                            std::lock_guard<std::mutex> guard_node(*mtx);
                            ++pattern_cnt[hv];
                        }
                    }
                }
            }
        }
    }
}


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

