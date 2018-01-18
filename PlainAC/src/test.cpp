#include<iostream>
#include<string>
#include "aho_corasick/src/aho_corasick/aho_corasick.hpp"

using namespace std;

int main(){

	cout << "hello " << endl;

	aho_corasick::trie trie;
	trie.insert("hers");
	trie.insert("his");
	trie.insert("she");
	trie.insert("he");
	string str = "ushers";
	auto result = trie.parse_text(str);

	for(auto r:result){
		cout << r.get_start() << "\t" << r.get_end() << "\t" << str.substr(r.get_start(), r.get_end() - r.get_start()+1) << endl; 

	}

}
