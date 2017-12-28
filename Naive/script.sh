mprof run -C python naive_v1.py -s /home/chelseaju/TahcoRoll/Data/Reference/Human_DNA/small_01200000_sortedSize.txt -i /home/chelseaju/TahcoRoll/Data/DNA/len75_sample_01/sample.fq -o /home/chelseaju/TahcoRoll/Results/Naive/len75_01_small_012.txt
mv mprofile* /home/chelseaju/TahcoRoll/Results/Naive/len75_01_small_012.log

mprof run -C python naive_v1.py -s /home/chelseaju/TahcoRoll/Data/Reference/Human_DNA/small_06000000_sortedSize.txt -i /home/chelseaju/TahcoRoll/Data/DNA/len75_sample_01/sample.fq -o /home/chelseaju/TahcoRoll/Results/Naive/len75_01_small_060.txt
mv mprofile* /home/chelseaju/TahcoRoll/Results/Naive/len75_01_small_060.log

mprof run -C python naive_v1.py -s /home/chelseaju/TahcoRoll/Data/Reference/Human_DNA/small_12000000_sortedSize.txt -i /home/chelseaju/TahcoRoll/Data/DNA/len75_sample_01/sample.fq -o /home/chelseaju/TahcoRoll/Results/Naive/len75_01_small_120.txt
mv mprofile* /home/chelseaju/TahcoRoll/Results/Naive/len75_01_small_120.log

mprof run -C python naive_v1.py -s /home/chelseaju/TahcoRoll/Data/Reference/Human_DNA/small_24000000_sortedSize.txt -i /home/chelseaju/TahcoRoll/Data/DNA/len75_sample_01/sample.fq -o /home/chelseaju/TahcoRoll/Results/Naive/len75_01_small_240.txt
mv mprofile* /home/chelseaju/TahcoRoll/Results/Naive/len75_01_small_240.log

