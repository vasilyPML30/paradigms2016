#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include "wsqueue.h"
#include "threadpool.h"

void* task_function(void *arg)
{
    struct ThreadPool *pool = arg;
    struct Task *task;
    while (true)
    {
        wsqueue_wait(&pool->tasks);
        task = (struct Task *)wsqueue_pop(&pool->tasks);
        if (!task) continue;
        if (!task->f) break;
        task->f(task->arg);
        pthread_mutex_lock(&task->mtx);
        task->finished = true;
        pthread_cond_signal(&task->cnd);
        pthread_mutex_unlock(&task->mtx);
    }
    return NULL;
}

void thpool_init(struct ThreadPool *pool, unsigned threads_nm)
{
    unsigned i;
    pool->threads_nm = threads_nm;
    pool->threads = malloc(sizeof(pthread_t) * threads_nm);
    wsqueue_init(&pool->tasks);
    for (i = 0; i < threads_nm; i++)
        pthread_create(&pool->threads[i], NULL, task_function, pool);
}

void thpool_submit(struct ThreadPool *pool, struct Task *task)
{
    pthread_mutex_init(&task->mtx, NULL);
    pthread_cond_init(&task->cnd, NULL);
    task->finished = false;
    wsqueue_push(&pool->tasks, &task->node);
}

void thpool_wait(struct Task *task)
{
    pthread_mutex_lock(&task->mtx);
    while (!task->finished)
        pthread_cond_wait(&task->cnd, &task->mtx);
    pthread_mutex_unlock(&task->mtx);
    pthread_cond_destroy(&task->cnd);
    pthread_mutex_destroy(&task->mtx);
}

void thpool_finit(struct ThreadPool *pool)
{
    unsigned i;
    struct Task *finit_tasks = malloc(sizeof(struct Task) * pool->threads_nm);
    for (i = 0; i < pool->threads_nm; i++)
    {
        finit_tasks[i].f = NULL;
        finit_tasks[i].arg = NULL;
        thpool_submit(pool, &finit_tasks[i]);
    }
    for (i = 0; i < pool->threads_nm; i++)
    {
        pthread_join(pool->threads[i], NULL);
    }    
    free(pool->threads);
    free(finit_tasks);
    wsqueue_finit(&pool->tasks);
}
