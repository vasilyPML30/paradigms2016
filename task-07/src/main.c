#include "threadpool.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

struct ArrayPart
{
    struct Task *task;
    struct ThreadPool *pool;
    int *base;
    unsigned elements_nm;
    unsigned cur_depth;
    unsigned max_depth;
};

int compare(const void *first, const void *second)
{
    int first_i = *(int *)first;
    int second_i = *(int *)second;
    if (first_i < second_i)
        return -1;
    if (first_i > second_i)
        return 1;
    return 0;
}

void swap(int *first, int *second)
{
    int third = *first;
    *first = *second;
    *second = third;
}

void my_sort(void *arg)
{
    struct ArrayPart *arr = arg;
    int left = 0;
    int right = arr->elements_nm - 1;
    int x = arr->base[right / 2];
    if (arr->cur_depth >= arr->max_depth)
    {
        qsort(arr->base, arr->elements_nm, sizeof(int), compare);
        free(arr);
        return;
    }
    while (left <= right)
    {
        while (arr->base[left] < x) left++;
        while (arr->base[right] > x) right--;
        if (left <= right)
            swap(arr->base + left++, arr->base + right--);
    }
    if (right >= 0)
    {
        struct Task *task1 = malloc(sizeof(struct Task));
        struct ArrayPart *prt1 = malloc(sizeof(struct ArrayPart));
        prt1->base = arr->base;
        prt1->elements_nm = right + 1;
        prt1->cur_depth = arr->cur_depth + 1;
        prt1->max_depth = arr->max_depth;
        prt1->pool = arr->pool;
        task1->arg = prt1;
        task1->f = my_sort;
        task1->left = task1->right = NULL;
        arr->task->left = prt1->task = task1;
        thpool_submit(arr->pool, task1);
    }
    if (left < (int)arr->elements_nm)
    {
        struct Task *task2 = malloc(sizeof(struct Task));
        struct ArrayPart *prt2 = malloc(sizeof(struct ArrayPart));
        prt2->base = arr->base + left;
        prt2->elements_nm = arr->elements_nm - left;
        prt2->cur_depth = arr->cur_depth + 1;
        prt2->max_depth = arr->max_depth;
        prt2->pool = arr->pool;
        task2->arg = prt2;
        task2->f = my_sort;
        arr->task->right = prt2->task = task2;
        task2->left = task2->right = NULL;
        thpool_submit(arr->pool, task2);
    }
    free(arr);
}

void wait_all(struct Task *task)
{
    if (!task)
        return;
    thpool_wait(task);
    wait_all(task->left);
    wait_all(task->right);
    free(task);
}

int main(int argc, char **argv)
{
    struct ArrayPart *arr = malloc(sizeof(struct ArrayPart));
    unsigned i;
    unsigned threads_nm;
    unsigned elements_nm;
    struct ThreadPool pool;
    struct Task *task = malloc(sizeof(struct Task));
    int *base = NULL;
    if (argc < 4)
        return 0;
    threads_nm = atoi(argv[1]);
    arr->elements_nm = elements_nm = atoi(argv[2]);
    arr->max_depth = atoi(argv[3]);
    arr->base = base = malloc(sizeof(int) * elements_nm);
    srand(42);
    for (i = 0; i < elements_nm; i++)
        base[i] = rand();
    arr->cur_depth = 1;
    arr->pool = &pool;
    task->f = my_sort;
    task->arg = arr;
    arr->task = task;
    task->left = task->right = NULL;                                                                                                                                                    
    thpool_init(arr->pool, threads_nm);
    thpool_submit(arr->pool, task);
    wait_all(task);
    thpool_finit(&pool);
    free(base);
    return 0;
}