#ifndef __THREAD_POOL_H__
#define __THREAD_POOL_H__

#include <stdbool.h>
#include <pthread.h>
#include "wsqueue.h"

struct Task
{
    struct list_node node;
    void (*f)(void*);
    void *arg;
    struct Task *left, *right;
    pthread_mutex_t mtx;
    pthread_cond_t cnd;
    bool finished;
};

struct ThreadPool
{
   unsigned threads_nm;
   pthread_t *threads;
   struct wsqueue tasks;
};

void thpool_init(struct ThreadPool *pool, unsigned threads_nm);
void thpool_submit(struct ThreadPool *pool, struct Task *task);
void thpool_wait(struct Task *task);
void thpool_finit(struct ThreadPool *pool);

#endif