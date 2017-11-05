#CXXFLAGS+=-Ofast -std=c++14 -march=native -Wall -fopenmp -Wextra -Wconversion -flto
CXXFLAGS+= -Ofast  -std=c++14 -march=native -Wall -Wextra -Wconversion -flto 
 
.PHONY: all clean

all: tahcoroll

tahcoroll: file_reader.o tahco.o

clean:
	$(RM) tahcoroll *.o
