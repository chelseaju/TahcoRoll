#CXXFLAGS+=-Ofast -std=c++14 -march=native -Wall -fopenmp -Wextra -Wconversion -flto
CXXFLAGS+= -Ofast  -std=c++14 -march=native -Wall -Wextra -Wconversion -flto -lpthread 
 
.PHONY: all clean

all: tahcoroll 

tahcoroll: util.o file_reader.o tahco.o

# tahcoload: util.o file_reader.o tahco.o

clean:
	$(RM) tahcoroll tahcoload *.o
