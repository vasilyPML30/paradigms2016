CC      ?= gcc -std=C11
CFLAGS  ?= -Wall -Wextra -Werror -ansi -pedantic -I include
LDFLAGS ?= -lpthread

all: bin/main.o bin/linkedlist.o bin/queue.o bin/squeue.o bin/wsqueue.o bin/threadpool.o
	$(CC) bin/main.o bin/linkedlist.o bin/queue.o bin/squeue.o \
		  bin/threadpool.o bin/wsqueue.o $(LDFLAGS) -o pqsort

bin/main.o: src/main.c
	$(CC) -c src/main.c $(CFLAGS) -o bin/main.o

bin/threadpool.o: src/threadpool.c
	$(CC) -c src/threadpool.c $(CFLAGS) -o bin/threadpool.o

bin/linkedlist.o: src/linkedlist.c
	$(CC) -c src/linkedlist.c $(CFLAGS) -o bin/linkedlist.o

bin/queue.o: src/queue.c
	$(CC) -c src/queue.c $(CFLAGS) -o bin/queue.o

bin/squeue.o: src/squeue.c
	$(CC) -c src/squeue.c $(CFLAGS) -o bin/squeue.o

bin/wsqueue.o: src/wsqueue.c
	$(CC) -c src/wsqueue.c $(CFLAGS) -o bin/wsqueue.o

clean:
	rm bin/* pqsort

.PHONY: clean
