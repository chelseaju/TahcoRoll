#CXXFLAGS+=-Ofast -std=c++14 -march=native -Wall -fopenmp -Wextra -Wconversion -flto
CXXFLAGS+= -Ofast  -std=c++14 -march=native -Wall -Wextra -Wconversion -flto 
 
.PHONY: all clean

all: tahcoroll tahcoload

tahcoroll: file_reader.o tahco.o

tahcoload: file_reader.o tahco.o

clean:
	$(RM) tahcoroll tahcoload *.o
